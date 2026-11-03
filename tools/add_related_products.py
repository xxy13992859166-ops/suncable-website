"""Add a reciprocal "Related products" block and BreadcrumbList JSON-LD.

Two passes, both idempotent:
  1. Related products: every product page links to the other five; every other
     page gets the same block listing all six. Placed before <footer> on product
     pages (in-content) and before </body> elsewhere.
  2. BreadcrumbList: built from the existing visible <div class="breadcrumb">
     markup so the structured data always matches what the user sees.

Runs from the repository root in GitHub Actions.
"""

import json
import pathlib
import re

ORIGIN = "https://xxy13992859166-ops.github.io"
BASE = "/suncable-website"
HOME = ORIGIN + BASE + "/"
PRODUCTS_INDEX = ORIGIN + BASE + "/products.html"

# slug, link text, one-line blurb (blurbs reuse facts already stated on the pages)
PRODUCTS = [
    (
        "pv1-f-solar-cable",
        "PV1-F Solar Cable",
        "2-core 0.6/1 kV PV cable, red/black, TUV &amp; UL certified, 1\u20136 mm\u00b2.",
    ),
    (
        "h1z2z2-k-solar-cable",
        "H1Z2Z2-K Solar Cable",
        "Single-core 1 kV solar cable to IEC 62930, TUV approved, 1.5\u20136 mm\u00b2.",
    ),
    (
        "mc4-connector",
        "MC4 Solar Connector",
        "Male/female MC4-Evo2 pair, IP68, 1500 V DC, TUV certified.",
    ),
    (
        "solar-cable-storage",
        "Storage Battery DC Cable",
        "LSZH low-smoke DC cable for battery banks, 0.6/1 kV, TUV.",
    ),
    (
        "solar-cable-ac",
        "AC Power Cable 450/750 V",
        "3-core AC cable for inverter output, IEC 60228, IEC &amp; VDE.",
    ),
    (
        "solar-cable-combiner",
        "Solar Combiner Box",
        "6/8/12/16-input PV combiner, IP65, SPD and DC breaker, IEC 61439.",
    ),
]

PRODUCT_SLUGS = {p[0] for p in PRODUCTS}

SKIP = {
    "thankyou.html",
    "wa-auto-dev.html",
    "seo-dashboard.html",
    "bing-submit.html",
    "baidu-submit.html",
    "submit-to-google.html",
    "google17308f79e30f35f7.html",
    "index-original.html",
    "index_fixed.html",
}

CARD = (
    '<a href="' + BASE + '/{slug}.html" style="display:block;border:1px solid #e2e8f0;'
    'border-radius:10px;padding:14px 16px;text-decoration:none;background:#f8fafc">'
    '<strong style="display:block;color:#1a5276;font-size:15px;font-weight:700">{name}</strong>'
    '<span style="display:block;color:#64748b;font-size:13px;line-height:1.5;margin-top:4px">{blurb}</span>'
    "</a>"
)

BLOCK = (
    "<!-- RELATED_PRODUCTS_START -->\n"
    '<section id="related-products" style="max-width:800px;margin:40px auto;padding:0 20px">\n'
    '  <h2 style="font-size:20px;font-weight:700;color:#0d1b2a;margin:0 0 14px">Related products</h2>\n'
    '  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px">\n'
    "    {cards}\n"
    "  </div>\n"
    "</section>\n"
    "<!-- RELATED_PRODUCTS_END -->\n"
)

START = "<!-- RELATED_PRODUCTS_START -->"
END = "<!-- RELATED_PRODUCTS_END -->"


def related_block(slug):
    items = [p for p in PRODUCTS if not (slug and p[0] == slug)]
    cards = "\n    ".join(CARD.format(slug=s, name=n, blurb=b) for s, n, b in items)
    return BLOCK.format(cards=cards)


def strip_tags(text):
    return re.sub(r"<[^>]+>", "", text).strip()


def breadcrumb_jsonld(page_url, crumb_items):
    items = []
    for pos, (name, url) in enumerate(crumb_items, start=1):
        node = {"@type": "ListItem", "position": pos, "name": name}
        if url:
            node["item"] = url
        items.append(node)
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(data, ensure_ascii=False, indent=2)
        + "\n</script>\n"
    )


def resolve(href):
    if href.startswith("http"):
        return href
    if "#" in href:
        frag = href.split("#", 1)[1].split("?")[0]
        if frag in ("products", "product"):
            return PRODUCTS_INDEX
        return ORIGIN + BASE + "/"
    if href.startswith("/"):
        return ORIGIN + href
    return ORIGIN + BASE + "/" + href


def build_crumbs(s):
    """Return [(name, url), ...] from the visible breadcrumb, or None."""
    m = re.search(r'<div class="breadcrumb">(.*?)</div>', s, re.S)
    if not m:
        return None
    inner = m.group(1)
    anchors = re.findall(r'<a href="([^"]*)"[^>]*>(.*?)</a>', inner, re.S)
    if not anchors:
        return None
    crumbs = [(strip_tags(t), resolve(h)) for h, t in anchors]
    tail = inner.rsplit("</a>", 1)[-1]
    tail = strip_tags(tail.replace("&gt;", " ")).strip()
    if tail:
        crumbs.append((tail, None))
    return crumbs if len(crumbs) >= 2 else None


def process(path):
    s = path.read_text(encoding="utf-8")
    orig = s
    slug = path.stem if path.stem in PRODUCT_SLUGS else None

    if START not in s:
        block = related_block(slug)
        # Sit above the site footer so the block stays in the reading flow.
        if "<footer" in s:
            idx = s.rindex("<footer")
            s = s[:idx] + block + "  " + s[idx:]
        elif "</body>" in s:
            idx = s.rindex("</body>")
            s = s[:idx] + block + s[idx:]
        else:
            return "no-anchor", orig

    if '"BreadcrumbList"' not in s:
        crumbs = build_crumbs(s)
        if crumbs:
            page_url = ORIGIN + BASE + "/" + path.name
            for i, (name, url) in enumerate(crumbs):
                if url is None:
                    crumbs[i] = (name, page_url)
            s = s.replace("</head>", breadcrumb_jsonld(page_url, crumbs) + "</head>", 1)

    if s == orig:
        return "unchanged", orig
    path.write_text(s, encoding="utf-8")
    return "updated", s


def main():
    root = pathlib.Path(".")
    files = [p for p in sorted(root.glob("*.html")) if p.name not in SKIP]
    counts = {}
    errors = []
    for p in files:
        try:
            status, _ = process(p)
        except Exception as exc:  # keep going: one bad file must not stop the batch
            errors.append("%s: %s" % (p.name, exc))
            status = "error"
        counts[status] = counts.get(status, 0) + 1
    have_block = have_crumb = 0
    for p in files:
        try:
            s = p.read_text(encoding="utf-8")
        except Exception:
            continue
        have_block += START in s
        have_crumb += '"BreadcrumbList"' in s
    print("files scanned:", len(files))
    print("files with related products:", have_block)
    print("files with BreadcrumbList:", have_crumb)
    for k in sorted(counts):
        print("%s: %d" % (k, counts[k]))
    for e in errors:
        print("ERROR", e)
    missing = [p.name for p in files if START not in p.read_text(encoding="utf-8")]
    if missing:
        print("missing related products:", len(missing))
    for slug in sorted(PRODUCT_SLUGS):
        p = pathlib.Path(slug + ".html")
        if p.exists():
            s = p.read_text(encoding="utf-8")
            ok = START in s and '"BreadcrumbList"' in s
            print("product %-26s block+breadcrumb=%s" % (slug, ok))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
