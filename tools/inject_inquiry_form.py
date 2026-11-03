import pathlib

TAG = '<script src="/suncable-website/assets/inquiry-form.js" defer></script>'
SKIP = {
    "index.html", "index-original.html", "index_fixed.html", "thankyou.html",
    "baidu-submit.html", "bing-submit.html", "bing-submit-guide.html",
    "bing-verify-guide.html", "submit-to-google.html", "gsc-bing-guide.html",
    "indexing-guide.html", "seo-dashboard.html", "wa-auto-dev.html",
}

n = 0
for p in sorted(pathlib.Path(".").glob("*.html")):
    if p.name in SKIP:
        continue
    s = p.read_text(encoding="utf-8", errors="surrogateescape")
    if "inquiry-form.js" in s or "</body>" not in s:
        continue
    s = s.replace("</body>", TAG + "\n</body>", 1)
    p.write_text(s, encoding="utf-8", errors="surrogateescape")
    n += 1
print("files injected:", n)
