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
import hashlib
CSSV = hashlib.md5((ROOT / "assets/style.css").read_bytes()).hexdigest()[:8]

UI = {
    "fr": {"home": "Accueil", "services": "Nos services", "more": "En savoir plus →", "why": "Pourquoi nous choisir",
           "blog": "Conseils et articles", "allposts": "Tous les articles →", "read": "Lire l'article →", "faq": "Questions fréquentes",
           "visit": "Venez au bureau", "address": "Adresse", "hours": "Horaires", "phone": "Téléphone", "call": "Appeler",
           "route": "Itinéraire", "offer": "Ce que nous proposons", "others": "Autres services", "related": "Nos conseils sur ce sujet",
           "quote": "Demandez un rendez-vous par téléphone ou WhatsApp.", "about": "À propos", "notfound": "Page introuvable",
           "notfound_txt": "Cette page n'existe pas. Retournez à l'accueil.", "blog_intro": "Permis de construire, mise en conformité, expertise : nos articles pour les propriétaires et les professionnels de Batna.",
           "about_title": "À propos de Saidi Walid, architecte agréé et expert judiciaire à Batna",
           "about_txt": ["Saidi Walid est architecte agréé et expert judiciaire. Son bureau d'architecture est installé Cité Frères Lembarkia, à Batna.",
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
           "about_txt": ["Saidi Walid is a licensed architect and court-appointed expert. His architecture office is located in Cité Frères Lembarkia, Batna, Algeria.",
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
           "about_txt": ["سعيدي وليد مهندس معماري معتمد وخبير قضائي. يقع مكتبه للهندسة المعمارية في حي الإخوة لمباركية، باتنة.",
                         "يصمم المكتب مشاريع خاصة وعمومية، ويحضّر ملفات التعمير (رخصة البناء، تسوية البنايات، شهادة المطابقة) ويتابع الورشات.",
                         "وبصفته خبيرًا قضائيًا، ينجز سعيدي وليد المهام التي تسندها إليه الجهات القضائية بباتنة في مجال البناء والعقار، إضافة إلى الخبرات الودية بطلب من الخواص."],
           "updated": "آخر تحديث", "by": "بقلم"},
}
BLOG_SLUG = {"fr": "blog", "en": "blog", "ar": "blog"}
ABOUT_SLUG = {"fr": "a-propos", "en": "about", "ar": "about"}
QUOTE_SLUG = {"fr": "devis", "en": "quote", "ar": "quote"}
QL = {"fr": "Demander un devis", "en": "Request a quote", "ar": "اطلب عرض سعر"}

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
        if lines[0].startswith("### "):
            out.append(f"<h3>{inline(lines[0][4:])}</h3>")
            lines = lines[1:]
            if not lines: continue
        elif lines[0].startswith("## "):
            out.append(f'<h2 id="s{sum(1 for x in out if x.startswith("<h2"))+1}">{inline(lines[0][3:])}</h2>')
            lines = lines[1:]
            if not lines: continue
        if all(re.match(r"^- ", l) for l in lines):
            out.append("<ul>" + "".join(f"<li>{inline(l[2:])}</li>" for l in lines) + "</ul>")
        elif all(re.match(r"^\d+\. ", l) for l in lines):
            out.append("<ol>" + "".join(f"<li>{inline(re.sub(r'^\d+\. ', '', l))}</li>" for l in lines) + "</ol>")
        elif all(l.startswith("|") for l in lines):
            rows = [[c.strip() for c in l.strip("|").split("|")] for l in lines if not re.match(r"^\|[-\s|:]+\|$", l)]
            h = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
            bd = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{bd}</tbody></table></div>')
        elif all(l.startswith("> ") for l in lines):
            out.append('<blockquote class="field">' + inline(" ".join(l[2:] for l in lines)) + "</blockquote>")
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

NAV = {
    "fr": {"home": "Accueil", "services": "Services", "exp": "Expertise judiciaire", "blog": "Blog", "about": "À propos", "contact": "Contact", "menu": "Menu", "all": "Tous les services"},
    "en": {"home": "Home", "services": "Services", "exp": "Court expertise", "blog": "Blog", "about": "About", "contact": "Contact", "menu": "Menu", "all": "All services"},
    "ar": {"home": "الرئيسية", "services": "الخدمات", "exp": "الخبرة القضائية", "blog": "المدونة", "about": "من نحن", "contact": "اتصل بنا", "menu": "القائمة", "all": "كل الخدمات"},
}

def main_nav(lang, cur):
    n = NAV[lang]
    exp = next(s for s in SERVICES if s["key"] == "expertise-judiciaire")
    def a(href, label, cls=""):
        c = ' aria-current="page"' if cur and href != url(lang) and cur.startswith(href) else (' aria-current="page"' if cur == href else "")
        return f'<a href="{href}"{c}{(" class=" + chr(34) + cls + chr(34)) if cls else ""}>{esc(label)}</a>'
    svc_links = "".join(f'<li><a href="{url(lang, s[lang]["slug"])}">{esc(s[lang]["title"])}</a></li>' for s in SERVICES)
    has_blog = any(q["lang"] == lang for q in POSTS)
    items = [a(url(lang), n["home"]),
             f'<div class="dd"><button type="button" aria-haspopup="true">{n["services"]} <span aria-hidden="true">▾</span></button><ul class="ddm">{svc_links}</ul></div>',
             a(url(lang, exp[lang]["slug"]), n["exp"])]
    if has_blog: items.append(a(url(lang, BLOG_SLUG[lang]), n["blog"]))
    items += [a(url(lang, ABOUT_SLUG[lang]), n["about"]), f'<a href="#contact">{n["contact"]}</a>']
    desk = '<nav class="mainnav" aria-label="main">' + "".join(items) + "</nav>"
    mob_items = [a(url(lang), n["home"]), f'<details><summary>{n["services"]}</summary><ul>{svc_links}</ul></details>', a(url(lang, exp[lang]["slug"]), n["exp"])]
    if has_blog: mob_items.append(a(url(lang, BLOG_SLUG[lang]), n["blog"]))
    mob_items += [a(url(lang, ABOUT_SLUG[lang]), n["about"]), f'<a href="#contact">{n["contact"]}</a>', f'<a class="btn" href="{url(lang, QUOTE_SLUG[lang])}">{QL[lang]}</a>', f'<a class="btn ghost" href="tel:{SITE["phone_intl"]}">{UI[lang]["call"]} <span dir="ltr">{SITE["phone_display"]}</span></a>']
    mob = f'<details class="burger"><summary aria-label="{n["menu"]}"><span></span><span></span><span></span></summary><div class="mpanel">' + "".join(mob_items) + "</div></details>"
    return desk + mob

# ---------- layout ----------
def head(lang, title, desc, path_by_lang, schema):
    d = SITE["i18n"][lang]
    canon = BASE + path_by_lang[lang]
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{BASE + p}">' for l, p in path_by_lang.items())
    if "fr" in path_by_lang:
        alts += f'<link rel="alternate" hreflang="x-default" href="{BASE + path_by_lang["fr"]}">'
    gsv = f'<meta name="google-site-verification" content="{esc(SITE["google_site_verification"])}">' if SITE["google_site_verification"] else ""
    navlink = main_nav(lang, path_by_lang.get(lang, ""))
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
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="/assets/favicon-96.png" sizes="96x96" type="image/png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&display=swap">
<link rel="stylesheet" href="/assets/style.css?v={CSSV}">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">{'Aller au contenu' if lang=='fr' else 'Skip to content' if lang=='en' else 'انتقل إلى المحتوى'}</a>
<header class="top"><div class="wrap bar">
<a class="brand" href="{url(lang)}"><img src="/assets/logo.svg" alt="{esc(d['name'])}" width="44" height="44"><span><b>{esc(d['brand'])}</b><small>{esc(d['tagline'])}</small></span></a>
{navlink}
<nav class="langs">{''.join(f'<a href="{path_by_lang.get(l, url(l))}"{" aria-current=\"true\"" if l==lang else ""} hreflang="{l}">{l.upper()}</a>' for l in LANGS)}</nav>
<a class="btn small" href="{url(lang, QUOTE_SLUG[lang])}"><span class="ql">{QL[lang]}</span><span class="qs">{ {"fr": "Devis", "en": "Quote", "ar": "عرض سعر"}[lang] }</span></a>
</div><div class="rule"></div></header>
<main id="main">
"""

def foot(lang):
    d, u = SITE["i18n"][lang], UI[lang]
    blog_link = f'<a href="{url(lang, BLOG_SLUG[lang])}">{u["blog"]}</a> · ' if any(p["lang"] == lang for p in POSTS) else ""
    links = "".join(f'<li><a href="{url(lang, s[lang]["slug"])}">{esc(s[lang]["title"])}</a></li>' for s in SERVICES)
    return f"""</main>
<section class="visit" id="contact"><div class="wrap grid2">
<div><h2>{u['visit']}</h2>
<dl><dt>{u['address']}</dt><dd>{esc(d['street'])}, {SITE['postal_code']} {esc(d['city'])}, {esc(d['country'])}</dd>
<dt>{u['hours']}</dt><dd>{'<br>'.join(esc(h) for h in d['hours'])}</dd>
<dt>{u['phone']}</dt><dd><a href="tel:{SITE['phone_intl']}" dir="ltr">{SITE['phone_display']}</a></dd>{f'<dt>E-mail</dt><dd><a href="mailto:{SITE["email"]}" dir="ltr">{SITE["email"]}</a></dd>' if SITE['email'] else ''}</dl>
<p class="ctas"><a class="btn" href="{url(lang, QUOTE_SLUG[lang])}">{QL[lang]}</a> <a class="btn ghost" href="tel:{SITE['phone_intl']}">{u['call']}</a> <a class="btn ghost" href="https://wa.me/{SITE['whatsapp']}">WhatsApp</a> <a class="btn ghost" href="{esc(SITE['maps_url'])}" rel="noopener">{u['route']}</a></p></div>
<div><h2>{u['services']}</h2><ul class="flist">{links}</ul>
<p>{blog_link}<a href="{url(lang, ABOUT_SLUG[lang])}">{u['about']}</a></p></div>
</div></section>
<footer class="foot"><div class="wrap">© {date.today().year} {esc(d['name'])} · Batna</div></footer>
<a class="wa" href="https://wa.me/{SITE['whatsapp']}" aria-label="WhatsApp"><svg viewBox="0 0 24 24" width="28" height="28" fill="#fff"><path d="M12 2a10 10 0 00-8.6 15.1L2 22l5-1.3A10 10 0 1012 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-3.3-.8-2.8-1.1-4.5-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6-.3.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.7-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.2z"/></svg></a>
</body></html>"""

def icon(name):
    return f'<svg class="ico" viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

def hero(lang, h1, intro, crumbs=None, svc=None):
    u = UI[lang]
    bc = ""
    if crumbs:
        bc = '<nav class="crumbs" aria-label="breadcrumb">' + " / ".join(
            f'<a href="{href}">{esc(t)}</a>' if href else f"<span>{esc(t)}</span>" for t, href in crumbs) + "</nav>"
    return f"""<section class="hero"><div class="wrap">{bc}
<h1>{esc(h1)}</h1><p class="lead">{esc(intro)}</p>
<p class="ctas"><a class="btn" href="{('#devis' if svc in FIELDS else url(lang, QUOTE_SLUG[lang])) if svc else url(lang, QUOTE_SLUG[lang])}">{QL[lang]}</a> <a class="btn ghost light" href="tel:{SITE['phone_intl']}">{u['call']} <span dir="ltr">{SITE['phone_display']}</span></a> <a class="btn ghost light" href="https://wa.me/{SITE['whatsapp']}">WhatsApp</a></p>
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
    body = hero(lang, c["h1"], c["intro"], [(u["home"], url(lang)), (c["title"], None)], svc=s["key"])
    body += f'<p class="wrap note">{u["quote"]}</p>'
    body += f'<section class="wrap sec"><h2>{u["offer"]}</h2><ul class="checks">' + "".join(f"<li>{esc(i)}</li>" for i in c["items"]) + "</ul></section>"
    if c.get("body"): body += f'<section class="wrap sec post">{md(c["body"])}</section>'
    if s["key"] in FIELDS:
        body += f'<section class="wrap sec quote" id="devis"><h2>{QX[lang][2]}</h2><div class="qgrid">{quote_form(lang, s["key"])}<aside class="qside"><ol class="qsteps">' + "".join(f"<li>{esc(x)}</li>" for x in QT[lang]["steps"]) + "</ol></aside></div></section>"
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

AUTHOR = {
    "fr": ("Saidi Walid", "Architecte agréé et expert judiciaire à Batna. Il réalise des missions d'expertise ordonnées par les juridictions de Batna (tribunal, cour, tribunal administratif) en bâtiment et en foncier, et conçoit des projets privés et publics dans la wilaya.", "Voir le profil"),
    "en": ("Saidi Walid", "Licensed architect and court-appointed expert in Batna. He carries out expert assignments ordered by the courts of Batna on buildings and land, and designs private and public projects in the wilaya.", "View profile"),
    "ar": ("سعيدي وليد", "مهندس معماري معتمد وخبير قضائي في باتنة. ينجز مهام الخبرة التي تأمر بها الجهات القضائية بباتنة (المحكمة، المجلس القضائي، المحكمة الإدارية) في مجال البناء والعقار، ويصمم مشاريع خاصة وعمومية في الولاية.", "عرض الملف"),
}
TOC = {"fr": "Sommaire", "en": "Contents", "ar": "محتويات المقال"}

def build_post(p):
    lang, u = p["lang"], UI[p["lang"]]
    sib = {q["lang"]: q for q in POSTS if q["key"] == p["key"]}
    pbl = {l: url(l, BLOG_SLUG[l] + "/" + q["slug"]) for l, q in sib.items()}
    svc = next((s for s in SERVICES if s["key"] == p.get("service")), None)
    link = f'<aside class="box"><a href="{url(lang, svc[lang]["slug"])}">{esc(svc[lang]["title"])} →</a></aside>' if svc else ""
    content = md(p["body"])
    heads = re.findall(r'<h2 id="(s\d+)">(.*?)</h2>', content)
    toc = ""
    if len(heads) >= 3:
        toc = f'<nav class="toc"><b>{TOC[lang]}</b><ol>' + "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in heads) + "</ol></nav>"
    name, bio, cta = AUTHOR[lang]
    author = f'<aside class="author"><img src="/assets/logo.svg" alt="" width="56" height="56"><div><b>{u["by"]} {esc(name)}</b><p>{esc(bio)}</p><a href="{url(lang, ABOUT_SLUG[lang])}">{cta}</a></div></aside>'
    upd = p.get("updated", p["date"])
    body = f"""<article class="wrap post"><nav class="crumbs dark"><a href="{url(lang)}">{u['home']}</a> / <a href="{url(lang, BLOG_SLUG[lang])}">{u['blog']}</a></nav>
<h1>{esc(p['title'])}</h1><p class="meta">{u['by']} <a href="{url(lang, ABOUT_SLUG[lang])}">{esc(name)}</a>{'،' if lang=='ar' else ','} {SITE['i18n'][lang]['tagline'].lower() if lang!='ar' else SITE['i18n'][lang]['tagline']} · {u['updated']} <time datetime="{upd}">{upd}</time></p>
{toc}{content}{link}{author}</article>"""
    same = [q for q in POSTS if q["lang"] == lang and q["key"] != p["key"] and q.get("service") == p.get("service")]
    rest = [q for q in POSTS if q["lang"] == lang and q["key"] != p["key"] and q not in same]
    others = (same + rest)[:3]
    if others: body += f'<section class="wrap sec"><h2>{u["related"]}</h2>{post_cards(lang, others)}</section>'
    full = abs_url(lang, BLOG_SLUG[lang] + "/" + p["slug"])
    art = {"@type": "BlogPosting", "headline": p["title"], "description": p["description"], "datePublished": p["date"], "dateModified": upd,
           "inLanguage": lang, "mainEntityOfPage": full, "author": {"@id": BASE + "/#walid"}, "publisher": {"@id": BASE + "/#business"}, "image": BASE + "/assets/og.png"}
    if svc: art["about"] = {"@type": "Service", "name": svc[lang]["title"], "url": abs_url(lang, svc[lang]["slug"])}
    if p.get("section"): art["articleSection"] = p["section"]
    schema = graph(art, person_schema(lang),
                   crumbs_schema([(u["home"], abs_url(lang)), (u["blog"], abs_url(lang, BLOG_SLUG[lang])), (p["title"], full)]))
    write(pbl, lang, head(lang, p["title"] + " | " + SITE["i18n"][lang]["brand"], p["description"], pbl, schema) + body + foot(lang))

QT = {
    "fr": {"title": "Demande de devis : architecte et expert à Batna | Saidi Walid", "h1": "Demander un devis",
           "intro": "Décrivez votre projet en quelques lignes. Le formulaire prépare votre demande et l'envoie sur WhatsApp au bureau Saidi Walid. Réponse sous 48 h ouvrées en général.",
           "desc": "Demande de devis gratuite au bureau Saidi Walid, architecte agréé et expert à Batna : conception, permis, suivi de chantier, mise en conformité, expertise amiable.",
           "name": "Nom et prénom", "phone": "Téléphone", "service": "Service", "commune": "Commune du projet", "commune_ph": "Batna, Tazoult, Fesdis...",
           "desc_l": "Votre besoin", "desc_ph": "Type de bâtiment, surface, situation du terrain, ce que vous attendez...", "contact": "Je préfère être recontacté par",
           "c_call": "Appel", "c_wa": "WhatsApp", "send": "Envoyer la demande sur WhatsApp", "or": "Ou appelez directement le",
           "choose": "Choisir un service", "other": "Autre demande", "req": "champ obligatoire",
           "judicial": "Expertise judiciaire : l'expert est désigné par le juge et rémunéré par la provision consignée au greffe, il n'y a donc pas de devis. Pour un avis technique hors procédure, choisissez « Expertise amiable et constat ».",
           "privacy": "Vos informations servent uniquement à répondre à votre demande. Rien n'est enregistré sur ce site.",
           "msg": "Bonjour, je souhaite un devis.", "steps": ["Remplissez le formulaire (1 minute)", "WhatsApp s'ouvre avec votre message prêt, il suffit d'envoyer", "Le bureau vous recontacte pour préciser le besoin et chiffrer"]},
    "en": {"title": "Request a quote: architect and expert in Batna | Saidi Walid", "h1": "Request a quote",
           "intro": "Describe your project in a few lines. The form prepares your request and sends it on WhatsApp to Saidi Walid's office. We usually reply within 2 working days.",
           "desc": "Free quote request to Saidi Walid, licensed architect and expert in Batna: design, permits, site supervision, compliance, private building surveys.",
           "name": "Full name", "phone": "Phone", "service": "Service", "commune": "Project location", "commune_ph": "Batna, Tazoult, Fesdis...",
           "desc_l": "Your request", "desc_ph": "Building type, area, plot location, what you expect...", "contact": "I prefer to be contacted by",
           "c_call": "Phone call", "c_wa": "WhatsApp", "send": "Send request on WhatsApp", "or": "Or call directly",
           "choose": "Choose a service", "other": "Other request", "req": "required",
           "judicial": "Court expertise: the expert is appointed by the judge and paid from the advance deposited with the court, so there is no quote. For a technical opinion outside court, choose “Private building survey”.",
           "privacy": "Your information is only used to answer your request. Nothing is stored on this website.",
           "msg": "Hello, I would like a quote.", "steps": ["Fill in the form (1 minute)", "WhatsApp opens with your message ready, just press send", "The office calls you back to clarify and price the work"]},
    "ar": {"title": "طلب عرض سعر: مهندس معماري وخبير في باتنة | سعيدي وليد", "h1": "اطلب عرض سعر",
           "intro": "صفوا مشروعكم في بضعة أسطر. يحضّر النموذج طلبكم ويرسله عبر واتساب إلى مكتب سعيدي وليد. نرد عادة خلال يومي عمل.",
           "desc": "طلب عرض سعر مجاني من مكتب سعيدي وليد، مهندس معماري معتمد وخبير في باتنة: تصميم، رخصة البناء، متابعة الأشغال، تسوية البنايات، خبرة ودية.",
           "name": "الاسم واللقب", "phone": "رقم الهاتف", "service": "الخدمة", "commune": "بلدية المشروع", "commune_ph": "باتنة، تازولت، فسديس...",
           "desc_l": "طلبكم", "desc_ph": "نوع البناية، المساحة، موقع قطعة الأرض، ما تنتظرونه...", "contact": "أفضّل التواصل عبر",
           "c_call": "مكالمة هاتفية", "c_wa": "واتساب", "send": "إرسال الطلب عبر واتساب", "or": "أو اتصلوا مباشرة على",
           "choose": "اختاروا خدمة", "other": "طلب آخر", "req": "حقل إلزامي",
           "judicial": "الخبرة القضائية: يعيّن القاضي الخبير وتُدفع أتعابه من التسبيق المودع بأمانة الضبط، لذلك لا يوجد عرض سعر. للحصول على رأي تقني خارج الدعوى، اختاروا «الخبرة الودية والمعاينة».",
           "privacy": "تُستعمل معلوماتكم فقط للرد على طلبكم. لا يُحفظ أي شيء على هذا الموقع.",
           "msg": "السلام عليكم، أريد عرض سعر.", "steps": ["املؤوا النموذج (دقيقة واحدة)", "يُفتح واتساب ورسالتكم جاهزة، يكفي الضغط على إرسال", "يتصل بكم المكتب لتوضيح الطلب وتحديد السعر"]},
}

from quote_fields import FIELDS
LI = {"fr": 0, "en": 1, "ar": 2}
QX = {"fr": ("Précisions", "Choisir", "Demander un devis pour ce service"), "en": ("Details", "Choose", "Request a quote for this service"), "ar": ("تفاصيل إضافية", "اختيار", "اطلب عرض سعر لهذه الخدمة")}

def quote_form(lang, preset=None):
    t, i = QT[lang], LI[lang]
    opts = "".join(f'<option value="{s["key"]}" data-label="{esc(s[lang]["title"])}"{" selected" if s["key"] == preset else ""}>{esc(s[lang]["title"])}</option>' for s in SERVICES)
    groups = ""
    for key, fields in FIELDS.items():
        inner = ""
        for n, (typ, lab, opt) in enumerate(fields):
            L = esc(lab[i])
            if typ == "select":
                o = "".join(f"<option>{esc(x)}</option>" for x in opt[i])
                inner += f'<label>{L}<select name="x_{key}_{n}" data-q="{L}"><option value="">{QX[lang][1]}</option>{o}</select></label>'
            else:
                extra = ' inputmode="numeric" dir="ltr"' if typ == "number" else ""
                inner += f'<label>{L}<input name="x_{key}_{n}" data-q="{L}"{extra}></label>'
        groups += f'<div class="qgroup" data-svc="{key}"{"" if key == preset else " hidden"}>{inner}</div>'
    labels = json.dumps({"name": t["name"], "phone": t["phone"], "service": t["service"], "commune": t["commune"], "desc": QX[lang][0], "contact": t["contact"], "msg": t["msg"]}, ensure_ascii=False)
    return f"""<form id="qf" class="qform" novalidate>
<label>{t['service']} *<select name="service" required><option value="">{t['choose']}</option>{opts}<option value="other" data-label="{t['other']}">{t['other']}</option></select></label>
<p class="qnote" id="qjud" hidden>{esc(t['judicial'])}</p>
{groups}
<div class="qrow"><label>{t['name']} *<input name="name" required autocomplete="name"></label>
<label>{t['phone']} *<input name="phone" type="tel" required autocomplete="tel" inputmode="tel" dir="ltr"></label></div>
<label>{t['commune']}<input name="commune" placeholder="{esc(t['commune_ph'])}"></label>
<label>{QX[lang][0]}<textarea name="desc" rows="4" placeholder="{esc(t['desc_ph'])}"></textarea></label>
<fieldset><legend>{t['contact']}</legend><label class="inl"><input type="radio" name="contact" value="{t['c_wa']}" checked> {t['c_wa']}</label><label class="inl"><input type="radio" name="contact" value="{t['c_call']}"> {t['c_call']}</label></fieldset>
<p class="qerr" id="qerr" hidden>* {t['req']}</p>
<div class="qbtns"><button class="btn" type="submit" value="wa">{t['send']}</button>{f'<button class="btn ghost" type="submit" value="mail">{ {"fr": "Envoyer par e-mail", "en": "Send by e-mail", "ar": "إرسال عبر البريد الإلكتروني"}[lang] }</button>' if SITE['email'] else ''}</div>
<p class="qsmall">{t['or']} <a href="tel:{SITE['phone_intl']}" dir="ltr">{SITE['phone_display']}</a>. {esc(t['privacy'])}</p>
</form>
<script>
(function(){{var F=document.getElementById('qf'),f=F.elements,L={labels},W='{SITE['whatsapp']}',sel=f.service,j=document.getElementById('qjud'),G=F.querySelectorAll('.qgroup');
var q=new URLSearchParams(location.search).get('service');if(q&&sel.querySelector('option[value="'+q+'"]'))sel.value=q;
function chk(){{j.hidden=sel.value!=='expertise-judiciaire';for(var k=0;k<G.length;k++)G[k].hidden=G[k].getAttribute('data-svc')!==sel.value}}sel.addEventListener('change',chk);chk();
F.addEventListener('submit',function(e){{e.preventDefault();var ok=true;['name','phone','service'].forEach(function(k){{var el=f[k];var v=el.value.trim();el.classList.toggle('bad',!v);if(!v)ok=false}});
document.getElementById('qerr').hidden=ok;if(!ok)return;var o=sel.options[sel.selectedIndex];
var m=[L.msg,'',L.service+' : '+(o.getAttribute('data-label')||o.text)];
var g=F.querySelector('.qgroup[data-svc="'+sel.value+'"]');if(g){{var xs=g.querySelectorAll('[data-q]');for(var k=0;k<xs.length;k++){{var v=xs[k].value.trim();if(v)m.push(xs[k].getAttribute('data-q')+' : '+v)}}}}
if(f.commune.value.trim())m.push(L.commune+' : '+f.commune.value.trim());if(f.desc.value.trim())m.push(L.desc+' : '+f.desc.value.trim());
m.push('');m.push(L.name+' : '+f.name.value.trim());m.push(L.phone+' : '+f.phone.value.trim());m.push(L.contact+' : '+f.contact.value);
var txt=m.join(String.fromCharCode(10)),sb=e.submitter;
if(sb&&sb.value==='mail'){{location.href='mailto:{SITE['email']}?subject='+encodeURIComponent(L.msg+' '+(o.getAttribute('data-label')||o.text))+'&body='+encodeURIComponent(txt);}}
else window.open('https://wa.me/'+W+'?text='+encodeURIComponent(txt),'_blank','noopener');}});}})();
</script>"""

def build_quote(lang):
    t, u = QT[lang], UI[lang]
    pbl = {l: url(l, QUOTE_SLUG[l]) for l in LANGS}
    steps = "".join(f"<li>{esc(x)}</li>" for x in t["steps"])
    body = f"""<section class="hero small"><div class="wrap"><nav class="crumbs" aria-label="breadcrumb"><a href="{url(lang)}">{u['home']}</a> / <span>{t['h1']}</span></nav>
<h1>{t['h1']}</h1><p class="lead">{esc(t['intro'])}</p></div></section>
<section class="wrap sec quote"><div class="qgrid">{quote_form(lang)}
<aside class="qside"><ol class="qsteps">{steps}</ol></aside></div></section>"""
    schema = graph({"@type": "ContactPage", "name": t["h1"], "url": abs_url(lang, QUOTE_SLUG[lang]), "about": {"@id": BASE + "/#business"}, "inLanguage": lang},
                   crumbs_schema([(u["home"], abs_url(lang)), (t["h1"], abs_url(lang, QUOTE_SLUG[lang]))]), org_schema(lang))
    write(pbl, lang, head(lang, t["title"], t["desc"], pbl, schema) + body + foot(lang))

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
    page = head("fr", u["notfound"], u["notfound_txt"], pbl, graph(org_schema("fr")))
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
    shutil.copy(ROOT / "assets/favicon.ico", OUT / "favicon.ico")
    (OUT / "site.webmanifest").write_text(json.dumps({"name": d["name"], "short_name": "Saidi Walid", "icons": [
        {"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}],
        "theme_color": "#14202e", "background_color": "#14202e", "display": "standalone", "start_url": "/"}, ensure_ascii=False), encoding="utf-8")

def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    for lang in LANGS:
        build_home(lang); build_blog(lang); build_about(lang); build_quote(lang)
        for s in SERVICES: build_service(s, lang)
    for p in POSTS: build_post(p)
    build_404(); build_meta_files()
    print(f"OK : {len(set(p for p, _ in SITEMAP))} pages -> {OUT}")

if __name__ == "__main__":
    main()
