#!/usr/bin/env python3
"""
build_fr.py — regenerate the French /fr/ pages from the English source pages.

Usage:
    python3 build_fr.py

The English pages at the repo root are the single source of truth for layout,
CSS, scripts, and structure. This script copies each English page, swaps in the
French text from the CATALOG below, fixes relative asset paths (../), sets the
French <title>/meta/canonical/og, and flips the EN/FR toggle — then writes the
result to /fr/<page>.

WHEN YOU EDIT THE ENGLISH PAGES:
  • Layout / CSS / script / image changes  -> just re-run this script; they
    propagate to /fr/ automatically (French is derived from the English file).
  • English *text* changes (copy, titles, alts) -> update the matching French
    string in the CATALOG (or ALT map) below, then re-run.
"""
import re, os

ROOT = os.path.dirname(os.path.abspath(__file__))
FRDIR = os.path.join(ROOT, "fr")
os.makedirs(FRDIR, exist_ok=True)
BASE = "https://ateliersanstitre.com"

# ── toggle markup (navigation between / and /fr/) ──
def en_toggle(fr_href):
    return ('    <div class="lang-toggle">\n'
            '      <span class="lang-btn active" aria-current="page">EN</span>\n'
            '      <span class="lang-sep">/</span>\n'
            f'      <a class="lang-btn" href="{fr_href}" hreflang="fr">FR</a>\n'
            '    </div>')

def fr_toggle(en_href):
    return ('    <div class="lang-toggle">\n'
            f'      <a class="lang-btn" href="{en_href}" hreflang="en">EN</a>\n'
            '      <span class="lang-sep">/</span>\n'
            '      <span class="lang-btn active" aria-current="page">FR</span>\n'
            '    </div>')

def fr_paths(s):
    s = s.replace('href="favicon.png"', 'href="../favicon.png"')
    s = s.replace('src="favicon.png"', 'src="../favicon.png"')
    s = s.replace('href="Fonts/', 'href="../Fonts/')
    s = s.replace("url('Fonts/", "url('../Fonts/")
    s = s.replace('src="brand_assets/', 'src="../brand_assets/')
    # French accessible names
    s = s.replace('aria-label="Open menu"', 'aria-label="Ouvrir le menu"')
    s = s.replace('aria-label="Main"', 'aria-label="Principale"')
    s = s.replace('aria-label="Featured work"', 'aria-label="Projet à la une"')
    return s

def translate(html, fr_map, literals, group_desc=None):
    for en, fr in literals:
        assert en in html, f"literal not found: {en[:50]!r}"
        html = html.replace(en, fr)
    if group_desc:
        en, fr = group_desc
        assert en in html, "group-desc not found"
        html = html.replace(en, fr)
    for key, fr in fr_map.items():
        pat = r'<(\w+)([^>]*\bdata-i18n="' + re.escape(key) + r'"[^>]*)>(.*?)</\1>'
        html, n = re.subn(pat, lambda m: f'<{m.group(1)}{m.group(2)}>{fr}</{m.group(1)}>', html, flags=re.S)
        if n == 0:
            print(f"  ! translation key absent (skipped): {key}")
    return html

# ── French alt-text for images (same set across pages) ──
ALT = {
 "Scenography and event production by Atelier Sans Titre, Beirut":"Scénographie et production événementielle par Atelier Sans Titre, Beyrouth",
 "Fashion show scenography by Atelier Sans Titre, Beirut":"Scénographie de défilé de mode par Atelier Sans Titre, Beyrouth",
 "Runway set design for a fashion show, Beirut":"Décor de podium pour un défilé de mode, Beyrouth",
 "Fashion show staging and lighting by Atelier Sans Titre, Beirut":"Mise en scène et éclairage de défilé par Atelier Sans Titre, Beyrouth",
 "Brand experience installation for a product launch, Beirut":"Installation d'expérience de marque pour un lancement de produit, Beyrouth",
 "Immersive brand activation by Atelier Sans Titre, Beirut":"Activation de marque immersive par Atelier Sans Titre, Beyrouth",
 "Brand experience scenography by Atelier Sans Titre, Beirut":"Scénographie d'expérience de marque par Atelier Sans Titre, Beyrouth",
 "Special event production by Atelier Sans Titre, Beirut":"Production d'événement spécial par Atelier Sans Titre, Beyrouth",
 "Gala dinner scenography in Beirut":"Scénographie de dîner de gala à Beyrouth",
 "Cultural event staging by Atelier Sans Titre, Beirut":"Mise en scène d'événement culturel par Atelier Sans Titre, Beyrouth",
 "Gala dinner scenography by Atelier Sans Titre, part of the Azzi Studios ecosystem, Beirut":"Scénographie de dîner de gala par Atelier Sans Titre, membre de l'écosystème Azzi Studios, Beyrouth",
 "Atelier Sans Titre scenography on Instagram, Beirut":"Scénographie Atelier Sans Titre sur Instagram, Beyrouth",
 "Atelier Sans Titre event production on Instagram, Beirut":"Production événementielle Atelier Sans Titre sur Instagram, Beyrouth",
 "Atelier Sans Titre brand experience on Instagram, Beirut":"Expérience de marque Atelier Sans Titre sur Instagram, Beyrouth",
 "Atelier Sans Titre, scenography and event production studio, Beirut":"Atelier Sans Titre, studio de scénographie et de production événementielle, Beyrouth",
 "Atelier Sans Titre studio, LED wall installation, Beirut":"Studio Atelier Sans Titre, installation de mur LED, Beyrouth",
 "Home of Atelier Sans Titre in Beirut, Lebanon":"Siège d'Atelier Sans Titre à Beyrouth, Liban",
 "Atelier Sans Titre studio location, Beirut, Lebanon":"Emplacement du studio Atelier Sans Titre, Beyrouth, Liban",
 "Scenography and event production by Atelier Sans Titre in Beirut, Lebanon":"Scénographie et production événementielle par Atelier Sans Titre à Beyrouth, Liban",
}

NAV = {'nav-work':'Travail','nav-about':'À propos','nav-disciplines':'Disciplines','nav-contact':'Contact'}
TAGS = {'tag-fashion':'Mode','tag-jewellery':'Joaillerie','tag-beauty':'Beauté','tag-spirits':'Spiritueux','tag-automotive':'Automobile','tag-culture':'Culture & Arts'}
FOOT = {'footer-location':'Beyrouth, Liban','copyright':'© 2026 Atelier Sans Titre. Tous droits réservés.'}

# ── CATALOG: per-page French text + URLs ──
PAGES = {
'index.html': dict(
    en_url=f"{BASE}/", fr_url=f"{BASE}/fr/", en_canon=f"{BASE}/", fr_canon=f"{BASE}/fr/",
    en_title="Atelier Sans Titre · Scenography &amp; Event Production, Beirut",
    fr_title="Atelier Sans Titre · Scénographie &amp; production événementielle, Beyrouth",
    en_desc="Atelier Sans Titre is a Beirut scenography and event production studio. Special events, brand experiences, and fashion shows for luxury clients.",
    fr_desc="Atelier Sans Titre est un studio de scénographie et de production événementielle à Beyrouth. Événements spéciaux, expériences de marque et défilés de mode pour des clients de luxe.",
    en_toggle_href="fr/index.html", fr_toggle_href="../index.html", json_en=None, json_fr=None,
    fr_map={**NAV, **TAGS, **FOOT,
        'tagline':'Scénographie<span class="m-br"><br></span> et production<br>pour <strong>des événements spéciaux</strong>,<br><strong>des expériences de marque</strong>,<br>et des <strong>défilés de mode</strong>.',
        'work-label':'Notre Travail', 'work-desc':"Atelier Sans Titre transforme l'espace en expérience.",
        'location-sub':'Notre base. Notre perspective.',
        'location-heading':'Beyrouth<br><span class="arrow">→ Liban</span>',
        'location-body':'Basée à Beyrouth, Sans Titre crée des événements spéciaux, des expériences de marque et des défilés de mode pour des clients de luxe à travers la région et au-delà.',
        'insta-label':'Suivez-nous sur Instagram'},
    literals=[],
    group_desc=('<span class="sec-desc" style="text-align:left;" data-i18n="group-desc">Atelier Sans Titre is part of<span class="m-br"><br></span> <strong style="font-weight:700;">Azzi Studios</strong> creative ecosystem.</span>',
                '<span class="sec-desc" style="text-align:left;" data-i18n="group-desc">Atelier Sans Titre fait partie de l\'écosystème créatif <strong style="font-weight:700;">Azzi Studios</strong>.</span>'),
),
'work.html': dict(
    en_url=f"{BASE}/work.html", fr_url=f"{BASE}/fr/work.html", en_canon=f"{BASE}/work.html", fr_canon=f"{BASE}/fr/work.html",
    en_title="Special Events, Brand Experiences &amp; Fashion Shows · Work · Atelier Sans Titre",
    fr_title="Événements spéciaux, expériences de marque &amp; défilés de mode · Travail · Atelier Sans Titre",
    en_desc="Discover the special events, brand experiences, and fashion shows produced by Atelier Sans Titre, Beirut.",
    fr_desc="Découvrez les événements spéciaux, expériences de marque et défilés de mode produits par Atelier Sans Titre, Beyrouth.",
    en_toggle_href="fr/work.html", fr_toggle_href="../work.html",
    fr_map={**NAV, **TAGS, **FOOT,
        'work-h1':'Événements spéciaux, expériences de marque et défilés de mode',
        'work-hero':'Scénographie<span class="m-br"><br></span> et production<br>pour <strong>des événements spéciaux</strong>,<br><strong>des expériences de marque</strong>,<br>et des <strong>défilés de mode</strong>.',
        'disc-fashion-label':'Défilés de mode',
        'disc-fashion-desc':"Sans Titre conçoit et produit des défilés de mode qui inscrivent la vision d'un créateur dans l'espace, du premier concept au salut final. Nous travaillons avec des maisons exigeantes pour mettre en scène des moments qui définissent une saison.",
        'disc-brand-label':'Expériences de marque',
        'disc-brand-desc':'Nous construisons des expériences de marque dans lesquelles le public entre : lancements de produits, activations et installations immersives qui placent les gens au cœur du récit.',
        'disc-events-label':'Événements spéciaux',
        'disc-events-desc':"Des dîners intimes aux rassemblements culturels à grande échelle, nous produisons des événements spéciaux qui donnent à chaque espace une identité propre. Chacun est construit de zéro, conçu, produit et livré comme quelque chose qui ne pouvait arriver qu'une seule fois."},
    literals=[], group_desc=None,
    json_en='{"@context":"https://schema.org","@graph":[{"@type":"WebPage","name":"Special Events, Brand Experiences & Fashion Shows · Work · Atelier Sans Titre","url":"https://ateliersanstitre.com/work.html","isPartOf":{"@type":"WebSite","name":"Atelier Sans Titre","url":"https://ateliersanstitre.com"}},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://ateliersanstitre.com/"},{"@type":"ListItem","position":2,"name":"Work","item":"https://ateliersanstitre.com/work.html"}]}]}',
    json_fr='{"@context":"https://schema.org","@graph":[{"@type":"WebPage","name":"Événements spéciaux, expériences de marque & défilés de mode · Travail · Atelier Sans Titre","url":"https://ateliersanstitre.com/fr/work.html","inLanguage":"fr","isPartOf":{"@type":"WebSite","name":"Atelier Sans Titre","url":"https://ateliersanstitre.com"}},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":"https://ateliersanstitre.com/fr/"},{"@type":"ListItem","position":2,"name":"Travail","item":"https://ateliersanstitre.com/fr/work.html"}]}]}',
),
'about.html': dict(
    en_url=f"{BASE}/about.html", fr_url=f"{BASE}/fr/about.html", en_canon=f"{BASE}/about.html", fr_canon=f"{BASE}/fr/about.html",
    en_title="Scenography Studio in Beirut · About · Atelier Sans Titre",
    fr_title="Studio de scénographie à Beyrouth · À propos · Atelier Sans Titre",
    en_desc="A scenography and event production studio built on one conviction: that space is the most powerful medium in any event. Based in Beirut.",
    fr_desc="Un studio de scénographie et de production événementielle fondé sur une conviction : l'espace est le médium le plus puissant de tout événement. Basé à Beyrouth.",
    en_desc2="A scenography and event production studio built on one conviction: that space is the most powerful medium in any event.",
    fr_desc2="Un studio de scénographie et de production événementielle fondé sur une conviction : l'espace est le médium le plus puissant de tout événement.",
    en_toggle_href="fr/about.html", fr_toggle_href="../about.html",
    fr_map={**NAV, **FOOT,
        'about-h1':'Un studio de scénographie et de production événementielle à Beyrouth',
        'page-title':'À propos',
        'page-desc':"Un studio de scénographie et de production événementielle fondé sur une conviction : l'espace est le medium le plus puissant dans tout événement.",
        'studio-label':'Le Studio',
        'studio-p1':'Sans Titre est un studio de scénographie et de production créative basé à Beyrouth, fondé en 2026 par Marc Azzi, architecte et scénographe. Nous concevons et produisons des événements spéciaux, des expériences de marque et des défilés de mode pour des clients de luxe à travers la région et au-delà.',
        'studio-p2':'Le studio reste délibérément indépendant : chaque projet est mené directement, du premier concept à la réalisation finale, en réunissant les producteurs et les spécialistes techniques que la commande demande. Une même conviction traverse l\'ensemble : les espaces que nous construisons portent du sens, et chaque événement mérite d\'être une expérience singulière.',
        'fashion-sec-label':'<strong>Défilés de mode</strong>',
        'fashion-sec-desc':"Sans Titre traduit la vision d'un créateur en espace. Chaque décision, du sol au système d'éclairage, est au service de la collection.",
        'brand-sec-label':'<strong>Événements spéciaux</strong> et <strong>Expériences de marque</strong>',
        'brand-sec-desc':"Nous concevons des événements faits pour rester en mémoire, et des espaces qui gardent du sens longtemps après que la salle s'est vidée."},
    literals=[('<span class="sec-desc" style="text-align:left;">Atelier Sans Titre is part of<span class="m-br"><br></span> <strong style="font-weight:700;">Azzi Studios</strong> creative ecosystem.</span>',
               '<span class="sec-desc" style="text-align:left;">Atelier Sans Titre fait partie de l\'écosystème créatif <strong style="font-weight:700;">Azzi Studios</strong>.</span>')],
    group_desc=None,
    json_en='{"@context":"https://schema.org","@graph":[{"@type":"AboutPage","name":"Scenography Studio in Beirut · About · Atelier Sans Titre","url":"https://ateliersanstitre.com/about.html","isPartOf":{"@type":"WebSite","name":"Atelier Sans Titre","url":"https://ateliersanstitre.com"},"about":{"@id":"https://ateliersanstitre.com/#org"},"mainEntity":{"@id":"https://ateliersanstitre.com/#marc"}},{"@type":"Person","@id":"https://ateliersanstitre.com/#marc","name":"Marc Azzi","jobTitle":"Founder, Architect & Scenographer","worksFor":{"@id":"https://ateliersanstitre.com/#org"},"sameAs":["https://www.instagram.com/ateliersanstitre"]},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://ateliersanstitre.com/"},{"@type":"ListItem","position":2,"name":"About","item":"https://ateliersanstitre.com/about.html"}]}]}',
    json_fr='{"@context":"https://schema.org","@graph":[{"@type":"AboutPage","name":"Studio de scénographie à Beyrouth · À propos · Atelier Sans Titre","url":"https://ateliersanstitre.com/fr/about.html","inLanguage":"fr","isPartOf":{"@type":"WebSite","name":"Atelier Sans Titre","url":"https://ateliersanstitre.com"},"about":{"@id":"https://ateliersanstitre.com/#org"},"mainEntity":{"@id":"https://ateliersanstitre.com/#marc"}},{"@type":"Person","@id":"https://ateliersanstitre.com/#marc","name":"Marc Azzi","jobTitle":"Fondateur, architecte et scénographe","worksFor":{"@id":"https://ateliersanstitre.com/#org"},"sameAs":["https://www.instagram.com/ateliersanstitre"]},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":"https://ateliersanstitre.com/fr/"},{"@type":"ListItem","position":2,"name":"À propos","item":"https://ateliersanstitre.com/fr/about.html"}]}]}',
),
'disciplines.html': dict(
    en_url=f"{BASE}/disciplines.html", fr_url=f"{BASE}/fr/disciplines.html", en_canon=f"{BASE}/disciplines.html", fr_canon=f"{BASE}/fr/disciplines.html",
    en_title="Event &amp; Fashion Show Scenography in Beirut · Atelier Sans Titre",
    fr_title="Scénographie d'événements &amp; de défilés à Beyrouth · Atelier Sans Titre",
    en_desc="Atelier Sans Titre specialises in three disciplines: special events, brand experiences, and fashion shows. Explore our approach.",
    en_desc2="Atelier Sans Titre specialises in three disciplines: special events, brand experiences, and fashion shows.",
    fr_desc2="Atelier Sans Titre se spécialise dans trois disciplines : événements spéciaux, expériences de marque et défilés de mode.",
    fr_desc="Atelier Sans Titre se spécialise dans trois disciplines : événements spéciaux, expériences de marque et défilés de mode. Découvrez notre approche.",
    en_toggle_href="fr/disciplines.html", fr_toggle_href="../disciplines.html",
    fr_map={**NAV, **FOOT, 'disc-page-title':'Disciplines','filter-all':'Tous','filter-fashion':'Défilés de mode','filter-brand':'Expériences de marque','filter-events':'Événements spéciaux'},
    literals=[], group_desc=None,
    json_en='{"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","name":"Event & Fashion Show Scenography in Beirut · Atelier Sans Titre","url":"https://ateliersanstitre.com/disciplines.html","isPartOf":{"@type":"WebSite","name":"Atelier Sans Titre","url":"https://ateliersanstitre.com"}},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://ateliersanstitre.com/"},{"@type":"ListItem","position":2,"name":"Disciplines","item":"https://ateliersanstitre.com/disciplines.html"}]}]}',
    json_fr='{"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","name":"Scénographie de défilés & d\'événements à Beyrouth · Atelier Sans Titre","url":"https://ateliersanstitre.com/fr/disciplines.html","inLanguage":"fr","isPartOf":{"@type":"WebSite","name":"Atelier Sans Titre","url":"https://ateliersanstitre.com"}},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":"https://ateliersanstitre.com/fr/"},{"@type":"ListItem","position":2,"name":"Disciplines","item":"https://ateliersanstitre.com/fr/disciplines.html"}]}]}',
),
'contact.html': dict(
    en_url=f"{BASE}/contact.html", fr_url=f"{BASE}/fr/contact.html", en_canon=f"{BASE}/contact.html", fr_canon=f"{BASE}/fr/contact.html",
    en_title="Contact · Scenography &amp; Event Production, Beirut · Atelier Sans Titre",
    fr_title="Contact · Scénographie &amp; production événementielle, Beyrouth · Atelier Sans Titre",
    en_desc="Get in touch with Atelier Sans Titre. We produce special events, brand experiences, and fashion shows from our studio in Beirut.",
    fr_desc="Contactez Atelier Sans Titre. Nous produisons des événements spéciaux, des expériences de marque et des défilés de mode depuis notre studio à Beyrouth.",
    en_toggle_href="fr/contact.html", fr_toggle_href="../contact.html",
    fr_map={**NAV, **FOOT,
        'location-h1':'Beyrouth<br><span class="dim">Liban</span>',
        'contact-city-label':'Adresse',
        'contact-beirut-body':'Atelier Sans Titre<br>Beyrouth, Liban',
        'contact-services':'Événements spéciaux<br>Expériences de marque<br>Défilés de mode'},
    literals=[('title="Atelier Sans Titre, Beirut, Lebanon"', 'title="Atelier Sans Titre, Beyrouth, Liban"')],
    group_desc=None,
    json_en='{"@context":"https://schema.org","@graph":[{"@type":"ContactPage","name":"Contact · Scenography & Event Production, Beirut · Atelier Sans Titre","url":"https://ateliersanstitre.com/contact.html","isPartOf":{"@type":"WebSite","name":"Atelier Sans Titre","url":"https://ateliersanstitre.com"},"about":{"@id":"https://ateliersanstitre.com/#org"}},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://ateliersanstitre.com/"},{"@type":"ListItem","position":2,"name":"Contact","item":"https://ateliersanstitre.com/contact.html"}]}]}',
    json_fr='{"@context":"https://schema.org","@graph":[{"@type":"ContactPage","name":"Contact · Scénographie & production événementielle, Beyrouth · Atelier Sans Titre","url":"https://ateliersanstitre.com/fr/contact.html","inLanguage":"fr","isPartOf":{"@type":"WebSite","name":"Atelier Sans Titre","url":"https://ateliersanstitre.com"},"about":{"@id":"https://ateliersanstitre.com/#org"}},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":"https://ateliersanstitre.com/fr/"},{"@type":"ListItem","position":2,"name":"Contact","item":"https://ateliersanstitre.com/fr/contact.html"}]}]}',
),
}

for fname, cfg in PAGES.items():
    src = os.path.join(ROOT, fname)
    en = open(src, encoding="utf-8").read()
    assert en_toggle(cfg["en_toggle_href"]) in en, (
        f"{fname}: EN nav-toggle not found — has the English page diverged from the expected structure?")
    fr = en
    fr = fr.replace('<html lang="en">', '<html lang="fr">')
    if cfg.get("json_en"):
        assert cfg["json_en"] in fr, f"{fname}: JSON-LD changed in English page — update json_en/json_fr in CATALOG."
        fr = fr.replace(cfg["json_en"], cfg["json_fr"])
    fr = fr.replace(cfg["en_title"], cfg["fr_title"])
    fr = fr.replace(cfg["en_desc"], cfg["fr_desc"])
    if cfg.get("en_desc2"):
        fr = fr.replace(cfg["en_desc2"], cfg["fr_desc2"])
    fr = fr.replace(f'<link rel="canonical" href="{cfg["en_canon"]}">',
                    f'<link rel="canonical" href="{cfg["fr_canon"]}">')
    fr = fr.replace(f'<meta property="og:url" content="{cfg["en_url"]}">',
                    f'<meta property="og:url" content="{cfg["fr_url"]}">')
    fr = fr.replace(en_toggle(cfg["en_toggle_href"]), fr_toggle(cfg["fr_toggle_href"]))
    fr = translate(fr, cfg["fr_map"], cfg["literals"], cfg.get("group_desc"))
    for en_alt, fr_alt in ALT.items():
        fr = fr.replace(en_alt, fr_alt)
    fr = fr_paths(fr)
    open(os.path.join(FRDIR, fname), "w", encoding="utf-8").write(fr)
    print(f"✓ fr/{fname}")

print("French pages regenerated. Remember to keep sitemap.xml in sync if you add/remove pages.")
