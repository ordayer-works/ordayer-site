"""Writes index.html and 404.html.

The logo comes from tools/brand.py (the ensō as the O of ORDAYER) and is inlined in the header and
footer. The hero shows the ensō painting from tools/enso.py. Run after changing the brand or the
words below: python tools/build_pages.py
"""

from pathlib import Path

import brand

ROOT = Path(__file__).resolve().parent.parent

_vb, _inner = brand.lockup_parts("currentColor", "var(--color-accent)", **brand.WORD)
_, _top, _w, _h = _vb.split()
LOGO = f'<svg class="logo__art" viewBox="{_vb}" aria-hidden="true" focusable="false">{_inner}</svg>'

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="Ordayer builds software and AI for tangled, difficult problems, and quietly puts them in order, so the people we serve feel looked after.">
<meta name="theme-color" content="#f6f4f1">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/bodoni-moda-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/jost-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/tokens.css">
<link rel="stylesheet" href="/css/site.css">
{extra}
</head>"""

INDEX_EXTRA = """<link rel="canonical" href="https://ordayer.com/">
<link rel="preload" href="/assets/enso.webp" as="image" type="image/webp">
<meta property="og:type" content="website">
<meta property="og:url" content="https://ordayer.com/">
<meta property="og:site_name" content="Ordayer">
<meta property="og:title" content="Ordayer">
<meta property="og:description" content="Everything in its place. We quietly put hard problems in order, so the people we serve feel looked after.">
<meta property="og:image" content="https://ordayer.com/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="A crimson ensō, a circle painted in one brush stroke, beside the Ordayer wordmark.">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"Ordayer","url":"https://ordayer.com/","logo":"https://ordayer.com/apple-touch-icon.png","email":"contact@ordayer.com","description":"Ordayer builds software and AI for tangled, difficult problems, and quietly puts them in order."}</script>"""

HEADER = f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="shell site-header__inner">
    <a class="logo" href="/" aria-label="Ordayer home">{LOGO}</a>
    <nav class="nav" aria-label="Main">
      <a href="/#careers">Careers</a>
      <a href="/#contact">Contact</a>
    </nav>
  </div>
</header>"""

FOOTER = f"""<footer class="site-footer">
  <div class="shell site-footer__inner">
    <a class="logo" href="/" aria-label="Ordayer home">{LOGO}</a>
    <p>&copy; 2026 Ordayer. Made with care.</p>
  </div>
</footer>"""

INDEX_BODY = f"""
<body>
{HEADER}
<main id="main">
  <section class="hero">
    <div class="shell grid hero__inner">
      <div class="hero__copy">
        <h1 class="hero__title">Everything in its place.</h1>
        <p class="hero__lead">Ordayer builds software and AI for tangled, difficult problems, and quietly puts them in order, so the people we serve feel looked after.</p>
        <div class="hero__actions">
          <a class="button" href="mailto:contact@ordayer.com">Say hello</a>
          <a class="text-link" href="#careers">Build with us</a>
        </div>
      </div>
      <figure class="hero__figure">
        <img class="artwork" src="/assets/enso.webp" width="1800" height="1800" alt="A crimson ensō: a circle painted in a single brush stroke, heavy where the brush lands and dry where it lifts.">
      </figure>
    </div>
  </section>

  <section class="section" aria-label="What order means to us">
    <div class="shell grid">
      <p class="statement">Not the cold, rigid kind of order. The warm kind you feel when everything is where it should be, and you can finally breathe.</p>
    </div>
  </section>

  <section class="section" aria-label="Careers and contact">
    <div class="shell grid reach">
      <div class="reach__item" id="careers">
        <h2 class="reach__title">Come build with us.</h2>
        <p class="reach__body">We are looking for people who care about the small details and the big picture alike, and who would rather do something well than do it fast. If that sounds like you, we would love to hear from you, and to see something you are proud of.</p>
        <a class="reach__address" href="mailto:careers@ordayer.com?subject=Building%20with%20Ordayer">careers@ordayer.com</a>
      </div>
      <div class="reach__item" id="contact">
        <h2 class="reach__title">Say hello.</h2>
        <p class="reach__body">A question, an idea, or a problem that needs untangling: write to us. A real person reads every message.</p>
        <a class="reach__address" href="mailto:contact@ordayer.com">contact@ordayer.com</a>
      </div>
    </div>
  </section>
</main>
{FOOTER}
</body>
</html>
"""

NOT_FOUND_BODY = f"""
<body>
{HEADER}
<main id="main">
  <section class="hero">
    <div class="shell grid hero__inner">
      <div class="hero__copy">
        <h1 class="hero__title">Nothing here, yet.</h1>
        <p class="hero__lead">The page you were looking for is not in its place. It may have moved, or the address may have a small typo.</p>
        <div class="hero__actions"><a class="button" href="/">Back to the home page</a></div>
      </div>
    </div>
  </section>
</main>
{FOOTER}
</body>
</html>
"""


def write(name: str, text: str) -> None:
    (ROOT / name).write_text(text, encoding="utf-8", newline="\n")


write("index.html", HEAD.format(title="Ordayer", extra=INDEX_EXTRA) + INDEX_BODY)
write("404.html", HEAD.format(title="Page not found | Ordayer", extra='<meta name="robots" content="noindex">') + NOT_FOUND_BODY)
write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: https://ordayer.com/sitemap.xml\n")
write(
    "sitemap.xml",
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    "  <url><loc>https://ordayer.com/</loc></url>\n</urlset>\n",
)
write("CNAME", "ordayer.com\n")
print("pages written")
