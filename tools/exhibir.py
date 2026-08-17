#!/usr/bin/env python3
"""
exhibir.py — copia SANITIZADA de una pieza para exhibición viva en el sitio.

⛔ LA FRONTERA, enmendada por Carlos (2026-08-16): el HTML de una pieza puede
cruzar SOLO como exhibición congelada y sanitizada — sin banners ajenos, sin
precios ajenos, sin metadatos de otra marca. La copia es un exhibit, no un
fork vivo: no se mantiene, se re-genera desde la fuente con esta herramienta.

Qué hace:
  1. Elimina bloques por clase (banners, ofertas, pies ajenos) contando nodos.
  2. Elimina <meta>/<link> y comentarios HTML que mencionen marcas ajenas.
  3. Inyecta la etiqueta honesta de Reasoned Web al pie (regla 1 del sitio).
  4. Copia las carpetas de assets de la pieza.

VERDE EN VACÍO — puerta de residuo: tras sanitizar, el HTML de salida se
escanea contra la lista de patrones prohibidos; si queda UNO, FALLA nombrando
cada residuo con su contexto. Una copia sin escanear tendría cara de limpia.

Uso:
  python tools/exhibir.py --src PIEZA.html --dest DIR --label "TEXTO"
      [--drop CLASE ...] [--min-dropped N] [--assets CARPETA ...]
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

PROHIBIDOS = [
    r"wemadeyoursite", r"WeMadeYourSite", r"WMYS",
    r"[Tt]u[Ww]eb\.pe", r"eureka\.pe", r"[Nn]ext ?[Ll]atam", r"nextlatam",
    r"wa\.me",
    r"\$995", r"\$96\b", r"\$29\b", r"S/500", r"S/50\b",
]


def die(msg: str) -> None:
    print(f"⛔ exhibir.py: {msg}", file=sys.stderr)
    sys.exit(1)


def quitar_bloque_por_clase(html: str, clase: str):
    """Elimina cada elemento cuyo atributo class contenga la clase dada,
    balanceando etiquetas del mismo tipo. Devuelve (html, n_eliminados)."""
    n = 0
    patron = re.compile(
        r"<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*class=\"[^\"]*\b" + re.escape(clase) + r"\b[^\"]*\"[^>]*>")
    while True:
        m = patron.search(html)
        if not m:
            return html, n
        tag = m.group(1)
        abre = re.compile(r"<" + tag + r"\b[^>]*>", re.IGNORECASE)
        cierra = re.compile(r"</" + tag + r"\s*>", re.IGNORECASE)
        prof = 1
        pos = m.end()
        while prof > 0:
            ma = abre.search(html, pos)
            mc = cierra.search(html, pos)
            if not mc:
                die(f"bloque .{clase}: <{tag}> sin cierre — la pieza no es la esperada")
            if ma and ma.start() < mc.start():
                # las etiquetas vacías (img, br, input…) no anidan
                if not ma.group(0).endswith("/>") and tag.lower() not in (
                        "img", "br", "hr", "input", "meta", "link", "source"):
                    prof += 1
                pos = ma.end()
            else:
                prof -= 1
                pos = mc.end()
        html = html[:m.start()] + html[pos:]
        n += 1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dest", required=True, help="carpeta destino del exhibit")
    ap.add_argument("--label", required=True,
                    help="etiqueta honesta visible al pie (regla 1)")
    ap.add_argument("--drop", action="append", default=[],
                    help="clase CSS cuyo elemento entero se elimina (repetible)")
    ap.add_argument("--min-dropped", type=int, default=0,
                    help="mínimo de bloques que la limpieza debe eliminar")
    ap.add_argument("--assets", action="append", default=[],
                    help="carpeta de assets a copiar junto a la pieza (repetible)")
    ap.add_argument("--fonts-from", default=None,
                    help="carpeta compartida de fuentes: cada ../fonts/X se "
                         "reescribe a fonts/X y el archivo se copia al exhibit")
    a = ap.parse_args()

    src = Path(a.src)
    dest = Path(a.dest)
    if not src.is_file():
        die(f"fuente no existe: {src}")
    html = src.read_text(encoding="utf-8", newline="")

    # 1 · bloques visibles ajenos
    dropped = 0
    for clase in a.drop:
        html, n = quitar_bloque_por_clase(html, clase)
        dropped += n
    if dropped < a.min_dropped:
        die(f"limpieza eliminó {dropped} bloque(s), mínimo {a.min_dropped}")

    # 2 · metadatos y comentarios con marcas ajenas
    marca = re.compile("|".join(PROHIBIDOS))
    html = re.sub(r"<!--(?:(?!-->).)*?-->",
                  lambda m: "" if marca.search(m.group(0)) else m.group(0),
                  html, flags=re.DOTALL)
    html = re.sub(r"/\*(?:(?!\*/).)*?\*/",
                  lambda m: "" if marca.search(m.group(0)) else m.group(0),
                  html, flags=re.DOTALL)
    html = re.sub(r"[ \t]*<(?:meta|link)\b[^>]*>\s*?\n?",
                  lambda m: "" if marca.search(m.group(0)) else m.group(0),
                  html)
    # JSON-LD apuntando a dominios ajenos: el bloque entero se va
    html = re.sub(r"[ \t]*<script type=\"application/ld\+json\"[^>]*>"
                  r"(?:(?!</script>).)*?</script>\s*?\n?",
                  lambda m: "" if marca.search(m.group(0)) else m.group(0),
                  html, flags=re.DOTALL)

    # 3 · etiqueta honesta al pie
    etiqueta = ('<div style="background:#16181C;color:#F3F4F3;padding:0.7rem 1rem;'
                'text-align:center;font:500 12px/1.5 system-ui,sans-serif;'
                'letter-spacing:0.02em">' + a.label + "</div>")
    if "</body>" not in html:
        die("la pieza no tiene </body> donde anclar la etiqueta")
    html = html.replace("</body>", etiqueta + "\n</body>", 1)

    # 4 · puerta de residuo: cero menciones prohibidas en la salida
    residuos = []
    for pat in PROHIBIDOS:
        for m in re.finditer(pat, html):
            ini = max(0, m.start() - 40)
            residuos.append(f"  · «…{html[ini:m.end()+40]}…»")
    if residuos:
        die("RESIDUO PROHIBIDO tras sanitizar (" + str(len(residuos)) +
            "):\n" + "\n".join(residuos[:10]))

    # 5 · fuentes compartidas: ../fonts/X → fonts/X, copiando cada archivo
    fuentes = sorted(set(re.findall(r"\.\./fonts/([A-Za-z0-9_.-]+)", html)))
    if fuentes and not a.fonts_from:
        die(f"la pieza referencia ../fonts/ ({len(fuentes)} archivo(s)) "
            f"pero no se dio --fonts-from")
    dest.mkdir(parents=True, exist_ok=True)
    if fuentes:
        origen_fonts = Path(a.fonts_from)
        (dest / "fonts").mkdir(exist_ok=True)
        for nombre in fuentes:
            f = origen_fonts / nombre
            if not f.is_file():
                die(f"fuente referenciada no existe: {f}")
            shutil.copy2(f, dest / "fonts" / nombre)
        html = html.replace("../fonts/", "fonts/")
        if "../fonts/" in html:
            die("quedaron referencias ../fonts/ sin reescribir")

    (dest / "index.html").write_text(html, encoding="utf-8", newline="")

    copiadas = 0
    for carpeta in a.assets:
        origen = src.parent / carpeta
        if not origen.is_dir():
            die(f"carpeta de assets no existe: {origen}")
        shutil.copytree(origen, dest / carpeta, dirs_exist_ok=True)
        copiadas += 1

    print(f"exhibir.py: {dest} · {dropped} bloque(s) eliminados · "
          f"residuo 0/{len(PROHIBIDOS)} patrones · {copiadas} carpeta(s) de assets · "
          f"{len(fuentes)} fuente(s) compartida(s)")


if __name__ == "__main__":
    main()
