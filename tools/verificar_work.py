#!/usr/bin/env python3
"""Verify the generated Work index and its progressive filter in a real browser.

The no-JavaScript contract is checked against the shipped HTML/CSS: all cards
must be present and unhidden before enhancement, while the filter controls are
hidden until the early `js` class is added. The enhanced state is exercised in
headless Edge, including native keyboard activation, arrow-key focus and Escape.

Usage: python tools/verificar_work.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

import websocket


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "site" / "work" / "index.html"
HOME = ROOT / "site" / "index.html"
DATA = ROOT / "site" / "data" / "work.json"
CSS = ROOT / "site" / "assets" / "css" / "work.css"
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
PORT = 9382


def die(message: str) -> None:
    print(f"verificar_work.py: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    projects = json.loads(DATA.read_text(encoding="utf-8"))["projects"]
    expected = len(projects)
    page = PAGE.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")

    cards = re.findall(r'<article class="work-card"[^>]*>', page)
    if len(cards) != expected or any(" hidden" in card for card in cards):
        die(f"no-JS HTML has {len(cards)} cards for {expected} projects, or a card is hidden")
    if not re.search(r"\.work-filters\s*\{\s*display:\s*none", css):
        die("base CSS does not hide the inert filters")
    if not re.search(r"\.js\s+\.work-filters\s*\{[^}]*display:\s*flex", css, re.S):
        die("enhanced CSS does not reveal the filters")
    if "\ufffd" in page or "\ufffd" in DATA.read_text(encoding="utf-8") or "\ufffd" in css:
        die("a U+FFFD replacement character reached a Work index source")

    if not EDGE.is_file():
        die(f"Edge executable not found at {EDGE}")
    profile = tempfile.TemporaryDirectory(prefix="reasoned-work-")
    process = subprocess.Popen(
        [
            str(EDGE), "--headless=new", "--no-first-run", "--hide-scrollbars",
            f"--remote-debugging-port={PORT}",
            f"--remote-allow-origins=http://127.0.0.1:{PORT}",
            f"--user-data-dir={profile.name}", "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    connection = None
    try:
        endpoint = None
        for _ in range(60):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json") as response:
                    tabs = [tab for tab in json.load(response) if tab.get("type") == "page"]
                if tabs:
                    endpoint = tabs[0]["webSocketDebuggerUrl"]
                    break
            except OSError:
                pass
            time.sleep(0.25)
        if not endpoint:
            die("Edge did not expose its debugging endpoint")
        connection = websocket.create_connection(endpoint, timeout=60)
        message_id = 0

        def command(method: str, **params: object) -> dict[str, object]:
            nonlocal message_id
            message_id += 1
            connection.send(json.dumps({"id": message_id, "method": method, "params": params}))
            while True:
                result = json.loads(connection.recv())
                if result.get("id") == message_id:
                    if "error" in result:
                        die(f"browser {method} failed: {result['error']}")
                    return result.get("result", {})

        def evaluate(expression: str) -> object:
            result = command("Runtime.evaluate", expression=expression, returnByValue=True)
            return result["result"].get("value")

        command("Page.enable")
        command("Runtime.enable")
        command("Page.bringToFront")
        command("Emulation.setDeviceMetricsOverride", width=1280, height=900,
                deviceScaleFactor=1, mobile=False)
        command("Page.navigate", url=PAGE.resolve().as_uri())
        time.sleep(1.2)

        initial = evaluate("""(() => ({
          js: document.documentElement.classList.contains('js'),
          filters: getComputedStyle(document.querySelector('.work-filters')).display,
          cards: document.querySelectorAll('.work-card').length,
          visible: [...document.querySelectorAll('.work-card')].filter(c => !c.hidden).length,
          buttons: [...document.querySelectorAll('.work-filter')].map(b => b.textContent.trim())
        }))()""")
        expected_labels = [item["label"] for item in json.loads(DATA.read_text(encoding="utf-8"))["categories"]]
        if initial != {
            "js": True, "filters": "flex", "cards": expected, "visible": expected,
            "buttons": expected_labels,
        }:
            die(f"unexpected initial enhanced state: {initial}")

        # Enter on a focused native button must invoke the same filter as a click.
        evaluate("document.querySelector('[data-filter=\"films\"]').focus()")
        command("Input.dispatchKeyEvent", type="rawKeyDown", key="Enter", code="Enter",
                windowsVirtualKeyCode=13, nativeVirtualKeyCode=13)
        command("Input.dispatchKeyEvent", type="char", key="Enter", code="Enter", text="\r",
                windowsVirtualKeyCode=13, nativeVirtualKeyCode=13)
        command("Input.dispatchKeyEvent", type="keyUp", key="Enter", code="Enter",
                windowsVirtualKeyCode=13, nativeVirtualKeyCode=13)
        filtered = evaluate("""(() => ({
          visible: [...document.querySelectorAll('.work-card')].filter(c => !c.hidden).length,
          pressed: document.querySelector('[data-filter="films"]').getAttribute('aria-pressed'),
          status: document.getElementById('work-status').textContent
        }))()""")
        if filtered["visible"] != 2 or filtered["pressed"] != "true" or "2 of" not in filtered["status"]:
            die(f"Films keyboard filter failed: {filtered}")

        # Escape clears the current filter; arrow keys move focus among the four buttons.
        command("Input.dispatchKeyEvent", type="keyDown", key="Escape", code="Escape")
        command("Input.dispatchKeyEvent", type="keyUp", key="Escape", code="Escape")
        cleared = evaluate("[...document.querySelectorAll('.work-card')].filter(c => !c.hidden).length")
        if cleared != expected:
            die(f"Escape left {cleared} of {expected} cards visible")
        evaluate("document.querySelector('[data-filter=\"decks\"]').focus()")
        command("Input.dispatchKeyEvent", type="keyDown", key="ArrowRight", code="ArrowRight")
        command("Input.dispatchKeyEvent", type="keyUp", key="ArrowRight", code="ArrowRight")
        focused = evaluate("document.activeElement.textContent.trim()")
        if focused != "Interactive & 3D":
            die(f"ArrowRight focused {focused!r}, not 'Interactive & 3D'")

        # The new film remains a plain MP4 link without JS. With enhancement,
        # keyboard activation replaces it in place and carries both caption files.
        command("Page.navigate", url=HOME.resolve().as_uri() + "#lg-magnit")
        time.sleep(1.2)
        featured = evaluate("""(() =>
          document.querySelectorAll('#decks article.card').length +
          document.querySelectorAll('#ar .case-lead').length +
          document.querySelectorAll('#film .case-lead').length +
          document.querySelectorAll('#lg .case-lead').length +
          document.querySelectorAll('#brandwork article.card').length
        )()""")
        if featured != 6:
            die(f"home page exposes {featured} featured projects, expected 6")
        film_link = evaluate("""(() => {
          const a = document.querySelector('a.film[href="assets/video/lg-magnit.mp4"]');
          if (!a) return null;
          return {
            en: a.dataset.en,
            es: a.dataset.es,
            poster: a.dataset.poster,
            kind: a.dataset.trackKind,
            href: a.getAttribute('href')
          };
        })()""")
        expected_film = {
            "en": "assets/video/lg-magnit.en.vtt",
            "es": "assets/video/lg-magnit.es.vtt",
            "poster": "assets/img/work/lg-magnit-1080.webp",
            "kind": "captions",
            "href": "assets/video/lg-magnit.mp4",
        }
        if film_link != expected_film:
            die(f"LG MAGNIT fallback/data attributes differ: {film_link}")
        evaluate("document.querySelector('a.film[href=\"assets/video/lg-magnit.mp4\"]').focus()")
        command("Input.dispatchKeyEvent", type="keyDown", key="Enter", code="Enter")
        command("Input.dispatchKeyEvent", type="keyUp", key="Enter", code="Enter")
        time.sleep(0.4)
        player = evaluate("""(() => {
          const video = document.querySelector('video.film-player');
          if (!video) return null;
          return {
            source: video.querySelector('source')?.getAttribute('src'),
            poster: video.getAttribute('poster'),
            focused: document.activeElement === video,
            tracks: [...video.querySelectorAll('track')].map(track => ({
              kind: track.kind,
              language: track.srclang,
              src: track.getAttribute('src'),
              default: track.default
            }))
          };
        })()""")
        expected_tracks = [
            {"kind": "captions", "language": "en", "src": "assets/video/lg-magnit.en.vtt", "default": True},
            {"kind": "captions", "language": "es", "src": "assets/video/lg-magnit.es.vtt", "default": False},
        ]
        if not player or player["source"] != "assets/video/lg-magnit.mp4" or not player["focused"] or player["tracks"] != expected_tracks:
            die(f"LG MAGNIT enhanced player failed: {player}")

        print(
            f"verificar_work.py: {expected} no-JS card(s), 4 exact filter(s), "
            "2 Film result(s), 6 home features; filter keys and LG MAGNIT captions passed in Edge"
        )
    finally:
        if connection is not None:
            connection.close()
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        profile.cleanup()


if __name__ == "__main__":
    main()
