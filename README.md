# ordayer.com

The Ordayer website: one static page, served by GitHub Pages from this repo's `main` branch. No build step: what is in the repo is what is served.

## The brand in one minute

- **The name** comes from *ordo*, Latin for order: the warm kind you feel when everything is where it should be.
- **The logo** is ORDAYER in spaced Bodoni Moda capitals, with one letter painted by hand: its O is an ensō, the circle a calligrapher paints in a single stroke. Order, made by a person.
- **The palette:** warm paper and ink, with crimson used as a painter would use one colour, rarely and with intent. A maroon band gives the page its heartbeat.
- **The type:** Bodoni Moda for headings and the wordmark, Jost (an open Futura) for everything read at length.
- **The voice** is kind, gentle and clear, with a little quiet mystery. Say what we do for people, never what we do not do wrong.
- **The one moment of motion:** the hero's ensō paints itself once, in a single sweep, as the page opens. People who prefer less motion see the finished painting.

## Files

| Path | What it is |
| --- | --- |
| `index.html`, `404.html` | The pages, written by `tools/build_pages.py` |
| `css/tokens.css` | Every design value, in two layers: primitives (raw values) and semantic tokens (jobs such as ground, text, accent). Change the look here |
| `css/site.css` | Layout and components. Reads semantic tokens only, never a raw value |
| `assets/enso.webp` | The ensō painting in the hero, painted by `tools/enso.py` |
| `assets/enso-mark.svg` | The ensō alone as a clean vector, for small sizes |
| `assets/logo.svg` | The logo in `currentColor`, for one colour use |
| `assets/logo-dark.svg`, `assets/logo-light.svg` | The full colour logo for light and dark grounds: documents, slides, other sites |
| `assets/wordmark.svg` | ORDAYER in Bodoni alone |
| `assets/og.png` | The image shown when the site is shared |
| `favicon.svg`, `favicon.ico`, `apple-touch-icon.png` | Browser and home screen icons |
| `fonts/` | Bodoni Moda and Jost, self-hosted, with their licences (SIL Open Font License 1.1) |
| `tools/enso.py` | Paints the ensō bristle by bristle, and draws its vector form |
| `tools/brand.py` | Builds the logo files from Bodoni Moda's own outlines and the ensō |

## Changing things

- **Words on the page:** edit the text in `tools/build_pages.py`, then run `python tools/build_pages.py` from this folder.
- **A colour, a size or spacing:** change the semantic token in `css/tokens.css`. Add a primitive only when no existing one fits.
- **The logo or the painting:** change `tools/enso.py` or `tools/brand.py`, run `python tools/enso.py paint`, `python tools/enso.py mark` and `python tools/brand.py final` from `tools/`, then rebuild the pages.
- **Preview:** `python -m http.server 8765` in this folder, then open `http://127.0.0.1:8765/`.

## Email

Contact goes to contact@ordayer.com and careers to careers@ordayer.com, both into the company's shared mailbox.
