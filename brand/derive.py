#!/usr/bin/env python3
"""
derive.py — la derivación de la marca Reasoned Web, computada.

Regla (decidida 2026-08-13, cuatro especímenes; ver CLAUDE.md § IDENTIDAD):
NINGÚN VALOR SE ELIGE DONDE UNO SE PUEDE DERIVAR.

  · Máster apilado: REASONED arriba, WEB abajo, MISMA medida (por avances,
    semántica de letter-spacing CSS: espacio tras cada letra, el de la última
    se recorta).
      W₁  = ancho conformado de REASONED (kerning real) + 7 × track₁
      track₁ = 0.02 em  (regla fijada para la línea 1)
      W₂  = ancho conformado de WEB (kerning real)
      gap = (W₁ − W₂) / 2   ← el tracking de WEB NO se elige
    Canal vertical entre líneas = gap: el mismo número gobierna ambos ejes.
  · Lockup horizontal: glifo (5m × 3m) con 3m = altura de mayúsculas del
    texto → m = capHeight / 3; separación glifo→texto = m (el módulo sigue).
    Tracking del texto −0.015 em: el ÚNICO valor óptico, declarado como tal.

La fuente es la entrada, no una constante: al cambiar de fuente se re-corre
esto y los másters se re-emiten. La regla es el logo; el render es su output.

Corre:  python brand/derive.py   (desde la raíz del repo o desde brand/)
Emite:  brand/derivation.json, brand/wordmark-stacked.svg, brand/lockup.svg
"""
import json
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.misc.transform import Transform

BRAND = Path(__file__).resolve().parent
FONT_PATH = BRAND / "fonts" / "Switzer-Bold.otf"

LINE1, LINE2 = "REASONED", "WEB"
TRACK1_EM = 0.02      # regla: tracking de la línea 1
LOCKUP_TEXT = "Reasoned Web"
LOCKUP_TRACK_EM = -0.015  # ÚNICO valor óptico de la identidad (se afina a ojo)


def die(msg: str) -> None:
    print(f"⛔ derive.py: {msg}", file=sys.stderr)
    sys.exit(1)


def shape(hb_font: "hb.Font", text: str, tracking: float):
    """Conforma `text` (kerning GPOS real) y devuelve (posiciones_x, ancho).

    `tracking` en unidades de fuente, añadido tras CADA glifo; el sobrante del
    último se recorta (semántica de letter-spacing CSS con margin-right
    negativo). VERDE EN VACÍO: cero glifos = error, no un ancho 0 silencioso.
    """
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hb_font, buf, {"kern": True, "liga": False})
    infos, positions = buf.glyph_infos, buf.glyph_positions
    if not infos:
        die(f"0 glifos conformados para {text!r} — no hay nada que medir "
            "(¿texto vacío o fuente sin esos glifos?)")
    xs, x = [], 0.0
    for info, pos in zip(infos, positions):
        xs.append((info.codepoint, x + pos.x_offset))
        x += pos.x_advance + tracking
    x -= tracking  # el espacio tras el último glifo se recorta
    return xs, x


def notdef_check(font: TTFont, hb_font: "hb.Font", text: str) -> None:
    """Un .notdef conformado mediría 'bien' y mentiría: se corta aquí."""
    for ch in text:
        if ch == " ":
            continue
        if hb_font.get_nominal_glyph(ord(ch)) is None:
            die(f"la fuente no tiene glifo para {ch!r} — el ancho sería mentira")


def paths_and_bbox(font: TTFont, placed, baseline_y: float):
    """SVG paths de glifos colocados (y-flip a coordenadas SVG) + bbox tinta."""
    glyph_set = font.getGlyphSet()
    glyph_order = font.getGlyphOrder()
    d_parts, bbox = [], [None]
    for gid, x in placed:
        name = glyph_order[gid]
        glyph = glyph_set[name]
        t = Transform(1, 0, 0, -1, x, baseline_y)
        spen = SVGPathPen(glyph_set)
        glyph.draw(TransformPen(spen, t))
        d = spen.getCommands()
        if d:
            d_parts.append(d)
        bpen = BoundsPen(glyph_set)
        glyph.draw(TransformPen(bpen, t))
        if bpen.bounds:
            x0, y0, x1, y1 = bpen.bounds
            if bbox[0] is None:
                bbox[0] = [x0, y0, x1, y1]
            else:
                b = bbox[0]
                b[0], b[1] = min(b[0], x0), min(b[1], y0)
                b[2], b[3] = max(b[2], x1), max(b[3], y1)
    if not d_parts or bbox[0] is None:
        die("0 contornos extraídos — glifos vacíos o extracción rota")
    return " ".join(d_parts), bbox[0]


def fmt(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".")


def svg(view_box, content, comment):
    x, y, w, h = view_box
    return (
        f"<!--\n{comment}\n-->\n"
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{fmt(x)} {fmt(y)} {fmt(w)} {fmt(h)}">\n'
        f"{content}\n</svg>\n"
    )


def main() -> None:
    if not FONT_PATH.exists():
        die(f"no encuentro la fuente en {FONT_PATH} — la medida ES la entrada")
    font = TTFont(str(FONT_PATH))
    upm = font["head"].unitsPerEm
    cap = font["OS/2"].sCapHeight
    if not cap or cap <= 0:
        die("la fuente no declara sCapHeight — sin capa de mayúsculas no hay "
            "derivación vertical honesta")

    blob = hb.Blob.from_file_path(str(FONT_PATH))
    hb_font = hb.Font(hb.Face(blob))

    for text in (LINE1, LINE2, LOCKUP_TEXT):
        notdef_check(font, hb_font, text)

    # ── Máster apilado ────────────────────────────────────────────────────
    track1 = TRACK1_EM * upm
    placed1, w1 = shape(hb_font, LINE1, track1)
    _, w2_raw = shape(hb_font, LINE2, 0.0)
    if w2_raw >= w1:
        die(f"WEB ({fmt(w2_raw)}u) no es más angosta que REASONED "
            f"({fmt(w1)}u) — la derivación del gap no aplica a esta fuente")
    gap = (w1 - w2_raw) / 2.0
    placed2, w2 = shape(hb_font, LINE2, gap)
    if abs(w2 - w1) > 1e-6:
        die(f"justificación rota: línea 1 = {w1!r}u, línea 2 = {w2!r}u")

    baseline1 = float(cap)
    baseline2 = cap + gap + cap  # canal vertical = gap, el mismo número
    d1, bb1 = paths_and_bbox(font, placed1, baseline1)
    d2, bb2 = paths_and_bbox(font, placed2, baseline2)
    bbox = [min(bb1[0], bb2[0]), min(bb1[1], bb2[1]),
            max(bb1[2], bb2[2]), max(bb1[3], bb2[3])]
    comment = (
        f"  Máster apilado Reasoned Web — GENERADO por brand/derive.py; no se edita a mano.\n"
        f"  Fuente: Switzer Bold (upm {upm}, capHeight {cap}).\n"
        f"  W1 = shaped(REASONED) + 7 × {fmt(track1)}u (0.02em) = {fmt(w1)}u\n"
        f"  W2 = shaped(WEB) = {fmt(w2_raw)}u\n"
        f"  gap = (W1 − W2) / 2 = {fmt(gap)}u = {gap/upm:.4f}em  ← no elegido: derivado\n"
        f"  canal vertical entre líneas = gap = {fmt(gap)}u (un número, dos ejes).\n"
        f"  viewBox = bbox de tinta MEDIDO, no elegido."
    )
    stacked = svg(
        (bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]),
        f'<path fill="currentColor" d="{d1} {d2}"/>',
        comment,
    )

    # ── Lockup horizontal ────────────────────────────────────────────────
    m = cap / 3.0            # 3m = capHeight → el glifo mide exactamente capa
    mark_w = 5.0 * m
    text_x0 = mark_w + m     # separación glifo→texto = m: el módulo sigue
    track_l = LOCKUP_TRACK_EM * upm
    placed_l, w_l = shape(hb_font, LOCKUP_TEXT, track_l)
    placed_l = [(g, x + text_x0) for g, x in placed_l]
    d_l, bb_l = paths_and_bbox(font, placed_l, float(cap))
    # marca: barra 5m×m arriba, canal m, tres cuadrados m×m en la línea base
    rects = [(0.0, 0.0, mark_w, m)] + [(i * 2.0 * m, 2.0 * m, m, m) for i in range(3)]
    rects_svg = "\n".join(
        f'<rect fill="currentColor" x="{fmt(x)}" y="{fmt(y)}" '
        f'width="{fmt(w)}" height="{fmt(h)}"/>' for x, y, w, h in rects
    )
    lb = [min(0.0, bb_l[0]), min(0.0, bb_l[1]),
          max(mark_w, bb_l[2]), max(float(cap), bb_l[3])]
    comment_l = (
        f"  Lockup horizontal Reasoned Web — GENERADO por brand/derive.py; no se edita a mano.\n"
        f"  m = capHeight / 3 = {fmt(m)}u → glifo 5m × 3m = altura de mayúsculas exacta.\n"
        f"  separación glifo→texto = m = {fmt(m)}u (el módulo sigue).\n"
        f"  tracking del texto = −0.015em = {fmt(track_l)}u — ÚNICO valor óptico de la identidad."
    )
    lockup = svg(
        (lb[0], lb[1], lb[2] - lb[0], lb[3] - lb[1]),
        f"{rects_svg}\n" f'<path fill="currentColor" d="{d_l}"/>',
        comment_l,
    )

    derivation = {
        "_": "Números CONGELADOS de la identidad. Se re-derivan corriendo brand/derive.py; no se editan a mano.",
        "font": {"family": "Switzer", "weight": 700, "file": "fonts/Switzer-Bold.otf",
                 "unitsPerEm": upm, "capHeight": cap, "license": "ITF Free Font License (fonts/FFL.txt)"},
        "stacked": {
            "rule": "gap = (W1 − W2) / 2; canal vertical entre líneas = gap",
            "track1_em": TRACK1_EM,
            "track1_units": track1,
            "W1_units": w1,
            "W2_raw_units": w2_raw,
            "gap_units": gap,
            "gap_em": gap / upm,
            "line_widths_equal": True,
        },
        "lockup": {
            "rule": "m = capHeight/3; glifo 5m×3m a línea base; separación = m",
            "m_units": m,
            "mark_width_units": mark_w,
            "text_gap_units": m,
            "tracking_em": LOCKUP_TRACK_EM,
            "tracking_units": track_l,
            "tracking_note": "único valor óptico; se afina a ojo",
            "text_width_units": w_l,
        },
        "glyph": {
            "rule": "módulo m; medida 5m; viewBox 100: barra x20 y32 60×12; cuadrados 12×12 y56, x 20/44/68",
            "favicon_grid": "m_px = round(size × 12/100): 16px→2, 32px→4, 48px→6 (rejilla entera, sin antialias)",
        },
    }

    (BRAND / "derivation.json").write_text(
        json.dumps(derivation, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8", newline="\n")
    (BRAND / "wordmark-stacked.svg").write_text(stacked, encoding="utf-8", newline="\n")
    (BRAND / "lockup.svg").write_text(lockup, encoding="utf-8", newline="\n")

    print("derive.py — derivación completada")
    print(f"  upm {upm} · capHeight {cap}")
    print(f"  W1(REASONED+track) = {fmt(w1)}u · W2(WEB) = {fmt(w2_raw)}u")
    print(f"  gap = {fmt(gap)}u = {gap/upm:.4f}em   (líneas justificadas: ✓)")
    print(f"  lockup: m = {fmt(m)}u · texto en x={fmt(text_x0)}u · tracking {fmt(track_l)}u")
    print("  emitidos: derivation.json, wordmark-stacked.svg, lockup.svg")


if __name__ == "__main__":
    main()
