# -*- coding: utf-8 -*-
"""Batch 3: put the 20+ years credential into the meta descriptions.

Scope:
  * all 56 country hub pages      -> templated description, "20+ years ..." first
  * the 7 country landing pages   -> hand-written description, same opening
  * 16 core supplier pages        -> hand-written description, same opening
  * visible body text and og:description that still say "15+ years" -> "20+ years"

Blog and guide descriptions keep describing the article: an article summary is
what earns the click there, not a company credential.

Idempotent: a second run reports 0 changes.
"""
import re
import sys
import html as H
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
_ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
TARGET = pathlib.Path(_ARGS[0]) if _ARGS else ROOT
DRY = "--apply" not in sys.argv

DESC_MAX = 155

DESC_RE = re.compile(
    r'(<meta[^>]+name=["\']description["\'][^>]+content=)(["\'])(.*?)\2', re.S | re.I
)
HUB_TITLE = re.compile(r"^Solar Cable Supplier for (.+?) \| TUV & UL Certified$")

# Two variants: the long one for short country names, the short one for the rest.
COUNTRY_DESC = [
    "20+ years of TUV & UL certified PV1-F and H1Z2Z2-K solar cable. Factory-direct pricing "
    "for {c}. IEC 62930, export documents, 2-hour quotes.",
    "20+ years of TUV & UL certified PV cable. Factory-direct pricing for {c}. IEC 62930, "
    "export documents, 2-hour quotes.",
]

OVR = {
    "index.html": "20+ years making TUV & UL certified PV1-F and H1Z2Z2-K solar cable, MC4 "
                  "connectors and storage cable. Factory-direct, 50+ export markets.",
    "about.html": "20+ years making TUV & UL certified PV cable and MC4 connectors in China: "
                  "PV1-F, H1Z2Z2-K, storage and AC cable, exported to 50+ countries.",
    "products.html": "20+ years of TUV & UL certified solar PV cable: PV1-F 4/6/10mm2, "
                     "H1Z2Z2-K, MC4 connectors. Factory-direct pricing, 25-year warranty.",
    "solar-cable-contact.html": "20+ years of solar cable manufacturing. Talk to JunlinChicheng "
                                "for quotes and technical support. WhatsApp +86 153 3900 5193, "
                                "reply within 2 hours.",
    "solar-cable-request-quote.html": "20+ years of TUV & UL certified solar cable. Free quote "
                                      "for PV1-F, H1Z2Z2-K and MC4 \u2014 send your spec, get a "
                                      "reply in 2 hours on WhatsApp.",
    "solar-cable-sample-order.html": "20+ years of TUV & UL certified solar cable. Request free "
                                     "PV1-F and H1Z2Z2-K samples to test before ordering in bulk.",
    "solar-cable-distributor.html": "20+ years of solar cable manufacturing. Become an authorised "
                                    "distributor: wholesale pricing, TUV & UL certified PV cable, "
                                    "MC4 and marketing support.",
    "solar-cable-exporter-china.html": "20+ years of solar cable manufacturing in China: TUV & UL "
                                       "certified PV1-F, H1Z2Z2-K and MC4, factory-direct "
                                       "pricing, 50+ export markets.",
    "solar-cable-exporter-africa.html": "20+ years of TUV & UL certified PV cable supplied to "
                                        "South Africa, Nigeria, Kenya, Ghana and 50+ African "
                                        "countries. Factory-direct pricing.",
    "solar-cable-certification-guide.html": "20+ years of solar cable certification work: TUV "
                                            "Rheinland, UL Listed, CE, SABS (South Africa), "
                                            "SONCAP (Nigeria) and KEBS (Kenya), explained.",
    "solar-cable-lead-time.html": "20+ years of solar cable manufacturing. Production lead times "
                                  "and worldwide shipping: standard orders ship in 7-15 days, "
                                  "express for urgent projects.",
    "faq.html": "20+ years of PV cable manufacturing. Answers on specs, TUV/UL certification, "
                "lead times and custom manufacturing from the JunlinChicheng team.",
    "solar-cable-price-list.html": "20+ years of factory-direct solar cable pricing. 2026 "
                                   "wholesale list for PV1-F, H1Z2Z2-K and MC4 connectors. Free "
                                   "quotation within 2 hours.",
    "solar-cable-price-list-2026.html": "20+ years of factory-direct pricing: 2026 solar cable "
                                        "price guide for PV1-F 2x2.5 mm\u00b2, H1Z2Z2-K 6 mm\u00b2 "
                                        "and MC4. Request a quote.",
    "solar-cable-price-comparison-by-country.html": "Compare solar cable prices by country, from "
                                                    "a manufacturer with 20+ years in TUV/UL "
                                                    "certified PV cable. See how Chinese cable "
                                                    "compares with EU brands.",
    "solar-cable-faq.html": "20+ years of solar cable manufacturing. FAQ on PV1-F vs H1Z2Z2-K, "
                            "certifications, pricing and ordering from JunlinChicheng.",
    "solar-cable-for-kenya.html": "20+ years of TUV & UL certified PV cable for Kenyan projects: "
                                  "PV1-F, H1Z2Z2-K and MC4, supplied to Nairobi and across Kenya.",
    "solar-cable-for-nigeria.html": "20+ years of TUV & UL certified PV cable, MC4 and storage DC "
                                    "shipped to Lagos, Abuja and Port Harcourt. Factory-direct "
                                    "from China.",
    "solar-cable-for-saudi-arabia.html": "20+ years of TUV & UL certified PV cable for Saudi "
                                         "projects: PV1-F, H1Z2Z2-K and MC4 for KSA utility and "
                                         "rooftop solar.",
    "solar-cable-for-south-africa.html": "20+ years of TUV & UL certified PV1-F, H1Z2Z2-K and "
                                         "MC4 supplied to EPCs and distributors across South "
                                         "Africa.",
    "solar-cable-for-uae.html": "20+ years of TUV & UL certified PV cable for UAE projects: PV1-F, "
                                "MC4, mounting rails and combiner boxes for Dubai and Abu Dhabi.",
    "solar-cable-for-india.html": "20+ years of TUV & UL certified PV cable for Indian projects: "
                                  "PV1-F, H1Z2Z2-K and MC4, factory-direct from China.",
    "solar-cable-manufacturer-india.html": "20+ years of solar PV cable manufacturing: PV1-F and "
                                           "H1Z2Z2-K supplied to Indian EPCs, TUV and UL "
                                           "certified, factory-direct.",
}

stats = {"country_desc": 0, "override_desc": 0, "years_bumped": 0, "files_written": 0}
problems = []


def set_desc(s, new):
    m = DESC_RE.search(s)
    if not m:
        return s, False
    quote, body = m.group(2), m.group(3)
    if H.unescape(body).strip() == new:
        return s, False
    if quote in new:
        problems.append(("quote-in-desc", "", len(new), new[:50]))
        return s, False
    return s[:m.start(3)] + new + s[m.end(3):], True


for p in sorted(TARGET.glob("*.html")):
    s = p.read_text(encoding="utf-8")
    orig = s
    name = p.name

    m = re.search(r"<title>(.*?)</title>", s, re.S | re.I)
    title = H.unescape(m.group(1).strip()) if m else ""

    if name in OVR:
        s, ch = set_desc(s, OVR[name])
        stats["override_desc"] += ch
    else:
        hub = HUB_TITLE.match(title)
        if hub:
            c = hub.group(1)
            fits = [v for v in COUNTRY_DESC if len(v.format(c=c)) <= DESC_MAX]
            if not fits:
                problems.append(("no-variant-fits", name, len(c), c))
            else:
                s, ch = set_desc(s, fits[0].format(c=c))
                stats["country_desc"] += ch

    # visible copy and og:description that still understate the age claim
    n = s.count("15+ years")
    if n:
        s = s.replace("15+ years", "20+ years")
        stats["years_bumped"] += n

    if s != orig:
        stats["files_written"] += 1
        if not DRY:
            p.write_text(s, encoding="utf-8")

    md = DESC_RE.search(s)
    if md:
        d = H.unescape(md.group(3).strip())
        if len(d) > DESC_MAX:
            problems.append(("desc-over", name, len(d), d[:60]))
        if name in OVR and "20+ years" not in d:
            problems.append(("missing-20", name, len(d), d[:60]))

print("mode:", "DRY-RUN" if DRY else "APPLY")
for k, v in stats.items():
    print("  %-16s %d" % (k, v))
print("  desc over %d     %d" % (DESC_MAX, sum(1 for x in problems if x[0] == "desc-over")))
print("  missing 20+      %d" % sum(1 for x in problems if x[0] == "missing-20"))
for kind, name, ln, val in problems[:20]:
    print("   %-16s %-42s %3d  %s" % (kind, name, ln, val))
