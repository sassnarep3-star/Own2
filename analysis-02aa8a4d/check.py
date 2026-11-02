#!/usr/bin/env python3
"""Checks for the analysis-02aa8a4d subsite. Fails loudly on any violation of
the evidence policy (blank-unless-verified), broken links, nondeterminism,
count mismatches, or score-math errors."""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
FAILS = []


def fail(msg):
    FAILS.append(msg)


def main():
    # 1) deterministic rebuild
    before = {}
    for p in sorted(BASE.rglob("*")):
        if p.is_file() and p.suffix in (".html", ".json") and "reports" not in p.parts:
            before[str(p.relative_to(BASE))] = p.read_bytes()
    subprocess.run([sys.executable, str(BASE / "build.py")], check=True, capture_output=True)
    after = {}
    for p in sorted(BASE.rglob("*")):
        if p.is_file() and p.suffix in (".html", ".json") and "reports" not in p.parts:
            after[str(p.relative_to(BASE))] = p.read_bytes()
    if before != after:
        diff = {k for k in set(before) | set(after) if before.get(k) != after.get(k)}
        fail(f"non-deterministic build output: {sorted(diff)}")

    contests = json.loads((ROOT / "data" / "contests.json").read_text(encoding="utf-8"))
    freshness = json.loads((BASE / "data" / "freshness.json").read_text(encoding="utf-8"))
    stats = json.loads((BASE / "reports" / "stats.json").read_text(encoding="utf-8"))

    # 2) counts reconcile
    if stats["total_rows"] != len(contests["entries"]):
        fail(f"row count mismatch: stats {stats['total_rows']} vs data {len(contests['entries'])}")
    if stats["freshness_records"] != len(freshness["records"]):
        fail("freshness record count mismatch")

    # 3) freshness evidence policy: value => quote + url (or explicit null)
    for r in freshness["records"]:
        for field in ("status", "prize", "free", "eligibility", "format"):
            f = r.get(field)
            if not f:
                continue
            if f.get("value") and not (f.get("quote") and f.get("url")):
                fail(f"{r['id']}.{field}: value published without quote+url")
            if not f.get("value") and f.get("quote"):
                fail(f"{r['id']}.{field}: quote without value (inconsistent)")
        if not r.get("url", "").startswith("https://"):
            fail(f"{r['id']}: missing official url")

    # 4) every all/cat table row has a source link or the no-source stamp
    for name in ["all.html"] + [f"cat-{s}.html" for s, _ in [
        ("skill", 0), ("trivia", 0), ("sports", 0), ("forecasting", 0), ("market", 0),
        ("creative", 0), ("tech", 0), ("directory", 0), ("pools", 0)]]:
        text = (BASE / name).read_text(encoding="utf-8")
        rows = re.findall(r"<tr data-search=.*?</tr>", text, flags=re.S)
        if not rows:
            fail(f"{name}: no data rows found")
        for row in rows:
            if 'class="src"' not in row and "no official source" not in row:
                fail(f"{name}: row without source link or no-source stamp: {row[:120]}")

    # 5) every generated page has charset/viewport/lang/h1 and all local links resolve
    for p in sorted(BASE.glob("*.html")):
        text = p.read_text(encoding="utf-8")
        for needle in ('charset="utf-8"', 'name="viewport"', '<html lang="en">', "<h1>", 'id="content"'):
            if needle not in text:
                fail(f"{p.name}: missing {needle}")
        for m in re.finditer(r'(?:href|src)="([^"#][^"]*)"', text):
            url = m.group(1)
            if re.match(r"^(https?:|mailto:|tel:|data:|javascript:|//)", url):
                continue
            path_part = url.split("#", 1)[0].split("?", 1)[0]
            if path_part and not (p.parent / path_part).exists():
                fail(f"{p.name}: broken local link {url}")

    # 6) score math: recompute totals from rendered ranked page components
    ranked = (BASE / "ranked.html").read_text(encoding="utf-8")
    for m in re.finditer(
        r"<strong>(\d+)</strong></td>\s*<td data-label=\"Free\">(\d+)/20 .*?"
        r"<td data-label=\"Cash\">(\d+)/25 .*?<td data-label=\"Open now\">(\d+)/20 .*?"
        r"<td data-label=\"Cadence\">(\d+)/15 .*?<td data-label=\"Eligibility\">(\d+)/10 .*?"
        r"<td data-label=\"Effort\">(\d+)/10",
        ranked, flags=re.S,
    ):
        total = int(m.group(1))
        parts = sum(int(m.group(i)) for i in range(2, 8))
        if total != parts:
            fail(f"score math error: total {total} != components {parts}")
    if "unranked" not in ranked:
        fail("ranked.html: missing unranked disclosure")

    # 7) all.html carries the full catalog
    all_text = (BASE / "all.html").read_text(encoding="utf-8")
    n_rows = len(re.findall(r"<tr data-search=", all_text))
    if n_rows != len(contests["entries"]):
        fail(f"all.html rows {n_rows} != catalog {len(contests['entries'])}")
    for row in contests["entries"]:
        if f">{row['id']}</span>" not in all_text:
            fail(f"all.html missing row id {row['id']}")

    # 8) JS syntax
    try:
        subprocess.run(["node", "--check", str(BASE / "app.js")], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        fail(f"app.js syntax check failed: {e}")

    if FAILS:
        print("CHECK FAILED:")
        for f in FAILS:
            print(" -", f)
        sys.exit(1)
    print(f"CHECK PASSED: {stats['total_rows']} rows, {stats['assessed_rows']} assessed, "
          f"{stats['freshness_records']} freshness records, "
          f"{stats['internal_pages_scanned']} internal pages scanned, "
          f"{stats['internal_broken']} broken internal links, deterministic build, evidence policy holds.")


if __name__ == "__main__":
    main()
