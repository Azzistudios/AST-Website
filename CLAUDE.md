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
work.html             Work: Built (Red Room band) then a Concepts grid; footer label 'Work'
  red-room.html  Built: a private dinner hosted by Marc Azzi (photographs, indexed)
  the-long-table · after-dark · the-couture-salon · silhouettes · three-rooms   (Concept pages, indexed)
about.html · faq.html · contact.html · privacy.html · terms.html · 404.html
special-events.html → private.html
disciplines.html    → index.html#sides
project.html        → work.html
dinner-in-red.html  → red-room.html
the-vernissage.html → red-room.html
hall-of-images.html → red-room.html                  (redirect stubs, noindex)
```

Nav: Private · Brands · About · Contact. FR: Privé · Marques · À propos · Contact. Work (built + concepts) and FAQ sit in the footer; the Concepts grid is also reached from the home mosaic and the Private and Brands pages.

## Images and SEO conventions (Oct 2026)

- Every photo in `brand_assets/` has a `.webp` beside its `.jpg`, plus `-480` and `-960` variants; hero bands also have landscape `-hero-*` / `-wide-*` crops. Markup is `<picture><source type="image/webp" srcset="…" sizes="…"><img src="x.jpg" alt="…"></picture>`. Selectors use descendant `img`, never `> img`. `build_fr.py` rewrites `src`, `srcset`, `imagesrcset` and `href` asset paths to `../`.
- Titles and metas prescribed by the brief or by Marc later are his decision. Do not rewrite them for length or keywords without asking. The FAQ's 15 questions are prescribed too.
- Every indexable page: self-canonical, en/fr/x-default hreflang, in `sitemap.xml`. Concept pages' JSON-LD is CreativeWork with creativeWorkStatus "Unbuilt concept"; Red Room is CreativeWork + ImageGallery with place, year and creator.
- Enquiries: every WhatsApp and email link except on the legal pages carries a pre-filled message by page (date, place, guests); `build_fr.py` swaps the general one in its `PREFILL` list. GA4 `generate_lead` and the Pixel `Contact` event fire on those clicks, consent-gated; from the Contact block `generate_lead` also carries `budget_band`, and the first edit there fires `enquiry_start`. `project_click` and `service_click` fire on links in the page body, not nav or footer. `build_fr.py` regenerates only index, work, about and contact: a script change must also reach the other `/fr/` pages. `/ig/` and `/fb/` are noindex redirect stubs that add UTM tags for the bio links. Contact has an enquiry block that only fills those messages; nothing is sent or stored by the site. "Now booking 2027" sits in every CTA body: change it when 2028 opens.
- Share images live in `brand_assets/og/` (1200x630 JPEG, one per page with its own picture; generic `og-image.jpg` on FAQ, legal, 404). `sitemap.xml` lists each page's images; regenerate those entries when images change. Instagram strip on Home links the three Red Room posts. `b120b4ea28d29f2956dbd5f99ddeaf2b.txt` is the IndexNow key: keep it at the root.
- Run `python3 build_fr.py` with its output visible. If the About, Contact or Work JSON-LD changes, update `json_en`/`json_fr` in the catalog, or the build stops halfway and `fr/about.html` and `fr/contact.html` go stale.

## Working locally

- Serve with `python3 serve.py` at http://localhost:3000. Never open a `file://` URL.
- Before asking for the push: every page EN and FR, desktop and 375 px, no console errors, no broken links.
- Node is available. Use `node --check` to validate inline scripts.
