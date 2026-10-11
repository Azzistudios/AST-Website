# CLAUDE.md · Atelier Sans Titre website

Static bilingual site in `~/Desktop/AST Website`. English at the root, French generated into `/fr/`.
Current brief: `~/My Drive/ATELIER SANS TITRE/08_Website & SEO/AST_Website_Relaunch_Brief_v01_20261010.md` (Edition 03). It replaces Edition 02 and the sub-services doc.

## Rules for every session

1. **Ask Marc before every step.** Say in one line what you are about to do, then wait for his yes.
2. **Show each step before committing.** Commit in logical steps (structure, copy, images, SEO) with clear messages.
3. **Never push without Marc's explicit yes.** The push is what makes it live. After a push, open https://ateliersanstitre.com and check the live pages match.
4. **Copy and light design only. No rebuild.** Keep the existing layout system, CSS, scripts, consent banner, GA4 and Meta Pixel. New blocks reuse existing classes wherever possible.
5. **Never caption, alt-text or label an image as AST work unless it is AST work.** No client, year, location or build time is claimed for anything that was not built. Concept renders read "Concept render, what it shows".
6. **French is generated, never hand-written.** Every English text change needs its French string in `build_fr.py` (`CATALOG` or the `ALT` map), then run `python3 build_fr.py`. Never edit `/fr/*.html` by hand.

## Identity

- Type: Syne only (400/500/600/700).
- Ink #000 · Near-black #111 · Graphite #555 · Grey #8A8A8A · Muted #BDBDBD · Mist #E0E0E0 · Paper #FFF.
- Muted palette as fills only (blocks, pills), never type on its own: Oxblood #6E1F26, Ochre #C28B2C, Olive #676A3B, Slate #4B5B73, Blush #E4BEB3.
- Wordmark black on white or white on black only.
- The studio is "Atelier Sans Titre", never "AST Studios".

## Voice

Short declaratives. Nouns over adjectives. Design first in every sentence.
Never in visible copy: luxury or luxurious (meta tags only), dream, magical, stunning, unforgettable, elegant, timeless, bespoke, curated, elevate, immersive (except the service name "immersive installations"), seamless, stress-free, journey, story, special day, event decor, turnkey, we do it all, "wedding planner" as the identity, "designed to be remembered", "singular moment", "intention", emoji, exclamation marks, dashes in body copy (use a full stop or a colon).

## Site map

```
index.html            Home: hero, statement, the two doors, Concepts, Lebanon, Instagram, CTA
private.html          Private hub: weddings and private events
  weddings.html       Weddings
brands.html           Brands hub: fashion shows, brand and corporate events, galas
  fashion-shows.html       Fashion shows
  brand-experiences.html   Brand and corporate events (URL kept for search)
work.html             Concepts
  the-long-table · the-vernissage · after-dark · the-couture-salon
  hall-of-images · silhouettes · three-rooms              (Concept pages)
about.html · faq.html · contact.html · privacy.html · terms.html · 404.html
special-events.html → private.html
disciplines.html    → index.html#sides
project.html        → work.html                           (redirect stubs, noindex)
```

Nav: Private · Brands · About · Contact. FR: Privé · Marques · À propos · Contact. Concepts and FAQ sit in the footer; Concepts is also reached from the home mosaic and the Private and Brands pages.

## Working locally

- Serve with `python3 serve.py` at http://localhost:3000. Never open a `file://` URL.
- Before asking for the push: every page EN and FR, desktop and 375 px, no console errors, no broken links.
- Node is available. Use `node --check` to validate inline scripts.
