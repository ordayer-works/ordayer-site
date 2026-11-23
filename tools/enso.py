"""Paints the Ordayer ensō and draws its vector forms.

An ensō is the circle a calligrapher paints in a single breath with one stroke of the brush. Ours is
the O of ORDAYER: order, drawn by hand rather than by ruler.

The painting is made bristle by bristle. Each bristle carries its own ink and runs dry along the
stroke, so the circle starts in a heavy, wet press and ends in dry streaks, the way a real brush
does. It renders at twice its size and is scaled down for clean edges.

python tools/enso.py paint   writes assets/enso.webp, the painting for the page
python tools/enso.py mark    writes the vector mark used in the logo and favicon
"""

import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent

MAROON = (92, 15, 30)
CRIMSON = (163, 22, 43)
RED = (194, 34, 58)

START = math.radians(328)  # where the brush lands, at about two o'clock
SWEEP = math.radians(326)  # all the way round, stopping a breath short of where it began


def centre_line(s: float, size: float, seed: float = 0.0):
    """A point on the stroke's path at s from 0 to 1, with the slight wander of a hand."""
    a = START + s * SWEEP
    r = size * 0.36 * (1 + 0.022 * math.sin(2 * math.pi * s * 1.3 + 0.7 + seed) + 0.012 * math.sin(2 * math.pi * s * 3.1))
    cx = size / 2 + size * 0.008 * math.sin(2 * math.pi * s)
    cy = size / 2 + size * 0.006 * math.cos(2 * math.pi * s * 0.8)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def width_at(s: float) -> float:
    """The brush's width along the stroke: a quick, heavy press, a full body, then a thinning tail."""
    press = 1 + 0.14 * max(0.0, 1 - s / 0.07)  # the brush lands swollen, then settles
    tail = 1.0 if s < 0.6 else max(0.3, 1 - ((s - 0.6) / 0.4) ** 1.5 * 0.7)
    swell = 1 + 0.06 * math.sin(2 * math.pi * s * 2.2)
    return press * tail * swell


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def paint(size=1800, scale=2, seed=7):
    rng = random.Random(seed)
    big = size * scale
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    brush = big * 0.1  # the full width of the brush at its widest
    bristles = 260
    steps = 1100

    for b in range(bristles):
        u = (b + rng.random()) / bristles - 0.5  # across the brush, from one edge to the other
        edge = abs(u) * 2
        ink = 1.45 - edge * 0.5 + rng.uniform(-0.1, 0.1)
        dry = 0.9 + edge * 1.1 + rng.uniform(0, 0.5)  # how fast this bristle runs out
        colour = mix(MAROON, CRIMSON, rng.random() * 0.8 + (1 - edge) * 0.2)
        if rng.random() < 0.08:
            colour = mix(colour, RED, 0.5)
        thick = max(1, int(brush / bristles * 3.4 * (1 - edge * 0.25)))
        gap_phase = rng.uniform(0, 100)
        # Edge bristles touch the paper a moment after the centre, which rounds the stroke's start.
        lands = 0.018 * (1 - math.sqrt(max(0.0, 1 - edge * edge)))
        prev = None
        for i in range(steps + 1):
            s = i / steps
            x, y = centre_line(s, big)
            nx, ny = centre_line(min(1, s + 1e-3), big)
            dx, dy = nx - x, ny - y
            n = math.hypot(dx, dy) or 1
            px, py = -dy / n, dx / n
            w = width_at(s) * brush
            off = u * w
            point = (x + px * off, y + py * off)
            left = ink - dry * s ** 2.2
            # Dry streaks: as ink runs low, the bristle skips in short broken runs.
            flicker = math.sin(gap_phase + s * 140 * (1 + edge)) * 0.5 + 0.5
            alpha = left - (0.0 if left > 0.45 else flicker * (0.45 - left) * 2.2)
            if s < lands:
                continue
            if prev is not None and alpha > 0.04:
                a = int(255 * min(1.0, alpha) * 0.92)
                draw.line([prev, point], fill=(*colour, a), width=thick)
            prev = point

    # A whisper of ink bleeding into the paper, then down to size for clean edges.
    bleed = img.filter(ImageFilter.GaussianBlur(scale * 1.4))
    bleed.putalpha(bleed.getchannel("A").point(lambda v: v * 0.45))
    img = Image.alpha_composite(bleed, img)
    img = img.resize((size, size), Image.LANCZOS)
    out = ROOT / "assets" / "enso.webp"
    img.save(out, "WEBP", quality=88, method=6)
    print("painted", out, out.stat().st_size)


def outline(size=100.0, taper_end=0.28):
    """The ensō as one smooth vector shape: the brush's two edges, joined at the ends."""
    samples = 240
    left, right = [], []
    brush = size * 0.11
    for i in range(samples + 1):
        s = i / samples
        x, y = centre_line(s, size)
        nx, ny = centre_line(min(1, s + 1e-3), size)
        dx, dy = nx - x, ny - y
        n = math.hypot(dx, dy) or 1
        px, py = -dy / n, dx / n
        w = width_at(s) * brush / 2
        if s > 0.92:
            w *= max(taper_end, 1 - (s - 0.92) / 0.08)
        left.append((x + px * w, y + py * w))
        right.append((x - px * w, y - py * w))
    # A rounded start, where the brush first touched the paper.
    x, y = centre_line(0, size)
    nx, ny = centre_line(1e-3, size)
    dx, dy = nx - x, ny - y
    n = math.hypot(dx, dy) or 1
    w = width_at(0) * brush / 2
    base = math.atan2(dy, dx)
    # From the right edge, round the back of the start, to the left edge where the outline began.
    cap = [(x + w * math.cos(base - math.pi / 2 - k * math.pi / 16), y + w * math.sin(base - math.pi / 2 - k * math.pi / 16)) for k in range(1, 16)]
    pts = left + right[::-1] + cap
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"


def mark():
    d = outline()
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="Ordayer"><path d="{d}" fill="#a3162b"/></svg>'
    (ROOT / "assets" / "enso-mark.svg").write_text(svg, encoding="utf-8")
    print("mark written")


if __name__ == "__main__":
    {"paint": paint, "mark": mark}[sys.argv[1]]()
