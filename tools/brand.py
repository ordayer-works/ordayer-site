"""Builds the Ordayer logo files.

The logo is the word ORDAYER in Bodoni Moda capitals, spaced wide, with one difference: its O is an
ensō, the circle a calligrapher paints in a single stroke (tools/enso.py draws it). A classical
word with one letter painted by hand: order, made by a person.

python tools/brand.py final    writes the logo set into assets/ and favicon.svg
"""

import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

import enso

ROOT = Path(__file__).resolve().parent.parent
BODONI = ROOT / "fonts" / "bodoni-moda-latin.woff2"

INK = "#16121a"
PAPER = "#f6f4f1"
CRIMSON = "#a3162b"

WORD = dict(wght=500, opsz=28, tracking=0.26)


def letters(text: str, wght: float, opsz: float, tracking: float):
    font = instantiateVariableFont(TTFont(BODONI), {"wght": wght, "opsz": opsz}, inplace=False)
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font["head"].unitsPerEm
    cap = font["OS/2"].sCapHeight
    x = 0.0
    paths = []
    for ch in text:
        g = gs[cmap[ord(ch)]]
        pen = SVGPathPen(gs)
        g.draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
        paths.append(pen.getCommands())
        x += g.width + tracking * upm
    return paths, x - tracking * upm, cap, upm


def lockup_parts(word_paint="currentColor", enso_paint=CRIMSON, wght=500, opsz=28, tracking=0.26):
    """The ensō as the O, then RDAYER. Returns the viewBox and the inner SVG."""
    paths, width, cap, upm = letters("RDAYER", wght, opsz, tracking)
    o = cap * 1.24  # a painted circle reads as an O a little larger than the capitals
    k = o / 100 / 0.82  # the ensō spans about 82 of its 100 unit box
    left = -9 * k  # trim the box's empty margin on the left
    top = -cap / 2 - 50 * k
    word_x = o + tracking * upm * 0.9
    inner = (
        f'<g transform="translate({left:.2f} {top:.2f}) scale({k:.5f})"><path d="{enso.outline()}" fill="{enso_paint}"/></g>'
        f'<path transform="translate({word_x:.2f} 0)" d="{" ".join(paths)}" fill="{word_paint}"/>'
    )
    height = 100 * k
    return f"0 {top:.0f} {word_x + width:.0f} {height:.0f}", inner


def lockup_svg(word_paint="currentColor", enso_paint=CRIMSON) -> str:
    vb, inner = lockup_parts(word_paint, enso_paint, **WORD)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="Ordayer">{inner}</svg>'


def final():
    assets = ROOT / "assets"
    (assets / "logo.svg").write_text(lockup_svg("currentColor", "currentColor"), encoding="utf-8")
    (assets / "logo-dark.svg").write_text(lockup_svg(INK, CRIMSON), encoding="utf-8")
    (assets / "logo-light.svg").write_text(lockup_svg(PAPER, "#e2475c"), encoding="utf-8")
    paths, width, cap, _ = letters("ORDAYER", **WORD)
    (assets / "wordmark.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {-cap:.0f} {width:.0f} {cap:.0f}" role="img" aria-label="Ordayer"><path d="{" ".join(paths)}" fill="currentColor"/></svg>',
        encoding="utf-8",
    )
    # The favicon: the crimson ensō on a paper tile, so it reads on light and dark tabs alike.
    (ROOT / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        f'<rect width="100" height="100" rx="24" fill="{PAPER}"/>'
        f'<g transform="translate(9 9) scale(0.82)"><path d="{enso.outline(taper_end=0.4)}" fill="{CRIMSON}"/></g></svg>',
        encoding="utf-8",
    )
    print("final written")


if __name__ == "__main__":
    {"final": final}[sys.argv[1]]()
