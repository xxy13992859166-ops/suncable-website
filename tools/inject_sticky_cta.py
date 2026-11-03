import pathlib

TAG = '<script src="/suncable-website/assets/sticky-cta.js" defer></script>'
SKIP = {"thankyou.html"}

n = 0
for p in sorted(pathlib.Path(".").glob("*.html")):
    if p.name in SKIP:
        continue
    s = p.read_text(encoding="utf-8", errors="surrogateescape")
    if "sticky-cta.js" in s or "</body>" not in s:
        continue
    s = s.replace("</body>", TAG + "\n</body>", 1)
    p.write_text(s, encoding="utf-8", errors="surrogateescape")
    n += 1
print("files with sticky cta:", n)
