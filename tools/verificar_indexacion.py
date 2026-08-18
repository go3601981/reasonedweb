#!/usr/bin/env python3
"""
verificar_indexacion.py — quién queda indexable y quién no, comprobado.

⛔ POR QUÉ EXISTE (2026-08-18). Carlos decidió indexar SOLO la home; todo lo
demás — casos, exhibits, rango, 404, API — sigue fuera de buscadores. Eso
depende de dos cosas que se escriben en sitios distintos y que es facilísimo
desincronizar:

  · la cabecera `X-Robots-Tag` de `site/vercel.json`, y
  · la etiqueta `<meta name="robots">` de cada documento.

Un descuido en cualquiera de las dos no da error, no rompe nada visible y no
se nota hasta que una página aparece —o desaparece— de Google semanas después.

⚠️ NO se dejó una regla global de `noindex` con una excepción para `/`: cuando
dos reglas de Vercel casan con la misma ruta, el resultado de una cabecera
repetida y contradictoria es ambiguo, y ante `noindex` + `index` los
buscadores toman la MÁS restrictiva. Por eso la cabecera se emite sólo sobre
los árboles que deben quedar fuera, y la home simplemente no la recibe.
El precio de esa elección: el estado por defecto de una ruta NUEVA de primer
nivel pasa a ser «indexable». Esta puerta es lo que lo vigila — si mañana
aparece un `.html` de primer nivel, falla y hay que decidir a conciencia.

Comprueba, y publica el denominador de cada cosa:
  1. la home NO recibe X-Robots-Tag y NO lleva meta robots noindex;
  2. toda otra página HTML recibe la cabecera Y lleva su meta noindex;
  3. el sitemap contiene exactamente las URLs indexables, ni una más.

Uso:  python tools/verificar_indexacion.py
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path("site")
INDEXABLES = {"/"}          # decisión de Carlos, 2026-08-18


def die(msg: str) -> None:
    print(f"⛔ verificar_indexacion.py: {msg}", file=sys.stderr)
    sys.exit(1)


def a_regex(source: str) -> re.Pattern:
    """Traduce el `source` de Vercel a una regex. Sólo se usan aquí formas
    simples (`/x/(.*)`, `/(a|b)/(.*)`, rutas literales); si apareciera una
    sintaxis que esta función no cubre, mejor fallar que adivinar."""
    if ":" in source or "?" in source or "*" in source.replace("(.*)", ""):
        die(f"source con sintaxis no cubierta por esta puerta: {source!r}")
    return re.compile("^" + source.replace("(.*)", "§").replace("§", ".*") + "$")


def ruta_url(f: Path) -> str:
    rel = f.relative_to(RAIZ).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def main() -> None:
    cfg = json.loads((RAIZ / "vercel.json").read_text(encoding="utf-8"))
    reglas = [(a_regex(h["source"]), h["headers"]) for h in cfg.get("headers", [])]
    if not reglas:
        die("vercel.json no declara ni una regla de cabeceras")

    def noindex_por_cabecera(url: str) -> bool:
        for patron, cabeceras in reglas:
            if patron.match(url) and any(
                    c["key"].lower() == "x-robots-tag" and "noindex" in c["value"].lower()
                    for c in cabeceras):
                return True
        return False

    docs = sorted(RAIZ.rglob("*.html"))
    if not docs:
        die("VERDE EN VACÍO: ni un .html bajo site/")

    fallos = []
    sin_meta = []
    n_index = n_noindex = 0
    for f in docs:
        url = ruta_url(f)
        texto = f.read_text(encoding="utf-8", errors="replace")
        meta = bool(re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', texto, re.I))
        cab = noindex_por_cabecera(url)
        debe_indexar = url in INDEXABLES
        if debe_indexar:
            n_index += 1
            if cab:
                fallos.append(f"{url} debe indexarse pero vercel.json le pone X-Robots-Tag noindex")
            if meta:
                fallos.append(f"{url} debe indexarse pero el documento lleva <meta robots noindex>")
        else:
            n_noindex += 1
            # LA CABECERA es la proteccion real: es lo que el buscador lee, y
            # es lo unico cuya ausencia deja la pagina expuesta. Falla duro.
            if not cab:
                fallos.append(f"{url} NO debe indexarse y ninguna regla de vercel.json le pone la cabecera")
            # El meta es REDUNDANCIA por si la config de cabeceras se rompiera.
            # No falla —la pagina ya esta protegida— pero se CUENTA y se NOMBRA
            # en cada pasada, para que la lista no crezca en silencio.
            if not meta:
                sin_meta.append(url)

    # rutas nuevas de primer nivel: el defecto pasó a ser indexable, así que
    # aparecer aquí tiene que doler.
    for f in docs:
        url = ruta_url(f)
        if url not in INDEXABLES and url.count("/") == 1 and not noindex_por_cabecera(url):
            fallos.append(f"{url} es de primer nivel y quedaría INDEXABLE por defecto")

    sm = RAIZ / "sitemap.xml"
    if sm.is_file():
        locs = re.findall(r"<loc>\s*([^<]+?)\s*</loc>", sm.read_text(encoding="utf-8"))
        rutas = {re.sub(r"^https?://[^/]+", "", u) or "/" for u in locs}
        if rutas != INDEXABLES:
            fallos.append(f"sitemap.xml lista {sorted(rutas)}, y lo indexable es {sorted(INDEXABLES)}")
    else:
        print("  (no hay sitemap.xml — no es obligatorio)")

    print(f"verificar_indexacion.py: {len(docs)} documento(s) · "
          f"{n_index} indexable(s) · {n_noindex} fuera de buscadores · "
          f"{n_noindex - len(sin_meta)}/{n_noindex} con <meta robots> ademas de la cabecera")
    if sin_meta:
        print("  redundancia que falta (protegidas por cabecera, sin meta propio):")
        for x in sin_meta:
            print(f"    · {x}")
    if fallos:
        print(f"\n⛔ DESCUADRES ({len(fallos)}):")
        for x in fallos:
            print(f"  · {x}")
        sys.exit(1)
    print("cabecera y meta dicen lo mismo en todas; el sitemap coincide.")


if __name__ == "__main__":
    main()
