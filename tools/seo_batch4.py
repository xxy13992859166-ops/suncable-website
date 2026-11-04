# -*- coding: utf-8 -*-
"""Batch 4: stop telling Google to index pages that should not rank.

Three problems, one pass:

 1. Canonical bug   - four pages carry a canonical of
                      ".../$(path.basename('x.html').replace('x','new'))", an
                      unexpanded shell template. That URL does not exist, so the
                      page is pointed at a 404. Reset to the page's own URL.
 2. Sitemap clutter - eleven operations pages are listed in sitemap.xml. Nine of
                      them already say noindex; three say nothing and therefore do
                      get indexed. Drop all eleven from the sitemap and make sure
                      every one of them is noindex, follow.
 3. Doorway risk    - the country hub pages are one page with the country name
                      swapped: pairwise 5-gram Jaccard 0.70-0.73 over 1,596 page
                      pairs, 128 identical DOM lines each. Keep the seven markets
                      that have real supporting content elsewhere on the site and
                      take the rest out of the index. The pages stay live and keep
                      their links; only indexation changes, so this is reversible.

Idempotent: a second run reports 0 changes.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
_ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
TARGET = pathlib.Path(_ARGS[0]) if _ARGS else ROOT
DRY = "--apply" not in sys.argv

BASE = "https://xxy13992859166-ops.github.io/suncable-website/"

# country hubs that have a dedicated landing page and/or article behind them
KEEP_COUNTRY = {
    "kenya.html",          # solar-cable-for-kenya.html
    "nigeria.html",        # solar-cable-for-nigeria.html
    "saudiarabia.html",    # solar-cable-for-saudi-arabia.html
    "southafrica.html",    # solar-cable-for-south-africa.html + africa case study
    "uae.html",            # solar-cable-for-uae.html + solar-cable-supplier-middle-east.html
    "india.html",          # solar-cable-for-india.html + solar-cable-manufacturer-india.html
    "australia.html",      # blog-solar-cable-australia.html
}

UTIL = {
    "baidu-submit.html",
    "bing-submit.html",
    "bing-submit-guide.html",
    "bing-verify-guide.html",
    "gsc-bing-guide.html",
    "indexing-guide.html",
    "seo-dashboard.html",
    "submit-to-google.html",
    "thankyou.html",
    "wa-auto-dev.html",
    "google17308f79e30f35f7.html",
}

# Thinner twin of a page that already owns the same intent. Each pair was checked
# for inbound links and word count before being listed here.
CONSOLIDATE = {
    # 361 / 435 words vs faq.html at 596 words and 115 inbound links
    "solar-cable-faq-extended.html": "faq.html",
    "solar-cable-faq.html": "faq.html",
    # 239 words vs solar-cable-price-list.html at 72 inbound links;
    # the 2026 price angle is already covered by blog-solar-cable-price-guide-2026 (502 w)
    "solar-cable-price-list-2026.html": "solar-cable-price-list.html",
    # 263-word stub against two installation articles at 785 and 853 words
    "solar-cable-installation-guide.html": "blog-solar-cable-installation.html",
}

CANON_BUG = re.compile(r'href="[^"]*\$\(path\.basename\([^")]*\)[^"]*"')
ROBOTS = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]*>', re.I)
TITLE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
HUB_TITLE = re.compile(r"^Solar Cable Supplier for (.+?) \| TUV & UL Certified$")

stats = {"canonical_fixed": 0, "util_noindex": 0, "hub_noindex": 0,
         "consolidated": 0, "sitemap_removed": 0, "files_written": 0}
retired = []
problems = []


def set_robots(s, value):
    m = ROBOTS.search(s)
    if m:
        if 'content="%s"' % value in m.group(0) or "content='%s'" % value in m.group(0):
            return s, False
        return s[:m.start()] + '<meta name="robots" content="%s">' % value + s[m.end():], True
    # page has no robots tag: put one right after <head>
    mh = re.search(r"<head[^>]*>", s, re.I)
    if not mh:
        problems.append(("no-head", "", 0, ""))
        return s, False
    return s[:mh.end()] + '\n<meta name="robots" content="%s">' % value + s[mh.end():], True


for p in sorted(TARGET.glob("*.html")):
    s = p.read_text(encoding="utf-8")
    orig = s
    name = p.name

    # 1. canonical written by an unexpanded shell template
    if CANON_BUG.search(s):
        s = CANON_BUG.sub('href="%s%s"' % (BASE, name), s)
        stats["canonical_fixed"] += 1

    # 2. operations pages
    if name in CONSOLIDATE:
        s, ch = set_robots(s, "noindex, follow")
        stats["consolidated"] += ch
    elif name in UTIL:
        s, ch = set_robots(s, "noindex, follow")
        stats["util_noindex"] += ch

    # 3. country hubs without supporting content
    elif name not in KEEP_COUNTRY:
        m = TITLE.search(s)
        if m and HUB_TITLE.match(re.sub(r"\s+", " ", m.group(1)).strip()):
            s, ch = set_robots(s, "noindex, follow")
            stats["hub_noindex"] += ch
            retired.append(name)

    if s != orig:
        stats["files_written"] += 1
        if not DRY:
            p.write_text(s, encoding="utf-8")

# 4. sitemap: drop utility pages and retired hubs
drop = set(UTIL) | set(CONSOLIDATE) | set(retired)
sm_path = TARGET / "sitemap.xml"
sm = sm_path.read_text(encoding="utf-8")


def keep(block):
    m = re.search(r"<loc>(.*?)</loc>", block)
    if not m:
        return True
    leaf = m.group(1).rstrip("/").split("/")[-1]
    return leaf not in drop and leaf + ".html" not in drop


blocks = re.findall(r"\s*<url>.*?</url>", sm, re.S)
head = sm[:sm.find("<url>")]
tail = "\n</urlset>\n"
kept = [b for b in blocks if keep(b)]
removed = len(blocks) - len(kept)
if removed:
    new_sm = head.rstrip() + "\n" + "".join(kept) + tail
    stats["sitemap_removed"] = removed
    if not DRY:
        sm_path.write_text(new_sm, encoding="utf-8")

print("mode:", "DRY-RUN" if DRY else "APPLY")
for k, v in stats.items():
    print("  %-16s %d" % (k, v))
print("  retired hubs     %d" % len(retired))
print("  sitemap locs now %d" % len(kept))
for k, n, ln, _ in problems[:10]:
    print("   problem", k, n, ln)
