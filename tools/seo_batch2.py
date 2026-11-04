# -*- coding: utf-8 -*-
"""Batch 2 SEO rewriter: title / description length + duplicate H1 + index footer site-map link.

Rules applied (all derive from text already present on the site; no new claims):
 1. Country hub pages  -> title loses the redundant "PV Cable Exporter" tail.
 2. Country hub descs  -> replaced with a compact template built from the same facts.
 3. Blog boilerplate   -> the long "Expert guide from ..." tail is shortened.
 4. Explicit overrides -> hand-written for the pages the rules above cannot fit.
 5. Duplicate H1       -> the 6 thin country landing pages get product-specific H1s.
 6. index.html         -> footer gets the same Site Map link the other 152 pages have.

Idempotent: running twice reports 0 changes.
"""
import re
import sys
import html as H
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
_ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
TARGET = pathlib.Path(_ARGS[0]) if _ARGS else ROOT
DRY = "--apply" not in sys.argv

TITLE_MAX = 60
DESC_MAX = 155

BRAND_TAIL = re.compile(r"\s*[|\u2013\u2014-]\s*JunlinChicheng[^|]*$", re.I)
COUNTRY_TITLE = re.compile(r"^Solar Cable Supplier for (.+?) \| TUV & UL Certified PV Cable Exporter(?:$|\s)")
COUNTRY_DESC = re.compile(
    r"^JunlinChicheng Metal Products Group Co\., Ltd\. is a leading (.+?) solar cable supplier "
    r"and exporter\..*$"
)
BLOG_TAIL = re.compile(
    r"\.\s*Expert guide from JunlinChicheng \u2014 TUV & UL certified PV cable manufacturer\. "
    r"Download free specs and request a quote today\.$"
)

BLOG_TAIL_NEW = ". TUV & UL certified PV cable maker \u2014 free specs on request."

# --- explicit overrides: page -> (title, description or None) ---
OVR = {
    "about.html": ("About JunlinChicheng | TUV & UL Solar Cable Maker",
                   "TUV & UL certified PV cable and MC4 connector manufacturer in China. PV1-F, "
                   "H1Z2Z2-K, storage and AC cable, exported to 50+ countries."),
    "index.html": ("PV Cable Manufacturer | TUV & UL Certified Solar Cable",
                   "TUV & UL certified manufacturer of PV1-F and H1Z2Z2-K solar cable, MC4 "
                   "connectors and storage cable. Factory-direct, 50+ export markets."),
    "blog.html": ("Solar Cable Blog: PV Installation & Price Guides", None),
    "blog-how-to-import-solar-cables-from-china.html": (
        "How to Import Solar Cables from China (2026 Guide)", None),
    "blog-mc4-connector-selection-guide.html": (
        "MC4 Connector Selection Guide: Choosing Solar Connectors",
        "How to choose the right MC4 connector for a PV array: current rating, IP68 sealing, "
        "1500 V DC compatibility and crimping quality. TUV certified."),
    "blog-pv-cable-selection-guide.html": (
        "PV Cable Selection Guide 2025: Choosing Solar DC Cable",
        "PV cable selection guide 2025: PV1-F vs H1Z2Z2-K, wire sizing, MC4 matching and "
        "TUV/UL certification. Free expert advice from JunlinChicheng."),
    "blog-pv-cable-testing-certification.html": (
        "PV Cable Testing & Certification: IEC 62930 vs TUV vs UL",
        "PV cable testing and certification explained: IEC 62930, TUV and UL 4703 test regimes, "
        "what each mark covers and what to ask a supplier."),
    "blog-pv-cable-vs-electrical-cable.html": (
        "PV Cable vs Electrical Cable: Why It Matters",
        "Can you use regular electrical cable for solar panels? The key differences in "
        "insulation, UV rating and warranty, and why PV cable is required."),
    "blog-solar-cable-case-study-africa.html": (
        "Solar Cable Case Study: 50MW South Africa Project", None),
    "blog-solar-cable-fault-diagnosis.html": (
        "Solar Cable Fault Diagnosis: 7 Common Problems",
        "Seven common PV cable faults and how to prevent them: hot spots, water ingress, UV "
        "cracking, rodent damage and connector failures."),
    "blog-solar-cable-for-agricultural-solar.html": (
        "Solar Cable for Agri-PV Projects: Wiring Solutions",
        "Wiring agrivoltaic and agricultural solar projects: cable routing around irrigation, "
        "rodent protection, UV exposure and connector choice."),
    "blog-solar-cable-for-commercial-project.html": (
        "Solar Cable for Commercial Projects: Procurement Guide",
        "Sizing, standards and procurement for commercial rooftop PV: cable schedule, voltage "
        "drop, certification and lead time. TUV & UL certified manufacturer."),
    "blog-solar-cable-for-contractors.html": (
        "Solar Cable for Contractors: PV1-F vs H1Z2Z2-K", None),
    "blog-solar-cable-harsh-environments.html": (
        "Solar Cable for Harsh Environments: Coastal & Desert", None),
    "blog-solar-cable-installation.html": (
        "Solar Cable Installation Guide: Sizing & Routing",
        "Solar cable installation guide: cable sizing, routing, grounding and connection best "
        "practice for a 25+ year service life. TUV & UL certified maker."),
    "blog-solar-cable-japan.html": (
        "Solar Cable for Japan: Earthquake & Typhoon Resilience",
        "PV cable selection for Japanese solar projects: seismic movement, typhoon wind loading, "
        "salt-air coastal sites and JIS-aligned documentation."),
    "blog-solar-cable-maintenance-tips.html": (
        "Solar Cable Maintenance: Extend System Life to 30 Years", None),
    "blog-solar-cable-manufacturing.html": (
        "Solar Cable Manufacturing: From Copper to Finished Cable", None),
    "blog-solar-cable-price-guide-2026.html": (
        "Solar Cable Price 2026: PV1-F, H1Z2Z2-K & MC4 Costs", None),
    "blog-solar-cable-return-investment.html": (
        "Solar Cable ROI: How Quality Cable Saves Money in 25 Years",
        "Why certified PV cable pays back over 25 years: failure cost, derating losses and "
        "replacement labour compared with cheap uncertified cable."),
    "blog-solar-cable-standards-comparison.html": (
        "Solar Cable Standards: IEC 62541 vs UL 4703 vs CE",
        "Compare solar cable standards side by side: IEC 62541, UL 4703 and CE marking \u2014 "
        "scope, test methods and which mark your project needs."),
    "blog-solar-cable-standards-iec-tuv-ul.html": (
        "Solar Cable Standards: IEC 62930, 62541 & UL 4703", None),
    "blog-solar-cable-storage-handling.html": (
        "Solar Cable Storage & Handling: Prevent Cable Damage",
        "How to store and handle solar cable without damaging it: drum handling, bend radius, "
        "UV exposure and moisture control before installation."),
    "blog-solar-cable-storage.html": (
        "Energy Storage Cables: Battery to Inverter Connections",
        "DC cable for battery-to-inverter connections in BESS: LSZH sheath, voltage rating, "
        "short-circuit withstand and routing in confined spaces."),
    "blog-top-10-solar-cable-manufacturers-china.html": (
        "Top 10 Solar Cable Manufacturers in China (2026)", None),
    "blog-solar-cable-manufacturer-china.html": (
        "Solar Cable Manufacturer China | TUV, UL & CE Certified",
        "Why 50+ countries buy PV cable from China: TUV, UL and CE certification, factory "
        "pricing and export delivery documented, from JunlinChicheng."),
    "how-to-verify-solar-cable-supplier-quality.html": (
        "How to Verify Solar Cable Supplier Quality: 7 Checks",
        "Don't get caught by fake TUV certificates. Seven verification steps to confirm your "
        "solar cable supplier is genuine. Quality inspection guide."),
    "faq.html": ("PV Cable Manufacturer FAQ | JunlinChicheng",
                 "Answers on PV cable specs, TUV/UL certification, lead times and custom "
                 "manufacturing \u2014 from the JunlinChicheng technical team."),
    "import-solar-cables-china.html": (
        "Import Solar Cables from China | TUV Certified Supplier",
        "Import TUV and UL certified solar cable from China: factory pricing, export documents "
        "for customs clearance and delivery to 50+ countries."),
    "solar-cable-certification-guide.html": (
        "Solar Cable Certification: TUV, UL, CE, SABS, SONCAP",
        "Which solar cable certificates your project needs: TUV Rheinland, UL Listed, CE, "
        "SABS (South Africa), SONCAP (Nigeria) and KEBS (Kenya), explained."),
    "solar-cable-exporter-china.html": (
        "Solar Cable Exporter China | PV Cable for Global Projects", None),
    "solar-cable-for-nigeria.html": (
        "Solar Cables for Nigeria: PV1-F, MC4 & Storage DC",
        "TUV & UL certified PV1-F, H1Z2Z2-K and MC4 shipped to Lagos, Abuja and Port Harcourt. "
        "Factory-direct pricing and export documents from China."),
    "solar-cable-installation-guide.html": (
        "Solar Cable Installation Guide: Routing, MC4 & Clipping",
        "PV1-F and H1Z2Z2-K routing, MC4 crimping, cable clipping and trunking, with IEC and "
        "NEC compliance notes for utility and rooftop PV."),
    "solar-cable-lead-time.html": ("Solar Cable Lead Time & Export Delivery Schedule", None),
    "solar-cable-price-list-2026.html": (
        "Solar Cable Price List 2026: PV1-F, H1Z2Z2-K, MC4",
        "2026 solar cable price guide: PV1-F 2x2.5 mm\u00b2, H1Z2Z2-K 6 mm\u00b2 and MC4 "
        "wholesale prices from a China manufacturer. Factory-direct quotes."),
    "solar-cable-sample-order.html": ("Order Free Solar Cable Samples | Quality Testing", None),
    "solar-cable-distributor.html": (
        "Solar Cable Distributor | Become a PV Cable Reseller",
        "Become an authorised solar cable distributor: wholesale pricing, TUV & UL certified PV "
        "cable, MC4 connectors and marketing support."),
    "solar-cable-for-south-africa.html": (
        "Solar Cables for South Africa: PV1-F & H1Z2Z2-K",
        "TUV & UL certified PV1-F, H1Z2Z2-K and MC4 supplied to EPCs and distributors across "
        "South Africa. Factory-direct pricing from China."),
    "solar-cable-price-comparison-by-country.html": (
        "Solar Cable Price Comparison 2026: China vs Europe vs USA",
        "Compare solar cable prices by country and see how Chinese PV cable compares with "
        "European brands at equal TUV/UL quality. 2026 guide."),
    "solar-cable-request-quote.html": (
        "Request a Solar Cable Quote | Reply in 2 Hours",
        "Free solar cable quote: PV1-F, H1Z2Z2-K and MC4, TUV & UL certified. Send your spec "
        "and get a reply within 2 hours on WhatsApp."),
    "pv1-f-solar-cable.html": (
        "PV1-F Solar Cable | 0.6/1 kV TUV & UL Certified",
        "PV1-F 2-core solar cable, 0.6/1 kV, XLPO insulated, TUV and UL certified. 1 to 6 mm\u00b2, "
        "factory-direct pricing from China."),
    "solar-cable-ac.html": (
        "AC Power Cable 450/750 V | 3-Core for PV Inverters",
        "Three-core AC cable (blue, brown, green/yellow) for inverter output and distribution "
        "circuits. 450/750 V, IEC 60228 conductor."),
    "solar-cable-combiner.html": (
        "PV Combiner Box | 6, 8, 12 & 16 Inputs, IP65",
        "PV combiner boxes with 6, 8, 12 or 16 inputs, IP65 enclosure, surge protection and DC "
        "disconnect. IEC 61439 compliant."),
    "solar-cable-faq.html": ("Solar Cable FAQ: Common Questions About PV Cables", None),
    "blog-microinverters-cabling.html": (
        "Microinverter Cable: String Lengths & Layout", None),
    "blog-pv1-f-vs-h1z2z2-k.html": (
        "PV1-F vs H1Z2Z2-K: Which Solar Cable to Choose", None),
    "blog-solar-cable-australia.html": (
        "Solar Cable for Australia: AS/NZS Requirements", None),
    "blog-solar-cable-certification-guide.html": (
        "Solar Cable Certification 2026: TUV, UL, IEC, CE",
        "Solar cable certifications explained: TUV, UL, IEC and CE standards, what each covers "
        "and which your project needs."),
    "blog-solar-cable-warranty-comparison.html": (
        "Solar Cable Warranty: What Manufacturers Offer", None),
    "blog-start-solar-cable-business-africa.html": (
        "Start a Solar Cable Business in Africa 2026", None),
    "solar-cable-for-india.html": (
        "Solar Cables for India: PV1-F, H1Z2Z2-K & MC4", None),
    "solar-cable-exporter-africa.html": (
        "Solar Cable Exporter to Africa | TUV & UL Certified",
        "TUV & UL certified solar PV cable supplied to South Africa, Nigeria, Kenya, Ghana and "
        "50+ African countries. Factory-direct pricing."),
    "solar-cable-manufacturer-india.html": (
        "Solar Cable Manufacturer India | PV1-F & H1Z2Z2-K", None),
    "solar-cable-exporter-china.html": (
        "Solar Cable Exporter China | PV Cable for Global Projects",
        "Solar cable exporter from China: TUV & UL certified PV1-F, H1Z2Z2-K and MC4 connectors, "
        "factory-direct pricing, 50+ export markets."),
    "solar-cable-lead-time.html": (
        "Solar Cable Lead Time & Export Delivery Schedule",
        "Solar cable production lead times and worldwide shipping: standard orders ship in 7-15 "
        "days, express options for urgent projects."),
    "solar-cable-sample-order.html": (
        "Order Free Solar Cable Samples | Quality Testing",
        "Request free solar cable samples: test PV1-F and H1Z2Z2-K before ordering in bulk. "
        "TUV & UL certified quality."),
    "blog-solar-cable-standards-iec-tuv-ul.html": (
        "Solar Cable Standards: IEC 62930, 62541 & UL 4703",
        "Solar cable standards explained: IEC 62930 (PV1-F), IEC 62541 (H1Z2Z2-K) and UL 4703, "
        "and which one your solar project needs."),
    "blog-start-solar-cable-business-africa.html": (
        "Start a Solar Cable Business in Africa 2026",
        "How to start a solar cable import and distribution business in Africa: market size, "
        "sourcing from China, certification and margins."),
    "blog-solar-cable-for-contractors.html": (
        "Solar Cable for Contractors: PV1-F vs H1Z2Z2-K",
        "Guide for electrical contractors choosing solar PV cable: PV1-F vs H1Z2Z2-K, MC4 "
        "connector matching, and residential vs commercial sizing."),
    "pv-cable-vs-electrical-cable-difference.html": (
        "PV Cable vs Electrical Cable: Key Differences",
        "Why regular electrical cable must not be used for solar installations: insulation, UV "
        "and temperature ratings, and how to pick the right PV cable."),
    "h1z2z2-k-solar-cable.html": (
        "H1Z2Z2-K Solar Cable | 1 kV TUV Certified, 1.5-6 mm2",
        "H1Z2Z2-K single core solar cable (1 kV) to IEC 62930, TUV approved, black XLPO "
        "insulated. 1.5 to 6 mm\u00b2 for DC string connections."),
}

# --- CTA headings that were auto-built from the old <title> ("Need <title>?") ---
CTA_FIX = {
    "solar-cable-contact.html": "\U0001F4E6 Need to Talk to a Sales Engineer?",
    "solar-cable-faq.html": "\U0001F4E6 Still Have Questions?",
    "solar-cable-lead-time.html": "\U0001F4E6 Need a Delivery Date?",
    "solar-cable-request-quote.html": "\U0001F4E6 Ready for a Quote?",
    "solar-cable-sample-order.html": "\U0001F4E6 Want to Test Before Ordering?",
}

# --- duplicate H1 fixes: thin country landing pages get product-specific headings ---
H1_FIX = {
    "solar-cable-for-kenya.html": ("Solar Cables for Kenya: PV1-F, MC4 & Off-Grid Sets",
                                   "Solar Cables for Kenya: PV1-F, MC4 & Off-Grid Sets"),
    "solar-cable-for-nigeria.html": ("Solar Cables for Nigeria: PV1-F, MC4 & Storage DC",
                                     None),
    "solar-cable-for-saudi-arabia.html": ("Solar Cables for Saudi Arabia: PV1-F & H1Z2Z2-K",
                                          "Solar Cables for Saudi Arabia: PV1-F & H1Z2Z2-K"),
    "solar-cable-for-south-africa.html": ("Solar Cables for South Africa: PV1-F & H1Z2Z2-K",
                                          None),
    "solar-cable-for-uae.html": ("Solar Cables for UAE: PV1-F, MC4 & Combiner Boxes",
                                 "Solar Cables for UAE: PV1-F, MC4 & Combiner Boxes"),
    "solar-cable-for-india.html": ("Solar Cables for India: PV1-F, H1Z2Z2-K & MC4",
                                   None),
    "solar-cable-manufacturer-india.html": ("Solar Cable Manufacturer for India: PV1-F & H1Z2Z2-K",
                                            None),
}

stats = {
    "country_title": 0, "brand_strip": 0, "country_desc": 0, "blog_desc": 0,
    "override_title": 0, "override_desc": 0, "h1_fixed": 0, "cta_fixed": 0,
    "footer_sitemap": 0, "files_written": 0,
}
problems = []


def set_title(s, new):
    m = re.search(r"<title>(.*?)</title>", s, re.S | re.I)
    if not m:
        return s, False
    if H.unescape(m.group(1)).strip() == new:
        return s, False
    return s[:m.start(1)] + new + s[m.end(1):], True


DESC_RE = re.compile(r'(<meta[^>]+name=["\']description["\'][^>]+content=)(["\'])(.*?)\2', re.S | re.I)


def set_desc(s, new):
    """Replace a description in place.

    The closing quote is a backreference so an apostrophe inside a
    double-quoted attribute (e.g. "Cote d'Ivoire") no longer ends the match.
    """
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


def set_h1(s, new):
    m = re.search(r"(<h1[^>]*>)(.*?)(</h1>)", s, re.S | re.I)
    if not m:
        return s, False
    if H.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip() == new:
        return s, False
    return s[:m.start(2)] + new + s[m.end(2):], True


for p in sorted(TARGET.glob("*.html")):
    s = p.read_text(encoding="utf-8")
    orig = s
    name = p.name

    # 1. country hub title
    m = re.search(r"<title>(.*?)</title>", s, re.S | re.I)
    title = H.unescape(m.group(1).strip()) if m else ""
    cm = COUNTRY_TITLE.match(title)
    if cm:
        s, ch = set_title(s, "Solar Cable Supplier for %s | TUV & UL Certified" % cm.group(1))
        stats["country_title"] += ch
        title = "Solar Cable Supplier for %s | TUV & UL Certified" % cm.group(1)
    elif title and len(title) > TITLE_MAX and BRAND_TAIL.search(title):
        # long only because of the company-name tail: drop the tail, keep the keywords
        title = BRAND_TAIL.sub("", title).strip()
        s, ch = set_title(s, title)
        stats["brand_strip"] += ch

    # 2. country hub description
    md = DESC_RE.search(s)
    desc = H.unescape(md.group(3).strip()) if md else ""
    cd = COUNTRY_DESC.match(desc)
    if cd:
        newd = ("TUV & UL certified PV1-F and H1Z2Z2-K solar cable for %s. Factory-direct "
                "pricing, IEC 62930, export documentation supplied. Quote in 2 hours." % cd.group(1))
        s, ch = set_desc(s, newd)
        stats["country_desc"] += ch
        desc = newd

    # 3. blog boilerplate tail
    if BLOG_TAIL.search(desc):
        desc = BLOG_TAIL.sub(BLOG_TAIL_NEW, desc)
        s, ch = set_desc(s, desc)
        stats["blog_desc"] += ch

    # 4. explicit overrides
    if name in OVR:
        nt, nd = OVR[name]
        s, ch = set_title(s, nt)
        stats["override_title"] += ch
        title = nt
        if nd:
            s, ch = set_desc(s, nd)
            stats["override_desc"] += ch
            desc = nd

    # 5a. CTA heading that echoed the old title
    if name in CTA_FIX:
        new_h3 = CTA_FIX[name]
        m3 = re.search(r"(<h3[^>]*>\s*\U0001F4E6[^<]*</h3>)", s, re.I)
        if m3 and H.unescape(re.sub(r"<[^>]+>", "", m3.group(1))).strip() != new_h3:
            s = s[:m3.start(1)] + "<h3>%s</h3>" % new_h3 + s[m3.end(1):]
            stats["cta_fixed"] += 1

    # 5. duplicate H1
    if name in H1_FIX:
        nh, nt2 = H1_FIX[name]
        s, ch = set_h1(s, nh)
        stats["h1_fixed"] += ch
        if nt2 and title != nt2:
            s, ch = set_title(s, nt2)
            if ch:
                stats["override_title"] += 1
                title = nt2

    if s != orig:
        stats["files_written"] += 1
        if not DRY:
            p.write_text(s, encoding="utf-8")

    if len(title) > TITLE_MAX:
        problems.append(("title", name, len(title), title))
    if desc and len(desc) > DESC_MAX:
        problems.append(("desc", name, len(desc), desc[:70] + "..."))

# 6. index.html footer site-map link
idx = TARGET / "index.html"
s = idx.read_text(encoding="utf-8")
if "site-map.html" not in s:
    pat = re.compile(r'(<div class="footer-col"><h4>Company</h4><ul>)')
    if pat.search(s):
        s2 = pat.sub(lambda mm: mm.group(1) + '<li><a href="/suncable-website/site-map.html">Site Map</a></li>', s, count=1)
        s2 = s2.replace("<li></li>", "")
        if s2 != s:
            stats["footer_sitemap"] += 1
            stats["files_written"] += 1
            if not DRY:
                idx.write_text(s2, encoding="utf-8")
    else:
        problems.append(("footer", "index.html", 0, "Company footer column not found"))

print("mode:", "DRY-RUN" if DRY else "APPLY")
for k, v in stats.items():
    print("  %-14s %d" % (k, v))
print("  over %d chars  %d" % (TITLE_MAX, sum(1 for x in problems if x[0] == "title")))
print("  desc over %d   %d" % (DESC_MAX, sum(1 for x in problems if x[0] == "desc")))
for kind, name, ln, val in problems[:40]:
    print("   %-5s %-46s %3d  %s" % (kind, name, ln, val))
