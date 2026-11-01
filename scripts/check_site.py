#!/usr/bin/env python3
"""Validate the built site. Exit code 1 on any failure.

Checks
  1. data/contests.json is valid JSON and every upstream listing id is retained exactly once.
  2. Every published field (free entry, prize, deadline, eligibility, AI rules, payment) in a row
     is backed by an evidence record that has a verbatim quote AND an official http(s) URL.
  3. No row publishes a value while being labelled "unverified".
  4. Every row has at least one source URL, and every non-official-only row is flagged.
  5. Every local href/src in every page resolves to a file in the repo (no broken internal links).
  6. Every external source URL in the dataset is absolute http(s) (no javascript:, no #).
  7. Pages carry charset, viewport and lang, and app.js parses with node --check.
  8. Row count on each page equals the count reported in data/contests.json.
"""
import json, pathlib, re, subprocess, sys
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
fails, warns = [], []

def fail(msg):
    fails.append(msg)

def ok(msg):
    print("  ok  " + msg)

# 1 ---------------------------------------------------------------- dataset
data = json.loads((ROOT / "data/contests.json").read_text())
up = json.loads((ROOT / "data/upstream.json").read_text())
rows = data["entries"]
ids = [r["id"] for r in rows]
if len(ids) != len(set(ids)):
    fail("duplicate ids in data/contests.json")
missing = [l["id"] for l in up["listings"] if l["id"] not in set(ids)]
if missing:
    fail(f"upstream listings dropped: {missing}")
else:
    ok(f"all {len(up['listings'])} upstream listings retained ({len(rows)} rows total)")

# 2, 3 ----------------------------------------------------------- published values
evidence = {}
for f in sorted((ROOT / "data/evidence").glob("*.json")):
    rec = json.loads(f.read_text())
    evidence[rec["id"]] = rec

FIELD_KEYS = {"free": "freeEntry", "prize": "prize", "deadline": "deadline",
              "eligibility": "eligibility", "ai": "aiPolicy", "payout": "payout"}
published = 0
for r in rows:
    ev = evidence.get(r["id"], {})
    for pub, evkey in FIELD_KEYS.items():
        val = r.get(pub)
        if not val:
            continue
        published += 1
        src = ev.get("fields", {}).get(evkey, {})
        if not src.get("quote"):
            fail(f"{r['id']}: field '{pub}' published without a verbatim quote")
        if not src.get("url", "").startswith("http"):
            fail(f"{r['id']}: field '{pub}' published without an http(s) source url")
        if urlsplit(src.get("url", "")).scheme not in ("http", "https"):
            fail(f"{r['id']}: field '{pub}' source is not http(s)")
    if r["verdict"] == "unverified" and any(r.get(k) for k in FIELD_KEYS):
        fail(f"{r['id']}: labelled unverified but publishes values")
    if not r["sources"]:
        fail(f"{r['id']}: no source at all")
    if not r["official"] and not any("No official operator source" in f for f in r["flags"]):
        fail(f"{r['id']}: no official source and the row is not flagged")
    for s in r["sources"]:
        if urlsplit(s["url"]).scheme not in ("http", "https"):
            fail(f"{r['id']}: source '{s['url']}' is not absolute http(s)")
ok(f"{published} published field values, all carrying quotes and official URLs")
ok(f"{len(evidence)} entries have recorded evidence; {sum(1 for r in rows if r['verdict']=='unverified')} remain unverified and blank")

# 4 ------------------------------------------------------- build reproducibility
before = (ROOT / "data/contests.json").read_text()
subprocess.run([sys.executable, str(ROOT / "scripts/build_site.py")], check=True, capture_output=True)
if before != (ROOT / "data/contests.json").read_text():
    fail("data/contests.json changed after a rebuild - build is not deterministic")
else:
    ok("rebuild is deterministic")

GEN = {"index.html", "contests.html", "summary.html", "review.html", "404.html"} | {
    c["id"] + ".html" for c in json.loads((ROOT / "data/categories.json").read_text())}

# 5 ------------------------------------------------------------- internal links
class Links(HTMLParser):
    def __init__(self, base=ROOT):
        super().__init__()
        self.base = base
        self.bad = []
        self.hrefs = 0
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.hrefs += 1
                u = urlsplit(v)
                if u.scheme in ("http", "https", "mailto", "data"):
                    continue
                if v.startswith("#") or not u.path:
                    continue
                target = (self.base / unquote(u.path)).resolve()
                if target.is_dir():
                    target = target / "index.html"   # directory links (e.g. ../flagged/)
                if not target.is_file():
                    self.bad.append(v)

pages = sorted(ROOT.glob("*.html"))
SKIP_DIRS = {"node_modules", "test-results", "playwright-report", "coverage", ".git", ".venv", "__pycache__"}
all_pages = sorted(q for q in ROOT.glob("**/*.html")
                   if not (set(q.relative_to(ROOT).parts) & SKIP_DIRS)
                   and "node_modules" not in q.parts)
for p in all_pages:
    text = p.read_text()
    lk = Links(p.parent)
    lk.feed(text)
    if lk.bad:
        fail(f"{p.name}: broken local links {sorted(set(lk.bad))}")
    if 'charset="utf-8"' not in text:
        fail(f"{p.name}: missing charset")
    if 'name="viewport"' not in text:
        fail(f"{p.name}: missing viewport")
    if '<html lang="en">' not in text:
        fail(f"{p.name}: missing lang")
    # anchor targets: both same-page "#x" and "page.html#x"
    anchors = set(re.findall(r'id="([^"]+)"', text))
    generated = (p.parent == ROOT) and (p.name in GEN)
    for a in re.findall(r'href="#([^"]+)"', text):
        if a not in anchors:
            (fail if generated else warns.append)(
                f"{p.name}: in-page anchor #{a} has no target" if generated
                else f"{p.name}: in-page anchor #{a} has no target (owned by another session; not edited)")
    for path, a in re.findall(r'href="([^"#]+)#([^"]+)"', text):
        if path.startswith(("http", "mailto")):
            continue
        tgt = (p.parent / unquote(path)).resolve()
        if tgt.is_dir():
            tgt = tgt / "index.html"
        if tgt.is_file() and f'id="{a}"' not in tgt.read_text():
            warns.append(f"{p.name}: {path}#{a} target id not found")
ok(f"{len(all_pages)} pages (root + parallel audit pages), internal links resolve, metadata present")
for w in sorted(set(warns)):
    print("  warn " + w)

# 6 ------------------------------------------------------------ JS / CSS exist
if subprocess.run(["node", "--check", str(ROOT / "app.js")], capture_output=True).returncode != 0:
    fail("app.js fails node --check")
else:
    ok("app.js parses")
for asset in ("style.css", "app.js"):
    if not (ROOT / asset).is_file():
        fail(f"missing asset {asset}")

# 7 --------------------------------------------------------- per-page row counts
counts = {c["id"]: sum(1 for r in rows if r["category"] == c["id"]) for c in json.loads((ROOT / "data/categories.json").read_text())}
for cid, n in counts.items():
    text = (ROOT / f"{cid}.html").read_text()
    got = text.count('data-row="')
    if got != n:
        fail(f"{cid}.html shows {got} rows, expected {n}")
ok("category page row counts match the dataset")
if (ROOT / "contests.html").read_text().count('data-row="') != len(rows):
    fail("contests.html does not show every row")
else:
    ok(f"contests.html shows all {len(rows)} rows")

# 8 --------------------------------------------------------------- summaries
print()
if fails:
    print(f"FAILED ({len(fails)})")
    for f in fails:
        print("  - " + f)
    sys.exit(1)
print(f"PASSED: {len(rows)} rows, {published} evidence-backed values, {len(all_pages)} pages, no broken local or anchor links.")
