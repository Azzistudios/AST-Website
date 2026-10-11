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
 "Downtown Beirut, a street between stone facades":"Le centre-ville de Beyrouth, une rue entre des façades de pierre",
 "Nejmeh Square, Beirut, the clock tower at midday":"La place de l'Étoile à Beyrouth, la tour de l'horloge à midi",
 "Beirut at night from above, the marina and the coast road":"Beyrouth la nuit vue d'en haut, la marina et la corniche",
 "Concept render, a lit linen vault with guests walking through":"Rendu de concept, une voûte de lin éclairée que des invités traversent",
 "Concept render, a steel plinth against grey plaster in daylight":"Rendu de concept, un socle en acier contre un enduit gris, en lumière du jour",
 "Concept render, a wall of red light with guests in silhouette":"Rendu de concept, un mur de lumière rouge et des invités en silhouette",
 "Concept render, a long dinner table under a draped canopy at dusk":"Rendu de concept, une longue table de dîner sous un voile tendu, au crépuscule",
 "Concept render, an exhibition opening hung with framed pictures":"Rendu de concept, un vernissage aux murs couverts de tableaux encadrés",
 "Concept render, a long candlelit table in a dark hall":"Rendu de concept, une longue table aux chandelles dans une salle sombre",
 "Concept render, a gallery of framed images with a long table":"Rendu de concept, une galerie de tableaux encadrés et une longue table",
 "Concept render, a curved metal wall on a blue floor":"Rendu de concept, un mur de métal courbe sur un sol bleu",
 "Concept render, long tables under light shafts in a stone hall":"Rendu de concept, de longues tables sous des rais de lumière dans une salle de pierre",
 "Concept render, an empty runway lit by a line of light":"Rendu de concept, un podium vide éclairé par une ligne de lumière",
 "Concept render, a wall of red fluted glass catching the light":"Rendu de concept, un mur de verre cannelé rouge qui accroche la lumière",
 "Concept render, a hand drawing a stage plan":"Rendu de concept, une main dessinant un plan de scène",
 "Concept render, a dark salon with a vertical slit of warm light":"Rendu de concept, un salon sombre fendu d'une ligne verticale de lumière chaude",
 "Concept render, a corridor washed in red light":"Rendu de concept, un couloir baigné de lumière rouge",
 "A private dinner in an art gallery under red light, one long table laid with candles and flowers":"Un dîner privé dans une galerie d'art sous lumière rouge, une longue table dressée avec bougies et fleurs",
 "The long table down the gallery, candles and flowers under red light":"La longue table le long de la galerie, bougies et fleurs sous lumière rouge",
 "Martini glasses lined up on the bar under red light, paintings behind":"Des verres à martini alignés sur le bar sous lumière rouge, des tableaux derrière",
 "A private dinner hosted by Marc Azzi in an art gallery, one long table under red light":"Un dîner privé organisé par Marc Azzi dans une galerie d'art, une longue table sous lumière rouge",
}

NAV = {'skip':'Aller au contenu','nav-private':'Privé','nav-brands':'Marques','nav-concepts':'Concepts','nav-about':'À propos','nav-faq':'FAQ','nav-contact':'Contact'}
TAGS = {'tag-fashion':'Mode','tag-jewellery':'Joaillerie','tag-beauty':'Beauté','tag-spirits':'Spiritueux','tag-automotive':'Automobile','tag-culture':'Culture & Arts'}
FOOT = {'footer-tagline':'Nous concevons les lieux qui rassemblent','footer-location':'Beyrouth, Liban','copyright':'© 2026 Atelier Sans Titre. Tous droits réservés.','ecosystem':"Fait partie de l'écosystème créatif Azzi Studios.",'legal-privacy':'Confidentialité','legal-notice':'Mentions légales'}

PROJ = {
 'proj-e1-t':'The Vernissage','proj-e1-d':'Concept · Marques',
 'proj-e2-t':'The Long Table','proj-e2-d':'Concept · Privé',
 'proj-e3-t':'After Dark','proj-e3-d':'Concept · Marques',
 'proj-b1-t':'The Couture Salon','proj-b1-d':'Concept · Marques',
 'proj-b2-t':'Hall of Images','proj-b2-d':'Concept · Marques',
 'proj-b3-t':'Silhouettes','proj-b3-d':'Concept · Marques',
    'proj-dr-t':'Dinner in Red','proj-dr-d':'Réalisé · Privé',
 'proj-f1-t':'Three Rooms','proj-f1-d':'Concept · Marques',
 'proj-f2-t':'Three Rooms','proj-f2-d':'Concept · Marques',
 'proj-f3-t':'Three Rooms','proj-f3-d':'Concept · Marques',
}

# ── CATALOG: per-page French text + URLs ──
PAGES = {
'index.html': dict(
    en_url=f"{BASE}/", fr_url=f"{BASE}/fr/", en_canon=f"{BASE}/", fr_canon=f"{BASE}/fr/",
    en_title="Atelier Sans Titre · Event Scenography, Beirut",
    fr_title="Atelier Sans Titre · Scénographie événementielle, Beyrouth",
    en_desc="Event scenography studio in Beirut. Weddings and private events, brand and corporate events, fashion shows. We design where people gather.",
    fr_desc="Studio de scénographie événementielle à Beyrouth. Mariages, événements privés, événements de marque, défilés. Nous concevons les lieux qui rassemblent.",
    en_toggle_href="fr/index.html", fr_toggle_href="../index.html", json_en=None, json_fr=None,
    fr_map={**NAV, **TAGS, **FOOT, **PROJ,
        'tagline':'<strong>Nous concevons les lieux<span class="d-br"><br></span> qui rassemblent.</strong>',
        'tagline-sub':'Scénographie événementielle pour mariages, célébrations privées, marques et défilés. Depuis Beyrouth.',
        'positioning':"Nous concevons d'abord le lieu : l'entrée, la place de chacun, la lumière à mesure que la nuit avance. Puis nous le construisons et dirigeons l'événement. Un studio de scénographie, chez lui à Beyrouth.",
        'side-private-label':'Privé','side-private-line':'Pour ceux que vous aimez. Mariages, fiançailles et dîners privés.','side-private-link':'Privé →',
        'side-brands-label':'Marques','side-brands-line':"Pour ceux que vous voulez impressionner. Défilés, lancements et événements d'entreprise.",'side-brands-link':'Marques →',
        'work-label':'Concepts',
        'work-desc':'Études des lieux que nous concevons.',
        'location-sub':'Notre base. Notre perspective.',
        'location-heading':'Beyrouth<br><span class="arrow">→ Liban</span>',
        'location-body':"Basés à Beyrouth, nous concevons des mariages, des événements privés, des événements de marque et d'entreprise et des défilés partout au Liban, et dans la région quand un projet le demande.",
        'insta-label':'Suivez-nous sur Instagram',
        'cta-title':'Parlez-nous de votre événement.',
        'cta-body':'Une date, un lieu, le nombre d\'invités. Nous répondrons par un espace.',
        'cta-link':'Écrivez-nous'},
    literals=[],
    group_desc=None,
),
'work.html': dict(
    en_url=f"{BASE}/work.html", fr_url=f"{BASE}/fr/work.html", en_canon=f"{BASE}/work.html", fr_canon=f"{BASE}/fr/work.html",
    en_title="Concepts · Atelier Sans Titre",
    fr_title="Concepts · Atelier Sans Titre",
    en_desc="Concept studies by Atelier Sans Titre for private events, brand events and fashion shows. Built projects follow this season.",
    fr_desc="Études de concepts par Atelier Sans Titre pour des événements privés, des événements de marque et des défilés. Les projets réalisés suivent cette saison.",
    en_toggle_href="fr/work.html", fr_toggle_href="../work.html",
    fr_map={**NAV, **TAGS, **FOOT, **PROJ,
        'work-h1':'<strong>Concepts</strong>',
        'work-standfirst':'Le premier dîner que nous avons réalisé, et des études des lieux que nous concevons.',
        'disc-built-label':'Réalisé',
          'disc-private-label':'Privé',
        'disc-brands-label':'Marques'},
    literals=[], group_desc=None,
    json_en='{"@context":"https://schema.org","@graph":[{"@type":"WebPage","name":"Special Events, Brand Experiences & Fashion Shows · Work · Atelier Sans Titre","url":"https://ateliersanstitre.com/work.html","isPartOf":{"@type":"WebSite","name":"Atelier Sans Titre","url":"https://ateliersanstitre.com"}},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://ateliersanstitre.com/"},{"@type":"ListItem","position":2,"name":"Work","item":"https://ateliersanstitre.com/work.html"}]}]}',
    json_fr='{"@context":"https://schema.org","@graph":[{"@type":"WebPage","name":"Événements spéciaux, expériences de marque & défilés de mode · Travail · Atelier Sans Titre","url":"https://ateliersanstitre.com/fr/work.html","inLanguage":"fr","isPartOf":{"@type":"WebSite","name":"Atelier Sans Titre","url":"https://ateliersanstitre.com"}},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":"https://ateliersanstitre.com/fr/"},{"@type":"ListItem","position":2,"name":"Travail","item":"https://ateliersanstitre.com/fr/work.html"}]}]}',
),
'about.html': dict(
    en_url=f"{BASE}/about.html", fr_url=f"{BASE}/fr/about.html", en_canon=f"{BASE}/about.html", fr_canon=f"{BASE}/fr/about.html",
    en_title="Scenography Studio in Beirut · About · Atelier Sans Titre",
    fr_title="Studio de scénographie, Beyrouth · Atelier Sans Titre",
    en_desc="Atelier Sans Titre is an event scenography studio in Beirut, founded by Marc Azzi, architect. Weddings, private events, brand and corporate events, fashion shows.",
    fr_desc="Atelier Sans Titre est un studio de scénographie événementielle à Beyrouth, fondé par Marc Azzi, architecte. Mariages, événements privés, événements de marque, défilés.",
    en_desc2="Atelier Sans Titre is an event scenography studio in Beirut, founded by Marc Azzi, architect. Weddings, private events, brand and corporate events, fashion shows.",
    fr_desc2="Atelier Sans Titre est un studio de scénographie événementielle à Beyrouth, fondé par Marc Azzi, architecte. Mariages, événements privés, événements de marque, défilés.",
    en_toggle_href="fr/about.html", fr_toggle_href="../about.html",
    fr_map={**NAV, **FOOT,
        'about-h1':'Un studio de <strong>scénographie événementielle</strong><span class="m-br"><br></span> à <strong>Beyrouth</strong>.',
        "studio-credential":"Architecte de formation, Marc Azzi dirige lui-même chaque projet, du premier dessin à la dernière soirée.",
        "studio-sectors":"Pour les marques, le travail touche la mode, la joaillerie, la beauté, les spiritueux, l'automobile, l'art et la culture.",
        "howwework-label":"Notre méthode",
        "howwework-body":"<strong>Concept.</strong> Nous lisons le brief et parcourons le lieu à l'heure où vous l'utiliserez, et répondons par une idée d'espace.<br><strong>Conception.</strong> L'idée est dessinée, maquettée et chiffrée jusqu'à ce qu'elle tienne.<br><strong>Réalisation.</strong> Nous la produisons sur place : fabrication, lumière, technique, et la conduite finale.",
        "howwework-cta":"Voir les concepts",
        "cta-title":"Parlez-nous de votre événement.",
        "cta-body":"Une date, un lieu, le nombre d'invités. Nous répondrons par un espace.",
        "cta-link":"Écrivez-nous",
        "credits":"Photographies © leurs auteurs respectifs.<br>Images de projets publiées avec l'accord des clients.",
        'page-title':'À propos',
        'page-desc':"Atelier Sans Titre est un studio de scénographie événementielle à Beyrouth, fondé par Marc Azzi, architecte. Mariages, événements privés, événements de marque, défilés.",
        'studio-label':'Le Studio',
        'studio-p1':"Atelier Sans Titre est un studio de scénographie événementielle à Beyrouth, fondé en 2026 par Marc Azzi, architecte et scénographe. Nous concevons des mariages et des événements privés, des événements de marque et d'entreprise, et des défilés : la pièce, la lumière, la façon dont on y entre. Puis nous les organisons, les construisons et dirigeons l'événement.",
        'studio-p2':'Le studio reste indépendant, à dessein. Vous travaillez avec la personne qui a dessiné la pièce, de la première visite du lieu au dernier invité.',
        'fashion-sec-label':'Marques',
        'fashion-sec-desc':"Mode, événements de marque et d'entreprise.",
        'brand-sec-label':'Privé',
        'brand-sec-desc':'Mariages et événements privés.'},
    literals=[('<span class="sec-desc" style="text-align:left;">Atelier Sans Titre is part of<span class="m-br"><br></span> <strong style="font-weight:700;">Azzi Studios</strong> creative ecosystem.</span>',
               '<span class="sec-desc" style="text-align:left;">Atelier Sans Titre fait partie de l\'écosystème créatif <strong style="font-weight:700;">Azzi Studios</strong>.</span>')],
    group_desc=None,
    json_en='{"@context":"https://schema.org","@graph":[{"@type":"AboutPage","name":"Scenography Studio in Beirut · About · Atelier Sans Titre","url":"https://ateliersanstitre.com/about.html","isPartOf":{"@type":"WebSite","name":"Atelier Sans Titre","url":"https://ateliersanstitre.com"},"about":{"@id":"https://ateliersanstitre.com/#org"},"mainEntity":{"@id":"https://ateliersanstitre.com/#marc"}},{"@type":"Person","@id":"https://ateliersanstitre.com/#marc","name":"Marc Azzi","jobTitle":"Founder, Architect & Scenographer","worksFor":{"@id":"https://ateliersanstitre.com/#org"},"sameAs":["https://www.instagram.com/ateliersanstitre"]},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://ateliersanstitre.com/"},{"@type":"ListItem","position":2,"name":"About","item":"https://ateliersanstitre.com/about.html"}]}]}',
    json_fr='{"@context":"https://schema.org","@graph":[{"@type":"AboutPage","name":"Studio de scénographie à Beyrouth · À propos · Atelier Sans Titre","url":"https://ateliersanstitre.com/fr/about.html","inLanguage":"fr","isPartOf":{"@type":"WebSite","name":"Atelier Sans Titre","url":"https://ateliersanstitre.com"},"about":{"@id":"https://ateliersanstitre.com/#org"},"mainEntity":{"@id":"https://ateliersanstitre.com/#marc"}},{"@type":"Person","@id":"https://ateliersanstitre.com/#marc","name":"Marc Azzi","jobTitle":"Fondateur, architecte et scénographe","worksFor":{"@id":"https://ateliersanstitre.com/#org"},"sameAs":["https://www.instagram.com/ateliersanstitre"]},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":"https://ateliersanstitre.com/fr/"},{"@type":"ListItem","position":2,"name":"À propos","item":"https://ateliersanstitre.com/fr/about.html"}]}]}',
),
'contact.html': dict(
    en_url=f"{BASE}/contact.html", fr_url=f"{BASE}/fr/contact.html", en_canon=f"{BASE}/contact.html", fr_canon=f"{BASE}/fr/contact.html",
    en_title="Contact · Atelier Sans Titre, Beirut",
    fr_title="Contact · Atelier Sans Titre, Beyrouth",
    en_desc="Write to Atelier Sans Titre: weddings, private events, brand events and fashion shows. Email, WhatsApp or phone, from Beirut.",
    fr_desc="Écrivez à Atelier Sans Titre : mariages, événements privés, événements de marque et défilés. E-mail, WhatsApp ou téléphone, depuis Beyrouth.",
    en_toggle_href="fr/contact.html", fr_toggle_href="../contact.html",
    fr_map={**NAV, **FOOT,
        'contact-lead':"Parlez-nous de votre événement. Une date, un lieu, le nombre d'invités. Nous répondrons par un espace.",
        'location-h1':'Écrivez-nous.',
        "contact-kicker":"Contact",
        "contact-h1":"Scénographie et production d'événements, Beyrouth",
        'contact-city-label':'Adresse',
        'contact-beirut-body':'Atelier Sans Titre<br>Beyrouth, Liban',
        'contact-services':'<a href="private.html">Privé</a><br><a href="brands.html">Marques</a>'},
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
