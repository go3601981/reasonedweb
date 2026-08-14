#!/usr/bin/env python3
"""
inline_brand.py — inyecta los másters de brand/ como SVG inline en el sitio.

Los másters usan currentColor: inline heredan la tinta del contexto (nav en
tinta, pie en papel) sin duplicar archivos ni elegir colores nuevos. Al
cambiar la fuente: brand/derive.py re-emite los másters y esto se re-corre.

Idempotente: el bloque inyectado queda entre <!--BRAND:X--> y <!--/BRAND:X-->
y se reemplaza completo en cada corrida.

VERDE EN VACÍO: falla si un máster no aporta contenido o si un archivo del
sitio no contiene el token que dice tener.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "brand"
SITE = ROOT / "site"

TARGETS = {
    SITE / "index.html": ["LOCKUP", "WORDMARK"],
    SITE / "work" / "lg-sound-suite" / "index.html": ["LOCKUP"],
    SITE / "work" / "ulric-de-varens" / "index.html": ["LOCKUP"],
    SITE / "work" / "smoothies" / "index.html": ["LOCKUP"],
    SITE / "work" / "the-woods-and-co" / "index.html": ["LOCKUP"],
}
SOURCES = {"LOCKUP": BRAND / "lockup.svg", "WORDMARK": BRAND / "wordmark-stacked.svg"}


def die(msg: str) -> None:
    print(f"⛔ inline_brand.py: {msg}", file=sys.stderr)
    sys.exit(1)


def load_svg(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = re.search(r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*)</svg>', text, re.S)
    if not m:
        die(f"{path.name}: no encuentro <svg viewBox>…</svg>")
    view_box, inner = m.group(1), m.group(2).strip()
    if not inner:
        die(f"{path.name}: el máster está vacío — nada que inyectar")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" '
            f'aria-hidden="true" focusable="false">{inner}</svg>')


def main() -> None:
    svgs = {k: load_svg(p) for k, p in SOURCES.items()}
    total = 0
    for target, keys in TARGETS.items():
        html = target.read_text(encoding="utf-8")
        for k in keys:
            pat = re.compile(rf"<!--BRAND:{k}-->(?:.*?<!--/BRAND:{k}-->)?", re.S)
            found = len(pat.findall(html))
            if found == 0:
                die(f"{target.relative_to(ROOT)}: token BRAND:{k} ausente")
            html = pat.sub(lambda _: f"<!--BRAND:{k}-->{svgs[k]}<!--/BRAND:{k}-->", html)
            total += found
            print(f"  {target.relative_to(ROOT)}: {k} × {found}")
        target.write_text(html, encoding="utf-8", newline="\n")
    if total == 0:
        die("0 inyecciones — no hubo nada que hacer")
    print(f"inline_brand.py: {total} inyecciones")


if __name__ == "__main__":
    main()
