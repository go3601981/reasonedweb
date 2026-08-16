#!/usr/bin/env python3
"""
record.py — walkthroughs en video de piezas para el sitio, con limpieza verificada.

⛔ LA FRONTERA: de las otras carpetas SOLO CRUZAN PÍXELES ("capturas y video").
Esta herramienta produce el video: navega una URL local, ELIMINA los selectores
pedidos (marcas ajenas, banners, precios ajenos), recorre la página con un
scroll suave y codifica los frames a MP4 (H.264, mudo).

VERDE EN VACÍO (tres puertas, cada una nombra su denominador):
  1. limpieza: si se pidió eliminar, FALLA cuando eliminó menos del mínimo.
  2. cobertura: FALLA si el scroll no recorrió ≥95% del alto de la página.
  3. frames: FALLA con cero frames capturados o encode vacío.

Uso:
  python tools/record.py --url URL --out out.mp4 --ffmpeg RUTA
      [--size 1440x900] [--remove ".aviso" --min-removed 1]
      [--duration 22] [--fps 8] [--settle 3] [--tail 1.5] [--scale 960]
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
PORT = 9341


def die(msg: str) -> None:
    print(f"⛔ record.py: {msg}", file=sys.stderr)
    sys.exit(1)


class CDP:
    def __init__(self, ws_url: str):
        self.ws = websocket.create_connection(ws_url, timeout=90)
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

    def js(self, expr: str, awaited: bool = True):
        r = self.cmd("Runtime.evaluate", expression=expr,
                     returnByValue=True, awaitPromise=awaited)
        return r.get("result", {}).get("value")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ffmpeg", required=True, help="ruta al binario ffmpeg")
    ap.add_argument("--size", default="1440x900")
    ap.add_argument("--remove", action="append", default=[],
                    help="selector CSS a eliminar antes de grabar (repetible)")
    ap.add_argument("--min-removed", type=int, default=None,
                    help="mínimo de nodos que la limpieza debe eliminar")
    ap.add_argument("--duration", type=float, default=22.0,
                    help="segundos del recorrido de scroll")
    ap.add_argument("--fps", type=int, default=8)
    ap.add_argument("--settle", type=float, default=3.0)
    ap.add_argument("--tail", type=float, default=1.5,
                    help="segundos quietos al final del recorrido")
    ap.add_argument("--scale", type=int, default=960, help="ancho del MP4")
    a = ap.parse_args()
    w, h = (int(x) for x in a.size.split("x"))
    out = Path(a.out)
    if a.remove and a.min_removed is None:
        die("--remove sin --min-removed: la limpieza sin mínimo es verde en vacío")

    prof = tempfile.mkdtemp(prefix="record-")
    frames_dir = Path(tempfile.mkdtemp(prefix="record-frames-"))
    proc = subprocess.Popen(
        [EDGE, f"--remote-debugging-port={PORT}", "--remote-allow-origins=*",
         f"--user-data-dir={prof}", "--headless=new", f"--window-size={w},{h}",
         "--autoplay-policy=no-user-gesture-required", "--mute-audio",
         "--hide-scrollbars", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ws_url = None
        for _ in range(50):
            try:
                tabs = json.loads(urllib.request.urlopen(
                    f"http://127.0.0.1:{PORT}/json", timeout=2).read())
                pages = [t for t in tabs if t.get("type") == "page"]
                if pages:
                    ws_url = pages[0]["webSocketDebuggerUrl"]
                    break
            except Exception:
                pass
            time.sleep(0.3)
        if not ws_url:
            die("Edge no expuso pestaña CDP")

        c = CDP(ws_url)
        c.cmd("Page.enable")
        c.cmd("Runtime.enable")
        c.cmd("Emulation.setDeviceMetricsOverride", width=w, height=h,
              deviceScaleFactor=1, mobile=False)
        c.cmd("Page.navigate", url=a.url)
        time.sleep(a.settle)

        # ── puerta 1: limpieza verificada ─────────────────────────────
        removed = 0
        if a.remove:
            sels = json.dumps(a.remove)
            removed = c.js(f"""(() => {{
              let n = 0;
              for (const s of {sels})
                document.querySelectorAll(s).forEach(el => {{ el.remove(); n++; }});
              return n; }})()""")
            if removed < a.min_removed:
                die(f"limpieza eliminó {removed} nodo(s), mínimo {a.min_removed} — "
                    f"un video sin limpiar tendría cara de verificado")

        alto = c.js("document.documentElement.scrollHeight")

        # ── scroll suave (fire-and-forget) + captura a ritmo fijo ─────
        c.js(f"""(() => {{
          const D = {a.duration} * 1000;
          const H = document.documentElement.scrollHeight - innerHeight;
          const t0 = performance.now();
          const ease = t => t < .5 ? 2*t*t : 1 - Math.pow(-2*t + 2, 2) / 2;
          (function paso() {{
            const p = Math.min(1, (performance.now() - t0) / D);
            scrollTo(0, H * ease(p));
            if (p < 1) requestAnimationFrame(paso);
          }})();
        }})()""", awaited=False)

        total = int((a.duration + a.tail) * a.fps)
        t0 = time.time()
        n = 0
        for i in range(total):
            objetivo = t0 + i / a.fps
            espera = objetivo - time.time()
            if espera > 0:
                time.sleep(espera)
            shot = c.cmd("Page.captureScreenshot", format="png")
            (frames_dir / f"f-{i:05d}.png").write_bytes(base64.b64decode(shot["data"]))
            n += 1

        # ── puerta 2: cobertura del recorrido ─────────────────────────
        fin = c.js("window.scrollY + window.innerHeight")
        cobertura = fin / alto if alto else 0
        if cobertura < 0.95:
            die(f"el scroll cubrió {cobertura:.0%} del alto ({fin}/{alto}px) — "
                f"el recorrido no muestra la pieza entera")

        # ── puerta 3: frames y encode ─────────────────────────────────
        if n == 0:
            die("cero frames capturados")
        enc = subprocess.run(
            [a.ffmpeg, "-y", "-framerate", str(a.fps),
             "-i", str(frames_dir / "f-%05d.png"),
             "-vf", f"scale={a.scale}:-2",
             "-c:v", "libx264", "-preset", "medium", "-crf", "30",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)],
            capture_output=True, text=True)
        if enc.returncode != 0:
            die(f"ffmpeg falló: {enc.stderr[-400:]}")
        peso = out.stat().st_size if out.exists() else 0
        if peso == 0:
            die("encode produjo un archivo vacío")

        print(f"record.py: {out} · {n} frames @ {a.fps}fps · "
              f"cobertura {cobertura:.0%} · eliminados {removed} nodo(s) · "
              f"{peso/1e6:.1f} MB")
    finally:
        proc.kill()


if __name__ == "__main__":
    main()
