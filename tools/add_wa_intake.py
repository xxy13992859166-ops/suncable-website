"""Load assets/wa-intake.js on every page so WhatsApp openers open pre-filled
with product name, landing page and blanks for country / spec / quantity.

Idempotent: pages that already carry the tag are left untouched.
Runs from the repository root in GitHub Actions.
"""

import pathlib
import re

TAG = '<script src="/suncable-website/assets/wa-intake.js" defer></script>\n'

SKIP = {
    "thankyou.html",
    "wa-auto-dev.html",
    "seo-dashboard.html",
    "google17308f79e30f35f7.html",
    "index-original.html",
    "index_fixed.html",
}


def process(path):
    s = path.read_text(encoding="utf-8")
    if "assets/wa-intake.js" in s:
        return "unchanged"
    if "</body>" not in s:
        return "no-body"
    idx = s.rindex("</body>")
    path.write_text(s[:idx] + TAG + s[idx:], encoding="utf-8")
    return "updated"


def main():
    asset = pathlib.Path("assets/wa-intake.js")
    if not asset.exists():
        raise SystemExit("assets/wa-intake.js is missing")
    files = [p for p in sorted(pathlib.Path(".").glob("*.html")) if p.name not in SKIP]
    counts = {}
    for p in files:
        status = process(p)
        counts[status] = counts.get(status, 0) + 1
    loaded = sum(1 for p in files if "assets/wa-intake.js" in p.read_text(encoding="utf-8"))
    print("html files:", len(files))
    print("pages loading wa-intake.js:", loaded)
    for k in sorted(counts):
        print("%s: %d" % (k, counts[k]))
    missing = [p.name for p in files if "assets/wa-intake.js" not in p.read_text(encoding="utf-8")]
    if missing:
        print("missing:", len(missing))
        for name in missing[:10]:
            print("  ", name)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
