"""Daily SEO batch for suncable-website (2026-11-04).

Four changes, each idempotent and counted:
  1. Fix the broken nav link: /suncable-website/contact.html -> solar-cable-contact.html
     (the file never existed; 74 pages linked to a 404 on the main CTA)
  2. Add a self-referencing canonical to content pages that have none
  3. Generate site-map.html listing every page (fixes 78 orphan pages with no
     inbound internal links) and link it from the footer on every page
  4. Register site-map.html in sitemap.xml

Runs from the repository root. Read-modify-write, UTF-8, LF preserved.
"""

import html
import pathlib
import re
from collections import Counter

ORIGIN = "https://xxy13992859166-ops.github.io"
BASE = "/suncable-website"
CONTACT = BASE + "/solar-cable-contact.html"
SITEMAP_PAGE = "site-map.html"

UTILITY = {
    "thankyou.html", "seo-dashboard.html", "wa-auto-dev.html",
    "bing-submit.html", "baidu-submit.html", "submit-to-google.html",
    "bing-submit-guide.html", "bing-verify-guide.html", "gsc-bing-guide.html",
    "indexing-guide.html", "google17308f79e30f35f7.html",
}

PRODUCTS = [
    "pv1-f-solar-cable.html", "h1z2z2-k-solar-cable.html", "mc4-connector.html",
    "solar-cable-storage.html", "solar-cable-ac.html", "solar-cable-combiner.html",
    "products.html", "solar-cable-price-list.html", "solar-cable-price-list-2026.html",
    "solar-cable-distributor.html", "solar-cable-request-quote.html",
    "solar-cable-sample-order.html", "solar-cable-lead-time.html",
    "solar-cable-price-comparison-by-country.html",
]

stats = Counter()


def read(p):
    return p.read_text(encoding="utf-8", errors="replace")


def write(p, s):
    p.write_text(s, encoding="utf-8", newline="")


def fix_contact(s):
    new, n = re.subn(r'href="/suncable-website/contact\.html"',
                     'href="' + CONTACT + '"', s)
    return new, n


def add_canonical(s, name):
    if re.search(r'<link[^>]+rel=["\']canonical["\']', s, re.I):
        return s, 0
    tag = '<link rel="canonical" href="%s%s/%s">\n' % (ORIGIN, BASE, name)
    if "</head>" not in s:
        return s, 0
    return s.replace("</head>", tag + "</head>", 1), 1


def add_footer_link(s):
    if SITEMAP_PAGE in s:
        return s, 0
    m = re.search(r'(<div class="footer-links">.*?)(\n\s*</div>)', s, re.S)
    if not m:
        # Second footer template: column layout with a Resources list.
        m2 = re.search(r'(<h4>Resources</h4><ul>.*?)(</ul>)', s, re.S)
        if not m2:
            return s, 0
        link = '<li><a href="%s/%s">Site Map</a></li>' % (BASE, SITEMAP_PAGE)
        return s[:m2.end(1)] + link + s[m2.end(1):], 1
    link = '\n                <a href="%s/%s">Site Map</a>' % (BASE, SITEMAP_PAGE)
    return s[:m.end(1)] + link + s[m.end(1):], 1


def page_title(s):
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    t = re.sub(r"\s+", " ", html.unescape(m.group(1))).strip() if m else ""
    return t.split("|")[0].strip() or t


def classify(name):
    if name in PRODUCTS:
        return "Products & pricing"
    if name.startswith("blog"):
        return "Blog articles"
    if re.match(r"^solar-cable-(for|manufacturer)-", name) or re.match(
            r"^(?!solar|blog|how|import|pv|about|contact|faq|index|products|site)[a-z_]+\.html$", name):
        return "Country markets"
    if name in ("about.html", "faq.html", "solar-cable-contact.html", "solar-cable-faq.html",
                "solar-cable-faq-extended.html", "solar-cable-case-studies.html"):
        return "Company & support"
    return "Guides & resources"


def build_sitemap_page(root):
    pages = [p for p in sorted(root.glob("*.html"))
             if p.name not in UTILITY and p.name != SITEMAP_PAGE and p.name != "index.html"]
    groups = {}
    for p in pages:
        title = page_title(read(p))
        groups.setdefault(classify(p.name), []).append((title, p.name))
    order = ["Products & pricing", "Country markets", "Guides & resources",
             "Blog articles", "Company & support"]
    for g in groups:
        groups[g].sort()
    blocks = []
    for g in order:
        if g not in groups:
            continue
        items = "\n".join(
            '        <li><a href="%s/%s">%s</a></li>' % (BASE, n, html.escape(t))
            for t, n in groups[g])
        blocks.append('    <h2>%s <span class="n">%d</span></h2>\n    <ul>\n%s\n    </ul>'
                      % (g, len(groups[g]), items))
    total = sum(len(v) for v in groups.values())
    body = "\n".join(blocks)
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Site Map | All Solar Cable Pages &amp; Guides</title>
<meta name="description" content="Index of every page on this site: solar cable products, country supply pages, installation guides and blog articles.">
<link rel="canonical" href="{origin}{base}/{page}">
<meta name="robots" content="index, follow">
<style>
  body{{margin:0;font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:#0d1b2a;background:#fff;line-height:1.6}}
  .wrap{{max-width:960px;margin:0 auto;padding:40px 20px 60px}}
  h1{{font-size:28px;margin:0 0 8px}}
  .sub{{color:#64748b;margin:0 0 32px;font-size:15px}}
  h2{{font-size:17px;margin:32px 0 10px;padding-bottom:6px;border-bottom:1px solid #e2e8f0}}
  h2 .n{{color:#94a3b8;font-weight:400;font-size:14px}}
  ul{{list-style:none;padding:0;margin:0;columns:2;column-gap:32px}}
  li{{margin:0 0 7px;break-inside:avoid;font-size:14.5px}}
  a{{color:#1a5276;text-decoration:none}}
  a:hover{{text-decoration:underline}}
  @media(max-width:640px){{ul{{columns:1}}}}
  footer{{margin-top:48px;padding-top:20px;border-top:1px solid #e2e8f0;color:#64748b;font-size:13px}}
  footer a{{margin-right:14px;color:#64748b}}
</style>
</head>
<body>
<div class="wrap">
  <h1>Site Map</h1>
  <p class="sub">Every page on this site — {total} pages in {ngroups} groups.</p>
{body}
  <footer>
    <a href="{base}/">Home</a>
    <a href="{base}/products.html">Products</a>
    <a href="{base}/blog.html">Blog</a>
    <a href="{base}/solar-cable-contact.html">Contact</a>
    <p>JunlinChicheng Metal Products Group Co., Ltd.</p>
  </footer>
</div>
</body>
</html>
""".format(origin=ORIGIN, base=BASE, page=SITEMAP_PAGE, total=total,
           ngroups=len(groups), body=body)


def main():
    root = pathlib.Path(".")
    files = sorted(root.glob("*.html"))

    for p in files:
        s = orig = read(p)
        if p.name != SITEMAP_PAGE:
            s, n = fix_contact(s)
            stats["contact_links_fixed"] += n
        if p.name not in UTILITY and p.name != SITEMAP_PAGE:
            s, n = add_canonical(s, p.name)
            stats["canonical_added"] += n
            s, n = add_footer_link(s)
            stats["footer_links_added"] += n
        if s != orig:
            write(p, s)
            stats["files_written"] += 1

    sm_page = root / SITEMAP_PAGE
    content = build_sitemap_page(root)
    if not sm_page.exists() or read(sm_page) != content:
        write(sm_page, content)
        stats["sitemap_page_written"] = 1

    sm = root / "sitemap.xml"
    if sm.exists():
        s = read(sm)
        loc = "%s%s/%s" % (ORIGIN, BASE, SITEMAP_PAGE)
        if loc not in s:
            block = ("  <url>\n    <loc>%s</loc>\n    <changefreq>weekly</changefreq>\n"
                     "    <priority>0.3</priority>\n  </url>\n") % loc
            s = s.replace("</urlset>", block + "</urlset>", 1)
            write(sm, s)
            stats["sitemap_entry_added"] = 1

    for k in sorted(stats):
        print("%-22s %d" % (k, stats[k]))
    print("pages with contact link to solar-cable-contact:",
          sum(1 for p in files if 'href="' + CONTACT + '"' in read(p)))
    print("pages linking site-map:", sum(1 for p in files if SITEMAP_PAGE in read(p)))
    print("pages with canonical:", sum(1 for p in files if re.search(r'rel=["\']canonical', read(p), re.I)))


if __name__ == "__main__":
    main()
