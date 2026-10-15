#!/usr/bin/env python3
"""
verificar_assets.py — todo lo que el sitio PIDE tiene que existir Y estar en git.

⛔ POR QUÉ EXISTE (2026-08-17). Las quince imágenes `-1080.webp` estaban en el
disco de Carlos y referenciadas en los `srcset`, pero nunca se commitearon. En
local todo se veía perfecto; en producción daban 404 y las tarjetas salían
rotas. El bug era invisible desde la máquina que lo creó, que es la clase de
bug que sólo caza una puerta.

Y no se rompía todo, lo que lo hacía aún más difícil de leer: una tarjeta
normal declara `sizes: 32rem` → a DPR 2 el navegador pide 1024 px y elige el
candidato de 1080w → 404. El catálogo declara `34rem` → pide 1088 px, el 1080
se le queda corto y salta al 1440, que sí estaba commiteado. Media galería
rota y media bien, según la aritmética de `sizes` × DPR.

Comprueba, para cada fichero LOCAL que el HTML referencia:
  1. que existe en el disco,
  2. que no está vacío,
  3. y que git lo SIGUE — porque lo que se despliega es lo commiteado, no lo
     que hay en la carpeta.

VERDE EN VACÍO: publica el denominador (cuántas referencias miró, en cuántos
documentos) y FALLA si contó cero — un escaneo que no escaneó nada no puede
dar «todo bien».

Uso:
  python tools/verificar_assets.py [--raiz site]
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

# src/href/poster y los data-* del reproductor progresivo. Los subtítulos
# viven en data-en/data-es hasta que apparatus.js crea los <track> al pulsar.
ATRIBUTOS = re.compile(
    r'(?:data-poster|data-en|data-es|src|href|poster)="([^"#?][^"]*?\.'
    r'(?:webp|png|jpg|jpeg|gif|svg|ico|css|js|mjs|json|woff2|woff|ttf|pdf|glb|usdz|mp4|webm|vtt))"',
    re.IGNORECASE)
SRCSET = re.compile(r'srcset="([^"]+)"')
EXTERNO = ("http://", "https://", "data:", "//", "mailto:", "tel:")


def die(msg: str) -> None:
    print(f"⛔ verificar_assets.py: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", default="site")
    a = ap.parse_args()
    raiz = Path(a.raiz)
    if not raiz.is_dir():
        die(f"raíz no existe: {raiz}")

    seguidos = set(subprocess.run(
        ["git", "ls-files", str(raiz)],
        capture_output=True, text=True, check=True).stdout.split("\n"))
    if not seguidos or seguidos == {""}:
        die("git no devolvió ni un fichero seguido — ¿esto es un repo?")

    docs = sorted(raiz.rglob("*.html"))
    if not docs:
        die(f"VERDE EN VACÍO: ni un .html bajo {raiz}")

    faltan, vacios, sin_git = [], [], []
    refs_totales = 0
    for doc in docs:
        texto = doc.read_text(encoding="utf-8", errors="replace")
        refs = set(ATRIBUTOS.findall(texto))
        for lista in SRCSET.findall(texto):
            for cand in lista.split(","):
                cand = cand.strip()
                if cand:
                    refs.add(cand.split()[0])
        for url in sorted(refs):
            if url.startswith(EXTERNO):
                continue
            refs_totales += 1
            destino = (doc.parent / url).resolve()
            donde = f"{doc.relative_to(raiz)} → {url}"
            if not destino.is_file():
                faltan.append(donde)
                continue
            if destino.stat().st_size == 0:
                vacios.append(donde)
            try:
                rel = destino.relative_to(Path.cwd()).as_posix()
            except ValueError:
                continue                      # fuera del repo: no es cosa de git
            if rel not in seguidos:
                sin_git.append(f"{rel}   ← {doc.relative_to(raiz)}")

    print(f"verificar_assets.py: {len(docs)} documento(s), "
          f"{refs_totales} referencia(s) local(es) comprobadas")
    if refs_totales == 0:
        die("VERDE EN VACÍO: cero referencias locales — el escaneo no midió nada")

    problemas = 0
    for titulo, lista in (("NO EXISTEN", faltan),
                          ("VACÍOS (0 bytes)", vacios),
                          ("EXISTEN PERO GIT NO LOS SIGUE — darán 404 al desplegar",
                           sorted(set(sin_git)))):
        if lista:
            problemas += len(lista)
            print(f"\n⛔ {titulo} ({len(lista)}):")
            for x in lista:
                print(f"  · {x}")
    if problemas:
        sys.exit(1)
    print("todo referenciado existe, pesa y está en git.")


if __name__ == "__main__":
    main()
