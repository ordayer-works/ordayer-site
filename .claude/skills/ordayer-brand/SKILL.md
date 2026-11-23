---
name: ordayer-brand
description: >-
  Ordayer's look and voice: warm paper and ink, one hand-painted crimson ensō, Bodoni Moda for large
  headings only, Jost for everything people read, short warm words, and the order the eye takes down
  a page. Use it for anything that carries the Ordayer name: a new page or section on ordayer.com
  (careers, about, a policy, the 404 page), a change to the home page, the logo, the share image,
  an email, a slide, a document or a social post. Use it whenever someone asks to restyle, extend,
  redesign, review or "make it look better", even if they never say "brand".
---

# Ordayer brand

Ordayer should feel like a house that intends to last a century: calm, warm, unhurried and
precise. The page is mostly paper. One painted circle carries the art. The words are few and kind.
Everything below was chosen by eye over many rounds, and every rejected look is listed at the end
so it is not proposed again.

## Where the system lives

| File | What it holds |
| --- | --- |
| `css/tokens.css` | Every value: primitives (paper, ink, crimson, type and space scales), then semantic tokens (ground, text, accent). Components read semantic tokens only |
| `css/site.css` | Layout and components |
| `tools/build_pages.py` | The pages and every word on them. Edit here, then run `python tools/build_pages.py`; never edit `index.html` by hand |
| `tools/enso.py` | Paints the ensō bristle by bristle (seeded, so it is the same every time) and draws its vector form |
| `tools/brand.py` | The logo lockup, favicon and share image, from Bodoni Moda's own outlines |

A new page reuses these. If something is missing, add a semantic token or a component to them
rather than styling one page on its own, so the next page matches without effort.

## Colour

Paper (`--color-ground`) and ink (`--color-text`) do nearly all the work. Crimson is used the way a
painter uses one colour: the ensō, the O of the logo, link underlines, focus rings and text
selection, and nothing else. There is no second accent, no gradient and no dark band.

Body text stays dark. "Muted" text is one step below ink (`ink-700`), never grey: lighter or thinner
text was found hard to read on the careers and contact sections and was changed.

## Type

- **Bodoni Moda only at heading size,** about 28px and up: the hero headline, section headings and
  one large statement. Its hairlines vanish at small sizes; the font's optical-size axis thickens
  them a little, but not enough for small text.
- **Jost for everything people read:** body at 18px, weight 400; small headings (such as a list of
  values), email addresses, links and labels at weight 500.
- One family per job. No italics for emphasis in body text; no all-caps labels above headings.

## Where the eye goes

On every screen, one thing wins, then a clear second and third. On the home page: the ensō, then
"Everything in its place.", then "Say hello". Check by blurring the page to 12px
(`document.body.style.filter = "blur(12px)"`): exactly one shape should still win. When two compete,
quiet the loser; never make the winner louder.

- **Desktop:** the words on the left, the painting on the right, the painting a little heavier.
- **Phone:** one centred poster, in the order the eye should take it: painting, headline, a short
  line, then the actions. All of it fits the first screen of a 390x844 phone.
- Check at 390px, 1440px and 1536x808 (a laptop window, where a tall hero hides everything else).

## Layout

A 12-column grid inside `.shell`, generous space, and one gap between sections (`--gap-section`),
with a hairline between neighbouring sections. No cards, boxes, shadows or rounded panels; no
captions under art; nothing that exists only to fill space. A section earns its place by saying
something a visitor would miss if it were gone.

## Words

Kind, gentle and clear, in short sentences. Say what we do for people, never what we do not do
wrong, and never defend ourselves. The voice the founders like best:

> Not the cold, rigid kind of order. The warm kind you feel when everything is where it should be,
> and you can finally breathe.

- Plain words over clever ones. A visitor should understand every line on first reading.
- No filler: no etymology lessons, no stock lines such as "We bring order to complexity".
- No em or en dashes anywhere.
- Contact is contact@ordayer.com; careers is careers@ordayer.com with the subject "Building with Ordayer".

## Motion

One moment only: the hero's ensō paints itself once, in a single sweep, as the page opens (a CSS
mask, no script). Nothing else moves on its own. Under "reduce motion" the finished painting shows
at once. Hover and focus answer the pointer quietly: an email's underline thickens, a button's ink softens a shade.

## Looks we turned down

Do not propose these again; each was tried and rejected.

- Flat navy with a dotted lattice: boring.
- A squared circle like a dial: not fun, a bland page.
- A gold tangram on oxblood: the gold felt uninteresting and the set "weird".
- Animated generative backgrounds, "like a 2008 live wallpaper".
- Ink marks that gather into the ensō as the page loads: the hero sat empty, and it is the old
  "particles form a logo" trick.
- Flowing ink lines in a band that move with scroll and the pointer: they read as stray hairs, and
  as scratches on a phone.
- A 3D-lit ensō (Three.js): a change nobody would notice, for a large download.
- A dark maroon band with the word "ordo" and its Latin meaning: filler.
- A caption under the painting.
- Four company values under "What we believe": generic lines any company could sign, and the
  warm statement already says what we care about. The home page is the hero, that statement, what we
  make (each product's name, one plain line and its link), then careers and contact.
- Light or thin body text, and Bodoni at small sizes: hard to read.

## Checking a change

On the laptop this is built on, every browser run goes through `C:\swt\run-light.ps1` (it
bluescreens when memory runs short). Take screenshots at the three sizes, sharp and blurred, read
the phone page top to bottom at full size, and fix the three biggest gaps before looking again.
