#!/usr/bin/env python3
"""Prepare structured entries.json from the source site's LEDGER data.js.

Source: https://karagemop466-tech.github.io/FreeMoneyApps/  (assets/data.js, pass S, reviewed 2026-08-19)
The 100_VERIFIED_CONTESTS.md in that repo is explicitly SUPERSEDED ("DO NOT USE AS A SOURCE")
and is NOT used here. See COORDINATION.md irregularities log.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_JS = ROOT / "data" / "source_data.js"
OUT = ROOT / "data" / "entries.json"

TYPE_LABELS = {
    "skill": "Skill tournaments",
    "trivia": "Trivia competitions",
    "sports": "Fantasy & sports picks",
    "forecasting": "Forecasting tournaments",
    "market": "Market competitions",
    "creative": "Creative contests",
    "tech": "Tech & data competitions",
    "directory": "Directories & forums",
    "pools": "Free pool & league platforms",
}
STATUS_LABELS = {"live": "Active", "ended": "Ended / out of season", "caution": "Caution", "mixed": "Mixed (paid option)"}
FREEPATH_LABELS = {"full": "Free USD path", "partial": "Some free events", "paid-cash": "Cash needs entry fee"}
PLATFORM_LABELS = {"web": "Browser", "ios": "iOS app", "android": "Android app"}

content = DATA_JS.read_text()
m = re.search(r"window\.LEDGER\s*=\s*(.*)\s*;?\s*$", content, re.DOTALL)
assert m, "LEDGER block not found"
s = m.group(1).rstrip().rstrip(";").strip()
# Tolerate JS-style trailing commas
s = re.sub(r",(\s*[}\]])", r"\1", s)
ledger = json.loads(s)
listings = ledger["listings"]
assert len(listings) == 206, len(listings)

entries = []
for e in listings:
    sources = e.get("sources", [])
    official = [s for s in sources if s.get("tier") == "official"]
    non_official = [s for s in sources if s.get("tier") != "official"]
    has_official = bool(official)

    # Per verification policy: values that cannot be confirmed from an official
    # source are left blank and flagged. If no official source exists at all,
    # the entry is flagged UNVERIFIED and monetary fields are blanked.
    unverified = not has_official

    prize = "" if unverified else (e.get("prizeUsd") or "")
    cashout = "" if unverified else (e.get("minCashout") or "")
    payout = "" if unverified else (", ".join(e.get("payoutMethods") or []) or "")

    # Best official source link; fallback to any source link for reference only.
    official_link = official[0]["url"] if official else ""
    official_title = official[0]["title"] if official else ""
    ref_link = (non_official[0]["url"] if non_official else "")
    ref_title = (non_official[0]["title"] if non_official else "")
    ref_tier = (non_official[0]["tier"] if non_official else "")

    entries.append({
        "id": e["id"],
        "name": e["name"],
        "short": e.get("short", ""),
        "type": e["type"],
        "typeLabel": TYPE_LABELS.get(e["type"], e["type"]),
        "status": e["status"],
        "statusLabel": STATUS_LABELS.get(e["status"], e["status"]),
        "freePath": e["freePath"],
        "freePathLabel": FREEPATH_LABELS.get(e["freePath"], e["freePath"]),
        "platforms": e.get("platforms", []),
        "platformLabels": [PLATFORM_LABELS.get(p, p) for p in e.get("platforms", [])],
        "signupUrl": e.get("signupUrl", ""),
        "iosUrl": e.get("iosUrl", ""),
        "rulesUrl": e.get("rulesUrl", ""),
        "tosUrl": e.get("tosUrl", ""),
        "prizeUsd": prize,
        "prizeNote": e.get("prizeNote", ""),
        "minCashout": cashout,
        "payoutMethods": e.get("payoutMethods", []),
        "payoutText": payout,
        "eligibility": e.get("eligibility", ""),
        "restricted": e.get("restricted", ""),
        "verificationLevel": e.get("verification", {}).get("level", ""),
        "verificationSteps": e.get("verification", {}).get("steps", []),
        "signupSteps": e.get("signupSteps", []),
        "howToWin": e.get("howToWin", []),
        "howToGetMoney": e.get("howToGetMoney", []),
        "tosNotes": e.get("tosNotes", []),
        "redFlags": e.get("redFlags", []),
        "sources": sources,
        "officialSourceUrl": official_link,
        "officialSourceTitle": official_title,
        "refSourceUrl": ref_link,
        "refSourceTitle": ref_title,
        "refSourceTier": ref_tier,
        "lastChecked": e.get("lastChecked", ""),
        "unverified": unverified,
    })

entries.sort(key=lambda x: (x["type"], x["name"].lower()))
OUT.write_text(json.dumps({
    "reviewed": ledger.get("reviewed"),
    "pass": ledger.get("pass"),
    "total": len(entries),
    "byType": {t: sum(1 for x in entries if x["type"] == t) for t in TYPE_LABELS},
    "byStatus": {s: sum(1 for x in entries if x["status"] == s) for s in STATUS_LABELS},
    "byFreePath": {f: sum(1 for x in entries if x["freePath"] == f) for f in FREEPATH_LABELS},
    "unverifiedCount": sum(1 for x in entries if x["unverified"]),
    "entries": entries,
}, indent=2))
print("wrote", OUT, "entries:", len(entries), "unverified:", sum(1 for x in entries if x["unverified"]))
print("by type:", {t: sum(1 for x in entries if x["type"] == t) for t in TYPE_LABELS})
print("by status:", {s: sum(1 for x in entries if x["status"] == s) for s in STATUS_LABELS})
print("by freepath:", {f: sum(1 for x in entries if x["freePath"] == f) for f in FREEPATH_LABELS})
