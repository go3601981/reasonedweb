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

⚠️ ENMIENDA 2026-08-17 — LA PUERTA ESCANEA TAMBIÉN LOS ASSETS COPIADOS.
Escaneaba solo el HTML, y por ese hueco entró al sitio un `qr-target.json`
que nombraba un dominio prohibido — y, peor, el `qr.png` de al lado era un
CÓDIGO QR que mandaba a cualquier teléfono que lo escaneara a ese dominio.
Un residuo puede viajar en un asset, y dentro de un QR ni siquiera es legible.
  · ficheros de TEXTO (por extensión): se escanean enteros contra TODOS los
    patrones;
  · BINARIOS: solo contra los patrones de MARCA, y sobre las cadenas
    imprimibles largas, como haría `strings`. Escanear un .glb comprimido
    como si fuera texto da falsos positivos garantizados — `$96` y `$29`
    aparecen en el ruido de cualquier binario grande. Medido, no supuesto.

--sub  reescribe una cadena en el HTML y en los assets de texto, contando las
       sustituciones y fallando si no tocó ninguna.
--qr   REGENERA un PNG como código QR de la URL dada: la única manera de
       arreglar un residuo que vive dentro de una imagen.

Uso:
  python tools/exhibir.py --src PIEZA.html --dest DIR --label "TEXTO"
      [--drop CLASE ...] [--min-dropped N] [--assets CARPETA ...]
      [--sub "VIEJA=NUEVA" ...] [--qr "ruta/rel.png=https://…"]
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

PROHIBIDOS = [
    r"wemadeyoursite", r"WeMadeYourSite", r"WMYS",
    r"[Tt]u[Ww]eb\.pe", r"eureka\.pe", r"[Nn]ext ?[Ll]atam", r"nextlatam",
    r"wa\.me",
    r"\$995", r"\$96\b", r"\$29\b", r"S/500", r"S/50\b",
]


TEXTO_EXT = {".html", ".htm", ".css", ".js", ".mjs", ".json", ".svg", ".txt",
             ".md", ".xml", ".csv", ".webmanifest", ".map"}
MARCAS = [p for p in PROHIBIDOS if not p.startswith("\\$") and not p.startswith("S/")]
CADENA_IMPRIMIBLE = re.compile(rb"[ -~]{6,}")
# el meta de robots, tolerando comilla simple o doble en el atributo
PATRON_ROBOTS = r"<meta[^>]+name=['\"]robots['\"][^>]+noindex"
META_ROBOTS = '<meta name="robots" content="noindex, nofollow">'


def escanear_arbol(raiz: Path):
    """(n_ficheros, residuos). Texto entero contra TODOS los patrones; binario
    solo contra MARCAS y sobre cadenas imprimibles — ver docstring."""
    residuos = []
    n = 0
    for f in sorted(raiz.rglob("*")):
        if not f.is_file():
            continue
        n += 1
        datos = f.read_bytes()
        if f.suffix.lower() in TEXTO_EXT:
            texto = datos.decode("utf-8", errors="replace")
            patrones = PROHIBIDOS
        else:
            texto = "\n".join(x.decode("ascii")
                              for x in CADENA_IMPRIMIBLE.findall(datos))
            patrones = MARCAS
        for pat in patrones:
            for m in re.finditer(pat, texto, re.IGNORECASE):
                ctx = texto[max(0, m.start() - 45):m.end() + 45].replace("\n", " ")
                residuos.append(f"  · {f.relative_to(raiz)} → «…{ctx}…»")
    return n, residuos


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
    ap.add_argument("--label-after", default=None, metavar="CADENA",
                    help="ancla la etiqueta honesta JUSTO DESPUÉS de esa cadena "
                         "en vez de antes de </body>. Necesario en piezas de "
                         "IMPRESIÓN: añadir un bloque al final del cuerpo crea "
                         "una página en blanco de más. Falla si no encuentra el "
                         "ancla — la etiqueta nunca se queda sin poner")
    ap.add_argument("--sub", action="append", default=[], metavar="VIEJA=NUEVA",
                    help="reescribe una cadena en el HTML y en los assets de "
                         "texto; falla si no sustituyó nada (repetible). Si la "
                         "cadena VIEJA contiene '=' (un atributo href, p. ej.), "
                         "usar la forma sed: |VIEJA|NUEVA")
    ap.add_argument("--qr", action="append", default=[], metavar="RUTA=URL",
                    help="regenera ese PNG del exhibit como código QR de la URL "
                         "dada — un residuo dentro de una imagen no se puede "
                         "sanitizar de otra forma (repetible)")
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

    # 2-bis · noindex propio. La cabecera global de Vercel ya protege estas
    # rutas, pero desde que la home SI se indexa (2026-08-18) la redundancia
    # deja de ser adorno: si la config de cabeceras se tocara, el meta es lo
    # unico que queda en pie.
    meta_puesto = 0
    if not re.search(PATRON_ROBOTS, html, re.IGNORECASE):
        if "</head>" not in html:
            die("la pieza no tiene </head> donde poner el noindex")
        html = html.replace(
            "</head>",
            META_ROBOTS + "\n</head>", 1)
        meta_puesto = 1

    # 3 · etiqueta honesta al pie
    etiqueta = ('<div style="background:#16181C;color:#F3F4F3;padding:0.7rem 1rem;'
                'text-align:center;font:500 12px/1.5 system-ui,sans-serif;'
                'letter-spacing:0.02em">' + a.label + "</div>")
    if a.label_after:
        if a.label_after not in html:
            die(f"--label-after: el ancla no aparece en la pieza: {a.label_after!r}")
        html = html.replace(a.label_after, a.label_after + "\n" + etiqueta, 1)
    else:
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

    subs = []
    for regla in a.sub:
        # forma sed |VIEJA|NUEVA: la única manera de sustituir una cadena que
        # contiene '=' (split("=") partiría dentro de un href="…")
        if regla.startswith("|"):
            partes = regla.split("|", 2)
            if len(partes) != 3 or not partes[1]:
                die(f"--sub sed mal formado (se espera |VIEJA|NUEVA): {regla!r}")
            viejo, nuevo = partes[1], partes[2]
        elif "=" in regla:
            viejo, nuevo = regla.split("=", 1)
        else:
            die(f"--sub mal formado (falta '='): {regla!r}")
        subs.append((viejo, nuevo))
    tocados = {viejo: 0 for viejo, _ in subs}
    for viejo, nuevo in subs:
        tocados[viejo] += html.count(viejo)
        html = html.replace(viejo, nuevo)

    (dest / "index.html").write_text(html, encoding="utf-8", newline="")

    # --assets acepta CARPETA o FICHERO suelto: hay piezas (un one-pager de
    # impresión, por ejemplo) cuyos assets viven al lado del HTML, no en una
    # carpeta. Un fichero suelto se copia manteniendo su nombre, que es lo que
    # el HTML referencia.
    copiadas = 0
    for ruta in a.assets:
        origen = src.parent / ruta
        if origen.is_dir():
            shutil.copytree(origen, dest / ruta, dirs_exist_ok=True)
        elif origen.is_file():
            (dest / ruta).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origen, dest / ruta)
        else:
            die(f"asset no existe (ni carpeta ni fichero): {origen}")
        copiadas += 1

    # 6 · --sub también en los assets de TEXTO (ahí se escondía el residuo)
    for f in dest.rglob("*"):
        if (not f.is_file() or f.suffix.lower() not in TEXTO_EXT
                or f.name == "index.html"):
            continue
        t = f.read_text(encoding="utf-8", errors="replace")
        original = t
        for viejo, nuevo in subs:
            tocados[viejo] += t.count(viejo)
            t = t.replace(viejo, nuevo)
        if t != original:
            f.write_text(t, encoding="utf-8", newline="")
    for viejo, veces in tocados.items():
        if veces == 0:
            die(f"--sub no sustituyó NADA para {viejo!r} — o la cadena cambió "
                f"en la fuente o la regla sobra; en ambos casos hay que mirarla")

    # 7 · QR: el residuo que vive dentro de una imagen
    qrs = []
    for regla in a.qr:
        if "=" not in regla:
            die(f"--qr mal formado (falta '='): {regla!r}")
        rel, url = regla.split("=", 1)
        destino = dest / rel
        if not destino.is_file():
            die(f"--qr: el PNG a regenerar no existe: {destino}")
        try:
            import segno
        except ImportError:
            die("--qr necesita `segno` (pip install segno)")
        antes = destino.stat().st_size
        with Image.open(destino) as im:
            lado = im.width
        # La escala se DERIVA del tamaño original, no se elige: un QR
        # reescalado a un tamaño que no es múltiplo exacto de su matriz deja
        # módulos de anchos distintos, y eso lo vuelve difícil de leer.
        simbolo = segno.make(url, error="m")
        modulos = simbolo.symbol_size(border=2)[0]
        escala = max(1, round(lado / modulos))
        simbolo.save(str(destino), scale=escala, border=2, kind="png")
        with Image.open(destino) as im:
            final = im.width
        qrs.append(f"{rel} → {url} ({antes}B → {destino.stat().st_size}B, "
                   f"{lado}px → {final}px = {modulos} módulos × {escala})")

    # 8 · LA PUERTA, ahora sobre TODO el exhibit y no solo sobre el HTML
    n_ficheros, residuos = escanear_arbol(dest)
    if n_ficheros == 0:
        die("VERDE EN VACÍO: el exhibit no tiene ni un fichero que escanear")
    if residuos:
        die(f"RESIDUO PROHIBIDO en el exhibit ({len(residuos)}) — "
            f"{n_ficheros} fichero(s) escaneados:\n" + "\n".join(residuos[:10]))

    print(f"exhibir.py: {dest} · {dropped} bloque(s) eliminados · "
          f"{n_ficheros} fichero(s) escaneados, residuo 0/{len(PROHIBIDOS)} patrones · "
          f"{copiadas} carpeta(s) de assets · {len(fuentes)} fuente(s) compartida(s)"
          + (" · noindex inyectado" if meta_puesto else " · noindex ya venia")
          + (f" · subs: {sum(tocados.values())} ocurrencia(s)" if subs else "")
          + (f" · QR: " + "; ".join(qrs) if qrs else ""))


if __name__ == "__main__":
    main()
