import re, pathlib

BASE = "/suncable-website"
ORIGIN = "https://xxy13992859166-ops.github.io"

attr = re.compile(r'(\b(?:href|src|action)=")(/(?!/|suncable-website)[^"]*?)(")', re.I)
dom = re.compile(r'(=")' + re.escape(ORIGIN) + r'/(?!suncable-website)([^"]*?)(")', re.I)
jsn = re.compile(r'("(?:url|@id|item|target|logo|image)":\s*")(/(?!/|suncable-website)[^"]*?)(")', re.I)
css = re.compile(r'(url\()(/(?!/|suncable-website)[^)\s]*?)')
repl = re.compile(r'\[CANONICAL_REPL\]')

changed = 0
for p in sorted(pathlib.Path(".").glob("*.html")):
    s = p.read_text(encoding="utf-8", errors="surrogateescape")
    o = s
    s = attr.sub(lambda m: m.group(1) + BASE + m.group(2) + m.group(3), s)
    s = dom.sub(lambda m: m.group(1) + ORIGIN + BASE + "/" + m.group(2) + m.group(3), s)
    s = jsn.sub(lambda m: m.group(1) + BASE + m.group(2) + m.group(3), s)
    s = css.sub(lambda m: m.group(1) + BASE + m.group(2), s)
    if repl.search(s):
        s = repl.sub(ORIGIN + BASE + "/" + p.name, s)
    if s != o:
        p.write_text(s, encoding="utf-8", errors="surrogateescape")
        changed += 1
print("files changed:", changed)
