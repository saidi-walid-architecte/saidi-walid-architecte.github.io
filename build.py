#!/usr/bin/env python3
"""Générateur statique du site Saidi Walid (FR / EN / AR).
Usage : python3 build.py  -> génère le dossier ./_site
Aucune dépendance externe.
"""
import json, re, shutil, html
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent
OUT = ROOT / "_site"
SITE = json.loads((ROOT / "data/site.json").read_text(encoding="utf-8"))
SERVICES = json.loads((ROOT / "data/services.json").read_text(encoding="utf-8"))
BASE = SITE["base_url"].rstrip("/")
LANGS = ["fr", "en", "ar"]
PREFIX = {"fr": "", "en": "/en", "ar": "/ar"}
TODAY = date.today().isoformat()

UI = {
    "fr": {"home": "Accueil", "services": "Nos services", "more": "En savoir plus →", "why": "Pourquoi nous choisir",
           "blog": "Conseils et articles", "allposts": "Tous les articles →", "read": "Lire l'article →", "faq": "Questions fréquentes",
           "visit": "Venez au bureau", "address": "Adresse", "hours": "Horaires", "phone": "Téléphone", "call": "Appeler",
           "route": "Itinéraire", "offer": "Ce que nous proposons", "others": "Autres services", "related": "Nos conseils sur ce sujet",
           "quote": "Demandez un rendez-vous par téléphone ou WhatsApp.", "about": "À propos", "notfound": "Page introuvable",
           "notfound_txt": "Cette page n'existe pas. Retournez à l'accueil.", "blog_intro": "Permis de construire, mise en conformité, expertise : nos articles pour les propriétaires et les professionnels de Batna.",
           "about_title": "À propos de Saidi Walid, architecte agréé et expert judiciaire à Batna",
           "about_txt": ["Saidi Walid est architecte agréé et expert judiciaire. Son bureau d'architecture est installé Cité Frères Lembarkia, Parc à Fourrage, à Batna.",
                         "Le bureau conçoit des projets privés et publics, monte les dossiers d'urbanisme (permis de construire, mise en conformité, certificat de conformité) et suit les chantiers.",
                         "En tant qu'expert judiciaire, Saidi Walid réalise des missions ordonnées par les juridictions de Batna en bâtiment et en foncier, et des expertises amiables à la demande des particuliers."],
           "updated": "Mis à jour le", "by": "Par"},
    "en": {"home": "Home", "services": "Our services", "more": "Learn more →", "why": "Why choose us",
           "blog": "Advice and articles", "allposts": "All articles →", "read": "Read article →", "faq": "Frequently asked questions",
           "visit": "Visit the office", "address": "Address", "hours": "Opening hours", "phone": "Phone", "call": "Call",
           "route": "Directions", "offer": "What we offer", "others": "Other services", "related": "Related advice",
           "quote": "Book an appointment by phone or WhatsApp.", "about": "About", "notfound": "Page not found",
           "notfound_txt": "This page does not exist. Go back home.", "blog_intro": "Building permits, compliance, expertise: articles for property owners and professionals in Batna.",
           "about_title": "About Saidi Walid, licensed architect and court-appointed expert in Batna",
           "about_txt": ["Saidi Walid is a licensed architect and court-appointed expert. His architecture office is located in Cité Frères Lembarkia, Parc à Fourrage, Batna, Algeria.",
                         "The office designs private and public projects, prepares planning files (building permits, regularisation, certificates of compliance) and supervises construction sites.",
                         "As a court-appointed expert, Saidi Walid carries out assignments ordered by the courts of Batna on buildings and land, as well as private surveys."],
           "updated": "Updated", "by": "By"},
    "ar": {"home": "الرئيسية", "services": "خدماتنا", "more": "← اعرف المزيد", "why": "لماذا تختاروننا",
           "blog": "نصائح ومقالات", "allposts": "← كل المقالات", "read": "← اقرأ المقال", "faq": "أسئلة شائعة",
           "visit": "زورونا في المكتب", "address": "العنوان", "hours": "أوقات العمل", "phone": "الهاتف", "call": "اتصل",
           "route": "الاتجاهات", "offer": "ما نقدمه", "others": "خدمات أخرى", "related": "نصائحنا حول الموضوع",
           "quote": "احجزوا موعدًا عبر الهاتف أو واتساب.", "about": "من نحن", "notfound": "الصفحة غير موجودة",
           "notfound_txt": "هذه الصفحة غير موجودة. عودوا إلى الصفحة الرئيسية.", "blog_intro": "رخصة البناء، تسوية البنايات، الخبرة: مقالات للملاك والمهنيين في باتنة.",
           "about_title": "من هو سعيدي وليد، المهندس المعماري المعتمد والخبير القضائي في باتنة",
           "about_txt": ["سعيدي وليد مهندس معماري معتمد وخبير قضائي. يقع مكتبه للهندسة المعمارية في حي الإخوة لمباركية، حظيرة العلف، باتنة.",
                         "يصمم المكتب مشاريع خاصة وعمومية، ويحضّر ملفات التعمير (رخصة البناء، تسوية البنايات، شهادة المطابقة) ويتابع الورشات.",
                         "وبصفته خبيرًا قضائيًا، ينجز سعيدي وليد المهام التي تسندها إليه الجهات القضائية بباتنة في مجال البناء والعقار، إضافة إلى الخبرات الودية بطلب من الخواص."],
           "updated": "آخر تحديث", "by": "بقلم"},
}
BLOG_SLUG = {"fr": "blog", "en": "blog", "ar": "blog"}
ABOUT_SLUG = {"fr": "a-propos", "en": "about", "ar": "about"}

ICONS = {
    "plan": '<path d="M3 3h18v18H3zM3 9h8v12M11 9V3M15 14h6"/>',
    "doc": '<path d="M6 2h9l5 5v15H6zM14 2v6h6M9 13h8M9 17h6"/>',
    "crane": '<path d="M4 21V5l6-2v18M10 6h11M18 6v5M16 11h4v3h-4zM2 21h12"/>',
    "check": '<path d="M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6zM8 12l3 3 5-6"/>',
    "scale": '<path d="M12 3v18M7 21h10M4 7h16M6 7l-3 7a3 3 0 006 0zM18 7l-3 7a3 3 0 006 0z"/>',
    "search": '<path d="M10 17a7 7 0 110-14 7 7 0 010 14zM21 21l-6-6M7 10h6"/>',
    "ruler": '<path d="M3 17L17 3l4 4L7 21zM7 13l2 2M10 10l2 2M13 7l2 2"/>',
    "home": '<path d="M3 11l9-8 9 8v10H3zM9 21v-6h6v6"/>',
    "building": '<path d="M4 21V4h10v17M14 9h6v12M7 8h4M7 12h4M7 16h4M2 21h20"/>',
}

def esc(s): return html.escape(s, quote=True)

def url(lang, path=""):
    p = PREFIX[lang] + "/" + (path.strip("/") + "/" if path else "")
    return p

def abs_url(lang, path=""): return BASE + url(lang, path)

# ---------- mini markdown ----------
def inline(t):
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', t)
    return t

def md(text):
    if text.lstrip().startswith("<"):
        return text  # contenu HTML venant de Pages CMS (rich-text)
    out, lst = [], None
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.strip().split("\n")
        if lines[0].startswith("## "):
            out.append(f"<h2>{inline(lines[0][3:])}</h2>")
            lines = lines[1:]
            if not lines: continue
        if all(re.match(r"^- ", l) for l in lines):
            out.append("<ul>" + "".join(f"<li>{inline(l[2:])}</li>" for l in lines) + "</ul>")
        elif all(re.match(r"^\d+\. ", l) for l in lines):
            out.append("<ol>" + "".join(f"<li>{inline(re.sub(r'^\d+\. ', '', l))}</li>" for l in lines) + "</ol>")
        else:
            out.append(f"<p>{inline(' '.join(lines))}</p>")
    return "\n".join(out)

def load_posts():
    posts = []
    for f in sorted((ROOT / "content/blog").glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        meta = {}
        for line in m.group(1).split("\n"):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
        meta["body"] = m.group(2)
        meta["date"] = str(meta.get("date", TODAY))
        posts.append(meta)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts

POSTS = load_posts()

# ---------- layout ----------
def head(lang, title, desc, path_by_lang, schema):
    d = SITE["i18n"][lang]
    canon = BASE + path_by_lang[lang]
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{BASE + p}">' for l, p in path_by_lang.items())
    if "fr" in path_by_lang:
        alts += f'<link rel="alternate" hreflang="x-default" href="{BASE + path_by_lang["fr"]}">'
    gsv = f'<meta name="google-site-verification" content="{esc(SITE["google_site_verification"])}">' if SITE["google_site_verification"] else ""
    fonts = "family=Barlow+Condensed:wght@600;700&family=Inter:wght@400;600&family=Cairo:wght@400;600;700"
    return f"""<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang == 'ar' else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#14202e">
{gsv}
<link rel="canonical" href="{canon}">
{alts}
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{BASE}/assets/og.png"><meta property="og:locale" content="{ {'fr':'fr_DZ','en':'en_US','ar':'ar_DZ'}[lang] }">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&display=swap">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">{'Aller au contenu' if lang=='fr' else 'Skip to content' if lang=='en' else 'انتقل إلى المحتوى'}</a>
<header class="top"><div class="wrap bar">
<a class="brand" href="{url(lang)}"><img src="/assets/logo.svg" alt="{esc(d['name'])}" width="44" height="44"><span><b>{esc(d['brand'])}</b><small>{esc(d['tagline'])}</small></span></a>
<nav class="langs">{''.join(f'<a href="{path_by_lang.get(l, url(l))}"{" aria-current=\"true\"" if l==lang else ""} hreflang="{l}">{l.upper()}</a>' for l in LANGS)}</nav>
<a class="btn small" href="tel:{SITE['phone_intl']}">{UI[lang]['call']}</a>
</div><div class="rule"></div></header>
<main id="main">
"""

def foot(lang):
    d, u = SITE["i18n"][lang], UI[lang]
    blog_link = f'<a href="{url(lang, BLOG_SLUG[lang])}">{u["blog"]}</a> · ' if any(p["lang"] == lang for p in POSTS) else ""
    links = "".join(f'<li><a href="{url(lang, s[lang]["slug"])}">{esc(s[lang]["title"])}</a></li>' for s in SERVICES)
    return f"""</main>
<section class="visit"><div class="wrap grid2">
<div><h2>{u['visit']}</h2>
<dl><dt>{u['address']}</dt><dd>{esc(d['street'])}, {SITE['postal_code']} {esc(d['city'])}, {esc(d['country'])}</dd>
<dt>{u['hours']}</dt><dd>{'<br>'.join(esc(h) for h in d['hours'])}</dd>
<dt>{u['phone']}</dt><dd><a href="tel:{SITE['phone_intl']}" dir="ltr">{SITE['phone_display']}</a></dd></dl>
<p class="ctas"><a class="btn" href="tel:{SITE['phone_intl']}">{u['call']}</a> <a class="btn ghost" href="https://wa.me/{SITE['whatsapp']}">WhatsApp</a> <a class="btn ghost" href="{esc(SITE['maps_url'])}" rel="noopener">{u['route']}</a></p></div>
<div><h2>{u['services']}</h2><ul class="flist">{links}</ul>
<p>{blog_link}<a href="{url(lang, ABOUT_SLUG[lang])}">{u['about']}</a></p></div>
</div></section>
<footer class="foot"><div class="wrap">© {date.today().year} {esc(d['name'])} · Batna</div></footer>
<a class="wa" href="https://wa.me/{SITE['whatsapp']}" aria-label="WhatsApp"><svg viewBox="0 0 24 24" width="28" height="28" fill="#fff"><path d="M12 2a10 10 0 00-8.6 15.1L2 22l5-1.3A10 10 0 1012 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-3.3-.8-2.8-1.1-4.5-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6-.3.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.7-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.2z"/></svg></a>
</body></html>"""

def icon(name):
    return f'<svg class="ico" viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

def hero(lang, h1, intro, crumbs=None):
    u = UI[lang]
    bc = ""
    if crumbs:
        bc = '<nav class="crumbs" aria-label="breadcrumb">' + " / ".join(
            f'<a href="{href}">{esc(t)}</a>' if href else f"<span>{esc(t)}</span>" for t, href in crumbs) + "</nav>"
    return f"""<section class="hero"><div class="wrap">{bc}
<h1>{esc(h1)}</h1><p class="lead">{esc(intro)}</p>
<p class="ctas"><a class="btn" href="tel:{SITE['phone_intl']}">{u['call']} <span dir="ltr">{SITE['phone_display']}</span></a> <a class="btn ghost light" href="https://wa.me/{SITE['whatsapp']}">WhatsApp</a></p>
</div></section>"""

def service_cards(lang, exclude=None):
    u = UI[lang]
    return '<div class="cards">' + "".join(
        f'<a class="card" href="{url(lang, s[lang]["slug"])}">{icon(s["icon"])}<h3>{esc(s[lang]["title"])}</h3><p>{esc(s[lang]["short"])}</p><span class="more">{u["more"]}</span></a>'
        for s in SERVICES if s["key"] != exclude) + "</div>"

def post_cards(lang, posts):
    u = UI[lang]
    return '<div class="cards posts">' + "".join(
        f'<a class="card" href="{url(lang, BLOG_SLUG[lang] + "/" + p["slug"])}"><time datetime="{p["date"]}">{p["date"]}</time><h3>{esc(p["title"])}</h3><p>{esc(p["description"])}</p><span class="more">{u["read"]}</span></a>'
        for p in posts) + "</div>"

def faq_html(lang, faq):
    if not faq: return ""
    return f'<section class="wrap sec"><h2>{UI[lang]["faq"]}</h2>' + "".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq) + "</section>"

# ---------- schema ----------
def org_schema(lang):
    d = SITE["i18n"][lang]
    s = {
        "@type": ["ProfessionalService", "LocalBusiness"],
        "@id": BASE + "/#business",
        "name": SITE["i18n"]["ar"]["name"] if lang == "ar" else d["name"],
        "alternateName": [SITE["i18n"]["ar"]["name"], SITE["i18n"]["fr"]["name"], "Bureau d'architecture Saidi Walid"],
        "description": d["home_desc"],
        "url": BASE + "/", "logo": BASE + "/assets/logo.svg", "image": BASE + "/assets/og.png",
        "telephone": SITE["phone_intl"],
        "address": {"@type": "PostalAddress", "streetAddress": SITE["i18n"]["fr"]["street"], "addressLocality": "Batna",
                    "postalCode": SITE["postal_code"], "addressRegion": "Batna", "addressCountry": "DZ"},
        "openingHours": SITE["opening_hours_schema"],
        "areaServed": [{"@type": "City", "name": "Batna"}, {"@type": "AdministrativeArea", "name": "Wilaya de Batna"}],
        "knowsLanguage": ["ar", "fr"],
        "founder": {"@id": BASE + "/#walid"},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": UI[lang]["services"], "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[lang]["title"], "url": abs_url(lang, s[lang]["slug"])}} for s in SERVICES]},
    }
    if SITE["same_as"]: s["sameAs"] = SITE["same_as"]
    if SITE["email"]: s["email"] = SITE["email"]
    return s

def person_schema(lang):
    return {"@type": "Person", "@id": BASE + "/#walid", "name": "Saidi Walid", "alternateName": "سعيدي وليد",
            "jobTitle": {"fr": "Architecte agréé et expert judiciaire", "en": "Licensed architect and court-appointed expert", "ar": "مهندس معماري معتمد وخبير قضائي"}[lang],
            "worksFor": {"@id": BASE + "/#business"}, "url": abs_url(lang, ABOUT_SLUG[lang]),
            "knowsAbout": ["Architecture", "Urbanisme", "Permis de construire", "Expertise judiciaire", "Expertise bâtiment", "Foncier"]}

def crumbs_schema(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

def faq_schema(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def graph(*items): return {"@context": "https://schema.org", "@graph": list(items)}

# ---------- writers ----------
SITEMAP = []

def write(path_by_lang, lang, content):
    p = path_by_lang[lang]
    f = OUT / p.strip("/") / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content, encoding="utf-8")
    SITEMAP.append((p, path_by_lang))

def build_home(lang):
    d, u = SITE["i18n"][lang], UI[lang]
    pbl = {l: url(l) for l in LANGS}
    faq = [[{"fr": "Où se trouve le bureau ?", "en": "Where is the office?", "ar": "أين يقع المكتب؟"}[lang],
            f"{d['street']}, {SITE['postal_code']} {d['city']}, {d['country']}."],
           [{"fr": "Quels sont vos horaires ?", "en": "What are your opening hours?", "ar": "ما هي أوقات العمل؟"}[lang], " ; ".join(d["hours"]) + "."],
           [{"fr": "Comment prendre rendez-vous ?", "en": "How do I book an appointment?", "ar": "كيف أحجز موعدًا؟"}[lang],
            {"fr": f"Par téléphone ou WhatsApp au {SITE['phone_display']}.", "en": f"By phone or WhatsApp on {SITE['phone_intl']}.", "ar": f"عبر الهاتف أو واتساب على الرقم {SITE['phone_display'].replace(' ', '')}."}[lang]],
           [{"fr": "Quels services proposez-vous ?", "en": "What services do you offer?", "ar": "ما هي الخدمات التي تقدمونها؟"}[lang],
            ("، " if lang == "ar" else ", ").join(s[lang]["title"] for s in SERVICES) + "."]]
    lposts = [p for p in POSTS if p["lang"] == lang][:3]
    why = '<div class="cards why">' + "".join(f"<div class='card plain'><h3>{esc(t)}</h3><p>{esc(x)}</p></div>" for t, x in d["why"]) + "</div>"
    body = hero(lang, d["home_h1"], d["home_intro"])
    body += f'<section class="wrap sec"><h2>{u["services"]}</h2>{service_cards(lang)}</section>'
    body += f'<section class="wrap sec"><h2>{u["why"]}</h2>{why}</section>'
    if lposts:
        body += f'<section class="wrap sec"><h2>{u["blog"]}</h2>{post_cards(lang, lposts)}<p><a class="link" href="{url(lang, BLOG_SLUG[lang])}">{u["allposts"]}</a></p></section>'
    body += faq_html(lang, faq)
    schema = graph(org_schema(lang), person_schema(lang),
                   {"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": d["name"], "inLanguage": lang, "publisher": {"@id": BASE + "/#business"}},
                   faq_schema(faq))
    write(pbl, lang, head(lang, d["home_title"], d["home_desc"], pbl, schema) + body + foot(lang))

def build_service(s, lang):
    c, u = s[lang], UI[lang]
    pbl = {l: url(l, s[l]["slug"]) for l in LANGS}
    rel = [p for p in POSTS if p["lang"] == lang and p.get("service") == s["key"]]
    body = hero(lang, c["h1"], c["intro"], [(u["home"], url(lang)), (c["title"], None)])
    body += f'<p class="wrap note">{u["quote"]}</p>'
    body += f'<section class="wrap sec"><h2>{u["offer"]}</h2><ul class="checks">' + "".join(f"<li>{esc(i)}</li>" for i in c["items"]) + "</ul></section>"
    body += faq_html(lang, c["faq"])
    if rel: body += f'<section class="wrap sec"><h2>{u["related"]}</h2>{post_cards(lang, rel)}</section>'
    body += f'<section class="wrap sec"><h2>{u["others"]}</h2>{service_cards(lang, exclude=s["key"])}</section>'
    schema = graph(
        {"@type": "Service", "name": c["title"], "description": c["meta_desc"], "serviceType": c["title"], "url": abs_url(lang, c["slug"]),
         "provider": {"@id": BASE + "/#business"}, "areaServed": {"@type": "City", "name": "Batna"}, "inLanguage": lang},
        crumbs_schema([(u["home"], abs_url(lang)), (c["title"], abs_url(lang, c["slug"]))]),
        faq_schema(c["faq"]), org_schema(lang))
    write(pbl, lang, head(lang, c["meta_title"], c["meta_desc"], pbl, schema) + body + foot(lang))

def build_blog(lang):
    u = UI[lang]
    lposts = [p for p in POSTS if p["lang"] == lang]
    pbl = {l: url(l, BLOG_SLUG[l]) for l in LANGS if any(p["lang"] == l for p in POSTS)}
    if lang not in pbl: return
    title = {"fr": "Conseils architecture, permis et expertise à Batna", "en": "Architecture, permit and expertise advice in Batna", "ar": "نصائح في الهندسة المعمارية والرخص والخبرة بباتنة"}[lang]
    body = hero(lang, title, u["blog_intro"], [(u["home"], url(lang)), (u["blog"], None)])
    body += f'<section class="wrap sec">{post_cards(lang, lposts)}</section>'
    schema = graph({"@type": "Blog", "name": title, "url": abs_url(lang, BLOG_SLUG[lang]), "publisher": {"@id": BASE + "/#business"}, "inLanguage": lang},
                   crumbs_schema([(u["home"], abs_url(lang)), (u["blog"], abs_url(lang, BLOG_SLUG[lang]))]), org_schema(lang))
    write(pbl, lang, head(lang, title + " | " + SITE["i18n"][lang]["brand"], u["blog_intro"], pbl, schema) + body + foot(lang))

def build_post(p):
    lang, u = p["lang"], UI[p["lang"]]
    sib = {q["lang"]: q for q in POSTS if q["key"] == p["key"]}
    pbl = {l: url(l, BLOG_SLUG[l] + "/" + q["slug"]) for l, q in sib.items()}
    svc = next((s for s in SERVICES if s["key"] == p.get("service")), None)
    link = f'<aside class="box"><a href="{url(lang, svc[lang]["slug"])}">{esc(svc[lang]["title"])} →</a></aside>' if svc else ""
    body = f"""<article class="wrap post"><nav class="crumbs dark"><a href="{url(lang)}">{u['home']}</a> / <a href="{url(lang, BLOG_SLUG[lang])}">{u['blog']}</a></nav>
<h1>{esc(p['title'])}</h1><p class="meta">{u['by']} <a href="{url(lang, ABOUT_SLUG[lang])}">{'سعيدي وليد' if lang=='ar' else 'Saidi Walid'}</a>, {SITE['i18n'][lang]['tagline'].lower() if lang!='ar' else SITE['i18n'][lang]['tagline']} · {u['updated']} <time datetime="{p['date']}">{p['date']}</time></p>
{md(p['body'])}{link}</article>"""
    others = [q for q in POSTS if q["lang"] == lang and q["key"] != p["key"]][:3]
    if others: body += f'<section class="wrap sec"><h2>{u["blog"]}</h2>{post_cards(lang, others)}</section>'
    full = abs_url(lang, BLOG_SLUG[lang] + "/" + p["slug"])
    schema = graph({"@type": "BlogPosting", "headline": p["title"], "description": p["description"], "datePublished": p["date"], "dateModified": p["date"],
                    "inLanguage": lang, "mainEntityOfPage": full, "author": {"@id": BASE + "/#walid"}, "publisher": {"@id": BASE + "/#business"}, "image": BASE + "/assets/og.png"},
                   person_schema(lang),
                   crumbs_schema([(u["home"], abs_url(lang)), (u["blog"], abs_url(lang, BLOG_SLUG[lang])), (p["title"], full)]))
    write(pbl, lang, head(lang, p["title"] + " | " + SITE["i18n"][lang]["brand"], p["description"], pbl, schema) + body + foot(lang))

def build_about(lang):
    u = UI[lang]
    pbl = {l: url(l, ABOUT_SLUG[l]) for l in LANGS}
    body = hero(lang, u["about_title"], u["about_txt"][0], [(u["home"], url(lang)), (u["about"], None)])
    body += '<section class="wrap sec prose">' + "".join(f"<p>{esc(t)}</p>" for t in u["about_txt"][1:]) + "</section>"
    schema = graph({"@type": "AboutPage", "url": abs_url(lang, ABOUT_SLUG[lang]), "mainEntity": {"@id": BASE + "/#walid"}}, person_schema(lang), org_schema(lang))
    write(pbl, lang, head(lang, u["about_title"], u["about_txt"][0], pbl, schema) + body + foot(lang))

def build_404():
    u = UI["fr"]
    pbl = {"fr": "/404.html"}
    page = head("fr", u["notfound"], u["notfound_txt"], pbl, graph(org_schema("fr"))).replace('content="index,follow,max-image-preview:large"', 'content="noindex"')
    page += f'<section class="hero"><div class="wrap"><h1>{u["notfound"]}</h1><p class="lead">{u["notfound_txt"]}</p><p><a class="btn" href="/">{u["home"]}</a></p></div></section>' + foot("fr")
    (OUT / "404.html").write_text(page, encoding="utf-8")

def build_meta_files():
    seen, urls = set(), []
    for p, pbl in SITEMAP:
        if p in seen: continue
        seen.add(p)
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{BASE + q}"/>' for l, q in pbl.items())
        urls.append(f"<url><loc>{BASE + p}</loc><lastmod>{TODAY}</lastmod>{alts}</url>")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    d = SITE["i18n"]["fr"]
    llms = [f"# {d['name']} ({SITE['i18n']['ar']['name']})", "", f"> {d['home_intro']}", "",
            f"- Adresse : {d['street']}, {SITE['postal_code']} Batna, Algérie", f"- Téléphone / WhatsApp : {SITE['phone_intl']}", f"- Horaires : {' ; '.join(d['hours'])}", "", "## Services"]
    llms += [f"- [{s['fr']['title']}]({abs_url('fr', s['fr']['slug'])}) : {s['fr']['short']}" for s in SERVICES]
    llms += ["", "## Articles"] + [f"- [{p['title']}]({abs_url(p['lang'], BLOG_SLUG[p['lang']] + '/' + p['slug'])}) : {p['description']}" for p in POSTS]
    llms += ["", "## Langues", f"- Français : {BASE}/", f"- English : {BASE}/en/", f"- العربية : {BASE}/ar/"]
    (OUT / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("")

def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    for lang in LANGS:
        build_home(lang); build_blog(lang); build_about(lang)
        for s in SERVICES: build_service(s, lang)
    for p in POSTS: build_post(p)
    build_404(); build_meta_files()
    print(f"OK : {len(set(p for p, _ in SITEMAP))} pages -> {OUT}")

if __name__ == "__main__":
    main()
