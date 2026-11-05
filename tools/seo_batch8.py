"""SEO batch 8 - cosmetic normalisation after batch 7.

Batch 7 turned "-40°C to +120°C" into "-40°C to 90°C" (the '+' was consumed by
the pattern), so the site now mixes "+90°C" and "90°C" for the same value.
This restores the sign so every temperature range reads the same way.

Idempotent: the replaced forms no longer match the source patterns.
"""

import pathlib

SUBS = [
    ("-40°C to 90°C", "-40°C to +90°C"),
    ("-40 to 90°C", "-40 to +90°C"),
    ("-40°C~90°C", "-40°C~+90°C"),
    ("-40~90°C", "-40~+90°C"),
    ("-40C to 90C", "-40C to +90C"),
]

root = pathlib.Path(".")
total = 0
files = 0
for p in sorted(root.glob("*.html")):
    s = orig = p.read_text(encoding="utf-8", errors="replace")
    n = 0
    for a, b in SUBS:
        c = s.count(a)
        if c:
            s = s.replace(a, b)
            n += c
    if s != orig:
        p.write_text(s, encoding="utf-8", newline="")
        files += 1
        total += n

print("files_written", files)
print("sign_restored", total)
left = 0
for p in sorted(root.glob("*.html")):
    s = p.read_text(encoding="utf-8", errors="replace")
    for a, _ in SUBS:
        left += s.count(a)
print("remaining_without_plus", left)
