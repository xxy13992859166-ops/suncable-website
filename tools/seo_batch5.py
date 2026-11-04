# -*- coding: utf-8 -*-
"""Batch 5: social cards, breadcrumbs, and the Export Markets page.

 1. og:image pointed three pages at images/h1z2z2k.jpg, which is a 404. The file
    on disk is images/h1zz2.jpg. Repoint them.
 2. Eight pages had no Open Graph block at all, so a LinkedIn or WhatsApp share
    of them produced no preview card.
 3. 79 pages had og: tags but no twitter:card.
 4. 48 pages had no BreadcrumbList. Build one from the page's real parent:
    product pages under products.html, articles under blog.html, country pages
    under export-markets.html, everything else straight off Home.
 5. Register export-markets.html in sitemap.xml and site-map.html.

Idempotent: a second run reports 0 changes.
"""
import pathlib
import re
import sys
import html as H

ROOT = pathlib.Path(__file__).resolve().parent.parent
_ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
TARGET = pathlib.Path(_ARGS[0]) if _ARGS else ROOT
DRY = "--apply" not in sys.argv

BASE = "https://xxy13992859166-ops.github.io/suncable-website/"
IMG = BASE + "images/pv1f.jpg"

PRODUCTS = {"pv1-f-solar-cable.html", "h1z2z2-k-solar-cable.html", "mc4-connector.html",
            "solar-cable-storage.html", "solar-cable-ac.html", "solar-cable-combiner.html"}
COUNTRIES = {"kenya.html", "nigeria.html", "saudiarabia.html", "southafrica.html",
             "uae.html", "india.html", "australia.html"}

stats = {"og_image_fixed": 0, "og_block_added": 0, "twitter_added": 0,
         "breadcrumb_added": 0, "sitemap_added": 0, "files_written": 0}
problems = []


def esc(t):
    return H.escape(t, quote=False).replace('"', "&quot;")


def meta(s, key):
    m = re.search(r'<meta[^>]+name=["\']%s["\'][^>]+content=["\'](.*?)["\']' % key, s, re.S | re.I)
    if not m:
        m = re.search(r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']%s["\']' % key, s, re.S | re.I)
    return H.unescape(m.group(1)).strip() if m else ""


def h1_of(s):
    m = re.search(r"(?is)<h1[^>]*>(.*?)</h1>", s)
    if not m:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()


def crumb_items(name, page_name, title, h1):
    items = [("Home", BASE)]
    parent = None
    if page_name in PRODUCTS:
        parent = ("Products", BASE + "products.html")
    elif page_name.startswith("blog-"):
        parent = ("Blog", BASE + "blog.html")
    elif page_name in COUNTRIES:
        parent = ("Export Markets", BASE + "export-markets.html")
    if parent:
        items.append(parent)
    label = h1 or title.split("|")[0].strip() or page_name.replace(".html", "")
    items.append((label, BASE + page_name))
    return items


for p in sorted(TARGET.glob("*.html")):
    s = p.read_text(encoding="utf-8")
    orig = s
    name = p.name
    if name.startswith("google"):      # verification file: byte-identical, never touch
        continue
    # retired / operations pages are noindex on purpose: social cards and
    # breadcrumbs there buy nothing, and every write is one more thing to review.
    rb = re.search(r'name=["\']robots["\'][^>]+content=["\']([^"\']+)', s, re.I)
    if rb and "noindex" in rb.group(1).lower():
        continue

    # 1. og:image pointing at the wrong file name
    if "images/h1z2z2k.jpg" in s:
        s = s.replace("images/h1z2z2k.jpg", "images/h1zz2.jpg")
        stats["og_image_fixed"] += 1

    title = re.search(r"<title>(.*?)</title>", s, re.S | re.I)
    title = H.unescape(title.group(1)).strip() if title else ""
    desc = meta(s, "description")
    canon = re.search(r'rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', s, re.I)
    canon = canon.group(1) if canon else BASE + name

    # 2. no Open Graph block at all
    if 'property="og:title"' not in s and '<meta name="description"' in s:
        img = BASE + ("images/logo.jpg" if name == "site-map.html" else "images/pv1f.jpg")
        block = (
            '\n<meta property="og:type" content="website">'
            '\n<meta property="og:site_name" content="JunlinChicheng Solar Cable">'
            '\n<meta property="og:title" content="%s">'
            '\n<meta property="og:description" content="%s">'
            '\n<meta property="og:url" content="%s">'
            '\n<meta property="og:image" content="%s">'
            '\n<meta property="og:image:width" content="500">'
            '\n<meta property="og:image:height" content="500">'
            '\n<meta name="twitter:card" content="summary_large_image">'
        ) % (esc(title), esc(desc), esc(canon), img)
        m = re.search(r'<meta name="description"[^>]*>', s)
        s = s[:m.end()] + block + s[m.end():]
        stats["og_block_added"] += 1

    # 3. og present but no twitter:card
    elif 'name="twitter:card"' not in s:
        last = None
        for m in re.finditer(r'<meta property="og:[^>]+>', s):
            last = m
        if last:
            s = s[:last.end()] + '\n<meta name="twitter:card" content="summary_large_image">' + s[last.end():]
            stats["twitter_added"] += 1

    # 4. breadcrumbs
    if "BreadcrumbList" not in s:
        items = crumb_items(name, name, title, h1_of(s))
        rows = []
        for i, (label, url) in enumerate(items, 1):
            rows.append('    {\n      "@type": "ListItem",\n      "position": %d,\n'
                        '      "name": "%s",\n      "item": "%s"\n    }' % (i, esc(label), url))
        ld = (' <!-- BREADCRUMB_LD_START -->\n<script type="application/ld+json">\n{\n'
              '  "@context": "https://schema.org",\n  "@type": "BreadcrumbList",\n'
              '  "itemListElement": [\n%s\n  ]\n}\n</script>\n<!-- BREADCRUMB_LD_END -->\n'
              % ",\n".join(rows))
        m = re.search(r"</head>", s, re.I)
        if m:
            s = s[:m.start()] + ld + s[m.start():]
            stats["breadcrumb_added"] += 1
        else:
            problems.append(("no-head", name, 0, ""))

    if s != orig:
        stats["files_written"] += 1
        if not DRY:
            p.write_text(s, encoding="utf-8")

# 5. sitemap + site map page
sm_path = TARGET / "sitemap.xml"
sm = sm_path.read_text(encoding="utf-8")
if "export-markets.html" not in sm:
    block = ('\n  <url>\n    <loc>%sexport-markets.html</loc>\n'
             '    <lastmod>2026-11-04</lastmod>\n    <changefreq>monthly</changefreq>\n'
             '    <priority>0.8</priority>\n  </url>' % BASE)
    sm = sm.replace("\n</urlset>", block + "\n</urlset>")
    stats["sitemap_added"] = 1
    if not DRY:
        sm_path.write_text(sm, encoding="utf-8")

sm_html = TARGET / "site-map.html"
h = sm_html.read_text(encoding="utf-8")
if "export-markets.html" not in h:
    m = re.search(r'(Country markets <span class="n">\d+</span></h2>\s*<ul>\s*)', h)
    if m:
        h = h[:m.end()] + ('<li><a href="/suncable-website/export-markets.html">'
                           'Solar Cable Export Markets &amp; Standards by Country</a></li>\n        '
                           ) + h[m.end():]
        h = re.sub(r'(Country markets <span class="n">)(\d+)(</span>)',
                   lambda x: x.group(1) + str(int(x.group(2)) + 1) + x.group(3), h)
        if not DRY:
            sm_html.write_text(h, encoding="utf-8")

print("mode:", "DRY-RUN" if DRY else "APPLY")
for k, v in stats.items():
    print("  %-18s %d" % (k, v))
for k, n, ln, _ in problems[:10]:
    print("   problem", k, n, ln)
