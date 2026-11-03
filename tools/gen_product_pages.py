import pathlib, re

ORIGIN = "https://xxy13992859166-ops.github.io"
BASE = "/suncable-website"

PRODUCTS = [
    {
        "slug": "solar-cable-storage",
        "title": "Storage Battery DC Cable | LSZH Low-Smoke 0.6/1kV TUV",
        "desc": "Low-smoke halogen-free DC cable for energy storage battery banks. 0.6/1 kV rated, TUV certified, green/yellow or black jacket, factory direct from China.",
        "keywords": "storage battery cable, energy storage DC cable, LSZH battery cable, 0.6/1kV DC cable, TUV storage cable",
        "h1": "Storage Battery DC Cable \u2014 LSZH Low-Smoke",
        "crumb": "Storage Battery DC Cable",
        "wa": "storage battery DC cable",
        "subject": "Storage%20Battery%20DC%20Cable%20Inquiry",
        "lead": "Low-smoke halogen-free DC cable built for energy storage battery banks. Optimized for high-current DC applications in residential and commercial storage systems, rated 0.6/1 kV and TUV certified.",
        "image": "images/storage.jpg",
        "alt": "Storage Battery DC Cable low smoke halogen free",
        "specs": [
            ("Rated Voltage", "0.6/1 kV DC"),
            ("Insulation / Sheath", "LSZH (low smoke zero halogen)"),
            ("Colors", "Green/Yellow or Black"),
            ("Certifications", "TUV"),
            ("Application", "Energy storage battery banks, high-current DC circuits"),
        ],
        "app_intro": "This DC cable connects battery racks, battery management systems and power conversion equipment inside <strong>energy storage systems</strong>. The low-smoke halogen-free construction limits smoke emission and corrosive gas in the event of fire, which matters for indoor cabinets and containerised storage.",
        "app_items": [
            "Residential battery storage cabinets",
            "Commercial and industrial BESS containers",
            "Battery rack to PCS / inverter DC runs",
            "Off-grid and hybrid solar storage systems",
        ],
        "cards": [
            ("LSZH Construction", "Low smoke, zero halogen \u2014 safer in enclosed battery cabinets and containers."),
            ("High-Current DC", "Rated 0.6/1 kV DC for continuous high-current battery bank connections."),
            ("TUV Certified", "German TUV certification for the insulation and sheath compound."),
            ("Factory Price", "Direct from our Xi'an factory. MOQ 1km per colour and specification."),
        ],
    },
    {
        "slug": "solar-cable-ac",
        "title": "AC Power Cable 450/750V 3-Core | IEC 60228 VDE",
        "desc": "Three-core AC cable with blue, brown and green/yellow cores for PV inverter output and distribution circuits. 450/750 V rated, IEC 60228 conductor, IEC and VDE compliant.",
        "keywords": "AC power cable 450/750V, 3 core AC cable, PV inverter AC cable, IEC 60228 cable, VDE AC cable",
        "h1": "AC Power Cable \u2014 450/750V Three-Core",
        "crumb": "AC Power Cable",
        "wa": "AC power cable",
        "subject": "AC%20Power%20Cable%20Inquiry",
        "lead": "Three-core AC cable with blue, brown and green/yellow core identification for PV inverter output and distribution circuits. Rated 450/750 V, conductor to IEC 60228, compliant with IEC and VDE standards.",
        "image": "images/ac_cable.jpg",
        "alt": "AC power cable three core blue brown green yellow",
        "specs": [
            ("Rated Voltage", "450/750 V AC"),
            ("Cores", "3-core"),
            ("Conductor", "Copper, to IEC 60228"),
            ("Core Colors", "Blue / Brown / Green-Yellow"),
            ("Standards", "IEC, VDE"),
        ],
        "app_intro": "This cable carries the AC side of a photovoltaic system \u2014 from the inverter output to the distribution board, and from there to the load. The three-core layout provides phase, neutral and protective earth in a single cable, which simplifies wiring on rooftop and ground-mount installations.",
        "app_items": [
            "PV inverter AC output to distribution board",
            "Rooftop and ground-mount solar installations",
            "AC combiner and distribution circuits",
            "Small commercial and residential solar systems",
        ],
        "cards": [
            ("Standard Conductor", "Copper conductor manufactured to IEC 60228 for predictable current rating."),
            ("Clear Core ID", "Blue / brown / green-yellow cores speed up correct phase, neutral and earth wiring."),
            ("IEC & VDE", "Built to meet IEC and VDE requirements for AC distribution cable."),
            ("Factory Price", "Direct from our Xi'an factory. MOQ 1km per colour and specification."),
        ],
    },
    {
        "slug": "solar-cable-combiner",
        "title": "Solar Combiner Box 6/8/12/16 Inputs | IP65 SPD DC Breaker",
        "desc": "PV combiner boxes with 6, 8, 12 or 16 inputs, IP65 enclosure, surge protection device and DC disconnect switch. IEC 61439 compliant, for outdoor string consolidation.",
        "keywords": "solar combiner box, PV combiner box, 6 8 12 16 input combiner, IP65 combiner box, SPD DC breaker combiner",
        "h1": "Solar Combiner Box \u2014 6/8/12/16 Inputs, IP65",
        "crumb": "Solar Combiner Box",
        "wa": "solar combiner box",
        "subject": "Solar%20Combiner%20Box%20Inquiry",
        "lead": "PV combiner boxes for consolidating multiple strings before the inverter. Available in 6, 8, 12 and 16 input configurations, IP65 enclosure, with surge protection device and DC disconnect switch, compliant with IEC 61439.",
        "image": "images/combiner.jpg",
        "alt": "Solar PV combiner box IP65 with SPD and DC breaker",
        "specs": [
            ("Input Configurations", "6 / 8 / 12 / 16 strings"),
            ("Enclosure Protection", "IP65"),
            ("Surge Protection", "SPD (surge protection device)"),
            ("Disconnection", "DC disconnect switch / breaker"),
            ("Standard", "IEC 61439"),
            ("Application", "Outdoor string consolidation before inverter"),
        ],
        "app_intro": "A combiner box gathers the output of several PV strings into one feed to the inverter, and provides a single point for isolation and surge protection. Multiple input configurations cover everything from a small rooftop array to a multi-string commercial installation.",
        "app_items": [
            "Rooftop commercial and residential arrays",
            "Ground-mount string consolidation",
            "Projects requiring string-level isolation",
            "Outdoor installations needing an IP65 enclosure",
        ],
        "cards": [
            ("Multiple Configurations", "6, 8, 12 and 16 input versions to match your string layout."),
            ("IP65 Enclosure", "Sealed against dust and water jets for outdoor mounting."),
            ("SPD + DC Breaker", "Built-in surge protection and DC disconnect in one enclosure."),
            ("IEC 61439", "Assemblies compliant with the IEC 61439 standard."),
        ],
    },
]

tpl = pathlib.Path("pv1-f-solar-cable.html").read_text(encoding="utf-8")
made = 0

for d in PRODUCTS:
    s = tpl
    url = "%s%s/%s.html" % (ORIGIN, BASE, d["slug"])

    s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % d["title"], s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % d["desc"], s, count=1)
    s = re.sub(r'<meta name="keywords" content="[^"]*">', '<meta name="keywords" content="%s">' % d["keywords"], s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url, s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % d["title"], s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % d["desc"], s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url, s, count=1)
    s = re.sub(r'<meta property="og:image" content="[^"]*">', '<meta property="og:image" content="%s%s/%s">' % (ORIGIN, BASE, d["image"]), s, count=1)

    s = re.sub(r'"name": "[^"]*"', '"name": "%s"' % d["title"], s, count=1)
    s = re.sub(r'"description": "[^"]*"', '"description": "%s"' % d["desc"], s, count=1)
    s = re.sub(r'"url": "https://xxy13992859166-ops\.github\.io/suncable-website/[^"]*"', '"url": "%s"' % url, s, count=1)

    s = re.sub(r'(<div class="breadcrumb">.*?&gt; )[^<]*(</div>)', lambda m: m.group(1) + d["crumb"] + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r"<h1>.*?</h1>", "<h1>%s</h1>" % d["h1"], s, count=1)
    s = re.sub(r'<p class="lead">.*?</p>', '<p class="lead">%s</p>' % d["lead"], s, count=1, flags=re.S)
    s = re.sub(r'<img src="[^"]*" alt="[^"]*"', '<img src="%s/%s" alt="%s"' % (BASE, d["image"], d["alt"]), s, count=1)

    rows = "".join(
        '<tr><td style="padding:10px;border:1px solid #e2e8f0">%s</td><td style="padding:10px;border:1px solid #e2e8f0">%s</td></tr>\n    ' % (k, v)
        for k, v in d["specs"]
    )
    s = re.sub(r'(<h2>Product Specifications</h2>\s*<table[^>]*>\s*<tr style="background:#f8fafc">.*?</tr>\s*)(.*?)(\s*</table>)',
               lambda m: m.group(1) + rows + m.group(3), s, count=1, flags=re.S)

    items = "".join("<li>%s</li>\n    " % i for i in d["app_items"])
    new_app = '<h2>Typical Applications</h2>\n  <p>%s</p>\n  <ul style="margin:12px 0 16px 20px;color:#475569">\n    %s</ul>\n\n  ' % (d["app_intro"], items)
    s = re.sub(r'<h2>Typical Applications</h2>.*?(?=<h2>Why Choose)', new_app, s, count=1, flags=re.S)

    cards = "".join('<div class="info-card"><h3>%s</h3><p>%s</p></div>\n    ' % (h, p) for h, p in d["cards"])
    s = re.sub(r'(<h2>Why Choose[^<]*</h2>\s*<div class="info-grid">\s*)(.*?)(\s*</div>)', lambda m: m.group(1) + cards + m.group(3), s, count=1, flags=re.S)

    s = s.replace("PV1-F%20Solar%20Cable%20Inquiry", d["subject"])
    s = s.replace("PV1-F%20solar%20cable", d["wa"].replace(" ", "%20"))
    s = s.replace("PV1-F Cable", d["crumb"])

    low = s.lower()
    assert "pv1-f" not in low, "template residue left in " + d["slug"]
    assert "/suncable-websiteimages" not in low, "bad image path in " + d["slug"]

    pathlib.Path(d["slug"] + ".html").write_text(s, encoding="utf-8")
    made += 1

print("pages written:", made)
sm_path = pathlib.Path("sitemap.xml")
if sm_path.exists():
    sm = sm_path.read_text(encoding="utf-8")
    added = 0
    for d in PRODUCTS:
        loc = "%s%s/%s.html" % (ORIGIN, BASE, d["slug"])
        if loc in sm:
            continue
        block = "  <url>\n    <loc>%s</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n" % loc
        sm = sm.replace("</urlset>", block + "</urlset>", 1)
        added += 1
    if added:
        sm_path.write_text(sm, encoding="utf-8")
    print("sitemap entries added:", added)
