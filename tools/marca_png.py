#!/usr/bin/env python3
"""
marca_png.py — la marca en PNG con fondo transparente, para sobreimprimir.

Para qué: poner el lockup encima de un vídeo. La web usa el SVG (nítido a
cualquier resolución), pero un editor de vídeo quiere un PNG con canal alfa.

Se rasteriza con el MISMO navegador que pinta el sitio, no con una librería
aparte: los SVG de `brand/` los genera `derive.py` y llevan `fill="currentColor"`,
así que el color se impone desde fuera sin tocar el fichero, y lo que sale es
exactamente lo que se ve en la página. Una librería de rasterizado distinta
sería una segunda opinión sobre la forma de la marca, y la marca no admite
segundas opiniones.

⛔ VERDE EN VACÍO — un PNG transparente VACÍO pesa poco, se abre sin error y
parece perfectamente correcto hasta que se monta sobre el vídeo y no hay nada.
Por eso cada fichero se ABRE y se comprueba:
  · que tiene píxeles transparentes (si no, el fondo se coló);
  · que tiene píxeles opacos (si no, está vacío);
  · que el color de los opacos es el pedido (si no, currentColor no se aplicó);
  · y que la tinta cubre entre el 2 % y el 80 % del lienzo — fuera de esa
    horquilla no es una marca, es un borrón o una mota.
Falla nombrando el fichero y el número que no cuadra.

Uso:  python tools/marca_png.py [--dest brand/png]
"""
import argparse
import base64
import json
import subprocess
import sys
import tempfile
import time
import urllib.request
from collections import Counter
from pathlib import Path

import websocket
from PIL import Image

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 9403

COLORES = {"ink": "#16181C", "blanco": "#FFFFFF"}
PIEZAS = {
    "lockup": ("brand/lockup.svg", (2400, 1200, 600)),
    "glifo": ("brand/glyph.svg", (1024, 512)),
}


def die(msg: str) -> None:
    print(f"⛔ marca_png.py: {msg}", file=sys.stderr)
    sys.exit(1)


def arranca():
    prof = Path(tempfile.mkdtemp(prefix="marca-"))
    proc = subprocess.Popen([
        EDGE, "--headless=new", "--no-first-run", "--hide-scrollbars",
        f"--remote-debugging-port={PORT}",
        f"--remote-allow-origins=http://127.0.0.1:{PORT}",
        f"--user-data-dir={prof}", "--force-device-scale-factor=1", "about:blank",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ws = None
    for _ in range(70):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json") as r:
                pg = [t for t in json.load(r) if t.get("type") == "page"]
            if pg:
                ws = pg[0]["webSocketDebuggerUrl"]
                break
        except OSError:
            pass
        time.sleep(0.25)
    if not ws:
        proc.terminate()
        die("Edge no expuso el puerto de debugging")
    return proc, websocket.create_connection(ws, timeout=60)


def revisa(f: Path, color_hex: str):
    """Devuelve (ancho, alto, cobertura). Falla si el PNG no es una marca."""
    esperado = tuple(int(color_hex[i:i + 2], 16) for i in (1, 3, 5))
    im = Image.open(f).convert("RGBA")
    px = list(im.getdata())
    alfas = [p[3] for p in px]
    if min(alfas) != 0:
        die(f"{f.name}: no hay ni un píxel transparente — el fondo se coló")
    solidos = [p for p in px if p[3] == 255]
    if not solidos:
        die(f"{f.name}: ni un píxel opaco — el PNG está vacío")
    dominante = Counter((p[0], p[1], p[2]) for p in solidos).most_common(1)[0][0]
    if max(abs(a - b) for a, b in zip(dominante, esperado)) > 6:
        die(f"{f.name}: la tinta es {dominante} y se pidió {esperado} — "
            f"currentColor no se aplicó")
    cobertura = len(solidos) / len(px)
    if not (0.02 <= cobertura <= 0.80):
        die(f"{f.name}: la tinta cubre el {cobertura:.1%} del lienzo — "
            f"fuera de la horquilla 2-80%, no parece una marca")
    return im.width, im.height, cobertura


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", default="brand/png")
    a = ap.parse_args()
    dest = Path(a.dest)
    dest.mkdir(parents=True, exist_ok=True)

    proc, conn = arranca()
    mid = [0]

    def cmd(m, **p):
        mid[0] += 1
        conn.send(json.dumps({"id": mid[0], "method": m, "params": p}))
        while True:
            r = json.loads(conn.recv())
            if r.get("id") == mid[0]:
                if "error" in r:
                    die(f"CDP {m}: {r['error']}")
                return r.get("result", {})

    hechos = []
    try:
        cmd("Page.enable")
        cmd("Runtime.enable")
        cmd("Emulation.setDefaultBackgroundColorOverride",
            color={"r": 0, "g": 0, "b": 0, "a": 0})
        for pieza, (ruta, anchos) in PIEZAS.items():
            svg = Path(ruta).read_text(encoding="utf-8")
            svg = svg[svg.index("<svg"):]                    # fuera el comentario
            for nombre_color, hex_color in COLORES.items():
                for ancho in anchos:
                    html = (
                        "<!doctype html><meta charset='utf-8'>"
                        "<style>html,body{margin:0;padding:0;background:transparent}"
                        f"#m{{display:block;width:{ancho}px;height:auto;color:{hex_color}}}"
                        "</style><div id='w'>" + svg.replace("<svg", "<svg id='m'", 1) + "</div>")
                    cmd("Page.navigate", url="data:text/html;charset=utf-8," +
                        urllib.parse.quote(html))
                    time.sleep(0.5)
                    caja = cmd("Runtime.evaluate", returnByValue=True, expression=(
                        "(() => { const r = document.getElementById('m')"
                        ".getBoundingClientRect();"
                        " return {w: r.width, h: r.height}; })()"
                    ))["result"].get("value")
                    if not caja or caja["h"] < 1:
                        die(f"{pieza}@{ancho}: el SVG no midió nada")
                    alto = int(round(caja["h"]))
                    cmd("Emulation.setDeviceMetricsOverride", width=ancho, height=alto,
                        deviceScaleFactor=1, mobile=False)
                    time.sleep(0.25)
                    datos = base64.b64decode(cmd(
                        "Page.captureScreenshot", format="png", captureBeyondViewport=True,
                        clip={"x": 0, "y": 0, "width": ancho, "height": alto, "scale": 1}
                    )["data"])
                    f = dest / f"reasonedweb-{pieza}-{nombre_color}-{ancho}.png"
                    f.write_bytes(datos)
                    w, h, cob = revisa(f, hex_color)
                    hechos.append(f"{f.name}  {w}×{h}  {f.stat().st_size/1024:.1f} KB  "
                                  f"tinta {cob:.1%}")
    finally:
        proc.terminate()

    if not hechos:
        die("VERDE EN VACÍO: no se generó ni un PNG")
    print(f"marca_png.py: {len(hechos)} PNG con alfa, todos verificados "
          f"(transparencia, tinta, color y cobertura)")
    for h in hechos:
        print("  ·", h)


if __name__ == "__main__":
    import urllib.parse
    main()
