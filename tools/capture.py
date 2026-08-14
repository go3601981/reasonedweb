#!/usr/bin/env python3
"""
capture.py — capturas de piezas para el sitio, con limpieza verificada.

⛔ LA FRONTERA: de las otras carpetas SOLO CRUZAN PÍXELES. Esta herramienta
sirve para producirlos: navega una URL local, ELIMINA los selectores pedidos
(p. ej. el banner de deslinde de otra marca — el sitio publicado no puede
mencionar ninguna marca que no sea Reasoned Web, y un píxel con su nombre es
una mención) y captura el viewport.

VERDE EN VACÍO: si se pidió eliminar selectores, la captura FALLA cuando
eliminó menos nodos del mínimo esperado — una limpieza que no limpió nada
produciría un píxel contaminado con cara de verificado.

Uso:
  python tools/capture.py --url URL --out out.png [--size 1440x900]
                          [--remove ".aviso" --min-removed 1] [--settle 2.0]
"""
import argparse
import base64
import json
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

import websocket

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 9333


def die(msg: str) -> None:
    print(f"⛔ capture.py: {msg}", file=sys.stderr)
    sys.exit(1)


class CDP:
    def __init__(self, ws_url: str):
        self.ws = websocket.create_connection(ws_url, timeout=60)
        self.mid = 0

    def cmd(self, method: str, **params):
        self.mid += 1
        self.ws.send(json.dumps({"id": self.mid, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.mid:
                if "error" in msg:
                    die(f"CDP {method}: {msg['error']}")
                return msg.get("result", {})

    def wait_event(self, name: str, timeout: float = 30.0):
        end = time.time() + timeout
        self.ws.settimeout(max(1.0, timeout))
        while time.time() < end:
            msg = json.loads(self.ws.recv())
            if msg.get("method") == name:
                return msg
        die(f"esperando {name}: timeout")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1440x900")
    ap.add_argument("--remove", action="append", default=[],
                    help="selector CSS a eliminar antes de capturar (repetible)")
    ap.add_argument("--min-removed", type=int, default=None,
                    help="mínimo de nodos que la limpieza debe eliminar "
                         "(default: 1 si hay --remove, 0 si no)")
    ap.add_argument("--settle", type=float, default=2.0,
                    help="segundos de asentamiento tras load (fuentes, imágenes)")
    args = ap.parse_args()
    w, h = (int(v) for v in args.size.split("x"))
    min_removed = args.min_removed if args.min_removed is not None else (1 if args.remove else 0)

    profile = Path(tempfile.mkdtemp(prefix="capture-edge-"))
    proc = subprocess.Popen([
        EDGE, "--headless=new", "--no-first-run", "--hide-scrollbars",
        f"--remote-debugging-port={PORT}",
        f"--remote-allow-origins=http://127.0.0.1:{PORT}",
        f"--user-data-dir={profile}",
        f"--window-size={w},{h}",
        "about:blank",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ws_url = None
        for _ in range(50):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json") as r:
                    targets = json.load(r)
                pages = [t for t in targets if t.get("type") == "page"]
                if pages:
                    ws_url = pages[0]["webSocketDebuggerUrl"]
                    break
            except OSError:
                pass
            time.sleep(0.2)
        if not ws_url:
            die("Edge no expuso el puerto de debugging")

        cdp = CDP(ws_url)
        cdp.cmd("Page.enable")
        cdp.cmd("Emulation.setDeviceMetricsOverride",
                width=w, height=h, deviceScaleFactor=1, mobile=False)
        cdp.cmd("Page.navigate", url=args.url)
        cdp.wait_event("Page.loadEventFired", timeout=60)
        time.sleep(args.settle)

        removed = 0
        if args.remove:
            sel = ", ".join(args.remove)
            expr = (f"(() => {{ const ns = document.querySelectorAll({json.dumps(sel)});"
                    f" ns.forEach(n => n.remove()); return ns.length; }})()")
            res = cdp.cmd("Runtime.evaluate", expression=expr, returnByValue=True)
            removed = res.get("result", {}).get("value", 0)
            if removed < min_removed:
                die(f"limpieza insuficiente: eliminó {removed} nodo(s) de "
                    f"{sel!r}, mínimo {min_removed} — el píxel saldría contaminado")

        shot = cdp.cmd("Page.captureScreenshot", format="png")
        data = base64.b64decode(shot["data"])
        if len(data) < 1000:
            die(f"captura sospechosamente vacía ({len(data)} bytes)")
        Path(args.out).write_bytes(data)
        print(f"capture.py: {args.out} · {w}x{h} · {len(data)} bytes · "
              f"eliminados {removed} nodo(s)")
    finally:
        proc.terminate()


if __name__ == "__main__":
    main()
