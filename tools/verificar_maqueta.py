#!/usr/bin/env python3
"""
verificar_maqueta.py — nada con texto se sale de su columna.

⛔ POR QUÉ EXISTE (2026-08-18). El bloque de la demo de 48 horas se inserto
por error DESPUES del `</div>` de `.wrap`, no dentro: quedo como hijo directo
de `<section>`, sin ancho maximo ni padding, pegado al borde izquierdo de la
ventana y con el texto cortado. Lo vio Carlos en pantalla.

Lo grave no es el fallo: es que NINGUNA de las puertas del sitio lo vio.
`auditar.py` mide contraste y desborde del documento — la caja no desbordaba
por la derecha. La puerta de hallazgos moviles mide dianas, pares y tamano de
texto. Ninguna comprobaba lo mas basico de una maqueta: que el contenido este
DENTRO de la caja de texto.

Comprueba dos cosas, y publica el denominador de cada una:
  1. ESTRUCTURA: el unico hijo directo de cada <section> es `div.wrap`. Es la
     convencion del sitio y es la que se rompio.
  2. MEDIDA: ningun elemento con texto propio y visible tiene su borde
     izquierdo a la izquierda del contenido de su `.wrap`, ni el derecho a la
     derecha. Se mide en el navegador, a varios anchos, porque un margen
     negativo o un `width` en `vw` producen el mismo sintoma sin tocar el HTML.

Exentos, y se dice cuantos son: lo posicionado en absoluto o fijo (sellos y
adornos), lo marcado `aria-hidden`, y las notas al margen (`.fn-note.al-margen`
flotan a la derecha del texto por diseno, ver § Pase de diseno).

Uso:  python tools/verificar_maqueta.py --base http://127.0.0.1:8791
      [--paths / /work/... ] [--widths 320,768,1440]
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

import websocket

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 9381

SONDA = r"""(() => {
  // Se recorre CADA elemento con texto una sola vez y se compara contra SU
  // propia columna (`closest('.wrap')`). La primera version iteraba por wrap
  // y miraba `wrap.parentElement`, asi que el wrap del hero —hijo de <main>—
  // media ademas todo el resto de la pagina, contra la columna equivocada.
  const fuera = [];
  let medidos = 0, exentos = 0;
  const cajas = new Set();
  for (const el of document.querySelectorAll('body *')) {
    const propio = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!propio) continue;
    const wrap = el.closest('.wrap');
    if (!wrap) continue;
    cajas.add(wrap);
    const e = el.getBoundingClientRect();
    if (e.width === 0 || e.height === 0) continue;
    const ecs = getComputedStyle(el);
    if (ecs.display === 'none' || ecs.visibility === 'hidden') continue;
    if (ecs.position === 'absolute' || ecs.position === 'fixed'
        || el.closest('[aria-hidden="true"]') || el.closest('.fn-note.al-margen')
        || e.left < -5000) { exentos++; continue; }
    const cs = getComputedStyle(wrap), r = wrap.getBoundingClientRect();
    const izq = r.left + parseFloat(cs.paddingLeft);
    const der = r.right - parseFloat(cs.paddingRight);
    medidos++;
    if (e.left < izq - 1.5 || e.right > der + 1.5) {
      fuera.push({sel: el.tagName.toLowerCase()
                    + (el.className && typeof el.className === 'string'
                       ? '.' + el.className.trim().split(/\s+/).join('.') : ''),
                  txt: el.textContent.trim().slice(0, 34),
                  izq: +e.left.toFixed(1), der: +e.right.toFixed(1),
                  columna: [+izq.toFixed(1), +der.toFixed(1)]});
    }
  }
  return {fuera, medidos, exentos, cajas: cajas.size};
})()"""


def die(msg):
    print(f"⛔ verificar_maqueta.py: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--paths", nargs="+", default=["/"])
    ap.add_argument("--widths", default="320,768,1440")
    a = ap.parse_args()
    anchos = [int(x) for x in a.widths.split(",")]

    # 1 · estructura, sin navegador: el hijo directo de cada section
    fallos_estruct, n_sec, n_notas = [], 0, 0
    for f in sorted(Path("site").rglob("index.html")):
        if any(p in f.parts for p in ("live", "piece", "deck", "range", "molecules", "one-pager")):
            continue
        t = f.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r'<section id="([a-z-]+)"', t):
            n_sec += 1
            cuerpo = t[m.end():t.index("  </section>", m.start())]
            hijos = [h[0] for h in re.findall(r"\n    <([a-z]+)([^>]*)>", cuerpo)]
            if hijos != ["div"]:
                fallos_estruct.append(f"{f.relative_to('site')} · <section id=\"{m.group(1)}\"> "
                                      f"tiene hijos directos {hijos}, se espera solo div.wrap")
        # ⛔ Las notas al pie CUELGAN DEL .wrap, nunca de una caja interior.
        # `apparatus.js` las flota al margen en pantallas anchas: metida dentro
        # de un bloque con borde —la oferta de 48h— la nota flotaba DENTRO del
        # recuadro, estrujada a la derecha, con medio bloque vacio al lado.
        # Se ve mal y ninguna otra puerta lo notaba: el texto seguia dentro de
        # su columna, que es lo unico que se estaba midiendo.
        for m in re.finditer(r'<aside class="fn-note" id="([^"]+)"', t):
            ini = t.rfind(chr(10), 0, m.start()) + 1
            sangria = m.start() - ini
            n_notas += 1
            if sangria != 6:
                fallos_estruct.append(
                    f"{f.relative_to('site')} · la nota #{m.group(1)} esta anidada "
                    f"({sangria} espacios de sangria, se esperan 6): no cuelga del "
                    f".wrap y flotara dentro de su caja en vez de al margen")
    if n_sec == 0:
        die("VERDE EN VACÍO: cero secciones inspeccionadas")

    prof = Path(tempfile.mkdtemp(prefix="maqueta-"))
    proc = subprocess.Popen([
        EDGE, "--headless=new", "--no-first-run", "--hide-scrollbars",
        f"--remote-debugging-port={PORT}", f"--remote-allow-origins=http://127.0.0.1:{PORT}",
        f"--user-data-dir={prof}", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ws = None
    for _ in range(60):
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

    conn = websocket.create_connection(ws, timeout=60)
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

    cmd("Page.enable")
    cmd("Runtime.enable")
    fallos_medida, medidos, exentos, vistas = [], 0, 0, 0
    try:
        for ruta in a.paths:
            for w in anchos:
                cmd("Emulation.setDeviceMetricsOverride", width=w, height=900,
                    deviceScaleFactor=1, mobile=w < 992)
                cmd("Page.navigate", url=a.base.rstrip("/") + ruta)
                time.sleep(1.6)
                d = cmd("Runtime.evaluate", expression=SONDA,
                        returnByValue=True)["result"].get("value")
                if not d or d["cajas"] == 0:
                    die(f"{ruta}@{w}: cero contenedores .wrap — ¿se cargó la página?")
                vistas += 1
                medidos += d["medidos"]
                exentos += d["exentos"]
                for x in d["fuera"]:
                    fallos_medida.append(
                        f"{ruta}@{w} · {x['sel']} «{x['txt']}» ocupa "
                        f"[{x['izq']}, {x['der']}] y su columna es {x['columna']}")
    finally:
        proc.terminate()

    print(f"verificar_maqueta.py: {n_sec} sección(es) y {n_notas} nota(s) por estructura · "
          f"{vistas} vista(s), {medidos} elemento(s) con texto medidos, "
          f"{exentos} exento(s) (absolutos, aria-hidden, notas al margen)")
    if medidos == 0:
        die("VERDE EN VACÍO: no se midió ni un elemento con texto")
    todos = fallos_estruct + fallos_medida
    if todos:
        print(f"\n⛔ FUERA DE COLUMNA ({len(todos)}):")
        for x in todos:
            print(f"  · {x}")
        sys.exit(1)
    print("todo el texto cae dentro de su columna.")


if __name__ == "__main__":
    main()
