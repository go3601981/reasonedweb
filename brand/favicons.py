#!/usr/bin/env python3
"""
favicons.py — el glifo en rejilla entera de píxel: 16/32/48 PNG + favicon.ico.

Derivación: en viewBox 100 el módulo es m=12 → a tamaño S px,
m_px = round(S × 12/100): 16→1.92≈2 · 32→3.84≈4 · 48→5.76≈6.
El redondeo a rejilla entera ES la derivación a resolución de dispositivo:
cuatro rellenos alineados al píxel, cero antialias, no puede emborronarse.

Geometría en módulos (idéntica a brand/glyph.svg):
  barra 5m×m; canal m; tres cuadrados m×m con gaps m; total 5m × 3m, centrado.

VERDE EN VACÍO: cada PNG se verifica contando píxeles de tinta — deben ser
exactamente 8m² (barra 5m² + 3 cuadrados 3m²). Cero o distinto = error.
"""
import sys
from pathlib import Path

from PIL import Image

BRAND = Path(__file__).resolve().parent
SITE = BRAND.parent / "site"
INK = (0x16, 0x18, 0x1C, 255)
SIZES = (16, 32, 48)


def die(msg: str) -> None:
    print(f"⛔ favicons.py: {msg}", file=sys.stderr)
    sys.exit(1)


def render(size: int) -> Image.Image:
    m = round(size * 12 / 100)
    if m < 1:
        die(f"tamaño {size}px: módulo redondea a 0 — no hay glifo posible")
    x0 = (size - 5 * m) // 2
    y0 = (size - 3 * m) // 2
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = img.load()
    rects = [(x0, y0, 5 * m, m)] + [(x0 + i * 2 * m, y0 + 2 * m, m, m) for i in range(3)]
    for rx, ry, rw, rh in rects:
        for y in range(ry, ry + rh):
            for x in range(rx, rx + rw):
                px[x, y] = INK
    ink = sum(1 for y in range(size) for x in range(size) if px[x, y][3] != 0)
    expected = 8 * m * m
    if ink != expected:
        die(f"{size}px: {ink} píxeles de tinta, esperaba 8m² = {expected}")
    print(f"  {size}px: m={m} · tinta {ink}px = 8m² ✓")
    return img


def main() -> None:
    imgs = {s: render(s) for s in SIZES}
    for s, img in imgs.items():
        out = SITE / f"favicon-{s}.png"
        img.save(out)
        if out.stat().st_size == 0:
            die(f"{out.name} quedó vacío")
    imgs[48].save(SITE / "favicon.ico",
                  sizes=[(s, s) for s in SIZES],
                  append_images=[imgs[16], imgs[32]])
    if (SITE / "favicon.ico").stat().st_size == 0:
        die("favicon.ico quedó vacío")
    print(f"  emitidos en site/: favicon-16/32/48.png + favicon.ico")


if __name__ == "__main__":
    main()
