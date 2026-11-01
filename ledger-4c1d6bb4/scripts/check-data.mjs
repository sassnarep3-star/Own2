#!/usr/bin/env node
/**
 * check-data.mjs — structural audit of the ledger (T3/T6 support).
 *
 * Rules enforced (per project verification policy):
 *  1. Every listing must carry at least one source URL.
 *  2. Every listing SHOULD carry at least one source with tier === "official".
 *     Listings without an official-tier source are UNVERIFIED: their prize
 *     value must be rendered blank and the row published on /flagged.html.
 *  3. No value is ever inferred. This script only reports; it never fills data.
 *
 * Outputs: reports/data-audit.json (machine) and reports/data-audit.md (human).
 */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const src = readFileSync(join(root, "assets", "data.js"), "utf8");

const sandbox = {};
// data.js assigns window.LEDGER; emulate a browser global.
const fn = new Function("window", src + "\n;return window.LEDGER;");
const ledger = fn(sandbox);

if (!ledger || !Array.isArray(ledger.listings)) {
  console.error("FATAL: window.LEDGER.listings not found in assets/data.js");
  process.exit(1);
}

const rows = [];
const unverified = [];
const noSources = [];

for (const item of ledger.listings) {
  const sources = item.sources || [];
  const official = sources.filter((s) => s.tier === "official");
  const row = {
    id: item.id,
    name: item.name,
    type: item.type,
    status: item.status,
    freePath: item.freePath,
    officialSourceCount: official.length,
    officialUrls: official.map((s) => s.url),
    allSources: sources.map((s) => ({ title: s.title, url: s.url, tier: s.tier })),
    lastChecked: item.lastChecked,
  };
  rows.push(row);
  if (sources.length === 0) noSources.push(row);
  if (official.length === 0) unverified.push(row);
}

// Sanity: unique ids, known types, known statuses, known freePath values.
const ids = new Set();
const dupIds = [];
const unknownType = [];
const unknownStatus = [];
const unknownFreePath = [];
const knownTypes = new Set((ledger.types || []).map((t) => t.id));
for (const item of ledger.listings) {
  if (ids.has(item.id)) dupIds.push(item.id);
  ids.add(item.id);
  if (!knownTypes.has(item.type)) unknownType.push(item.id);
  if (!["live", "ended", "caution", "mixed", "inactive"].includes(item.status))
    unknownStatus.push(item.id);
  if (!["full", "partial", "paid-cash"].includes(item.freePath))
    unknownFreePath.push(item.id);
}

// URL well-formedness for signup + rules (the per-row source links shown on tables).
const badUrls = [];
for (const item of ledger.listings) {
  for (const [field, u] of [["signupUrl", item.signupUrl], ["rulesUrl", item.rulesUrl]]) {
    if (!u) continue;
    try {
      const parsed = new URL(u);
      if (!/^https?:$/.test(parsed.protocol)) badUrls.push({ id: item.id, field, url: u, why: "non-http(s)" });
    } catch {
      badUrls.push({ id: item.id, field, url: u, why: "malformed" });
    }
  }
  for (const s of item.sources || []) {
    try {
      const parsed = new URL(s.url);
      if (!/^https?:$/.test(parsed.protocol)) badUrls.push({ id: item.id, field: "sources", url: s.url, why: "non-http(s)" });
    } catch {
      badUrls.push({ id: item.id, field: "sources", url: s.url, why: "malformed" });
    }
  }
}

const report = {
  generatedAt: new Date().toISOString(),
  listingCount: ledger.listings.length,
  duplicateIds: dupIds,
  unknownType,
  unknownStatus,
  unknownFreePath,
  malformedUrls: badUrls,
  listingsWithoutAnySource: noSources,
  listingsWithoutOfficialSource: unverified,
};

mkdirSync(join(root, "reports"), { recursive: true });
writeFileSync(join(root, "reports", "data-audit.json"), JSON.stringify(report, null, 2));

const md = [
  `# Data audit (${report.generatedAt})`,
  ``,
  `Listings: ${report.listingCount}`,
  `Duplicate ids: ${report.duplicateIds.length}`,
  `Unknown type: ${report.unknownType.length}`,
  `Unknown status: ${report.unknownStatus.length}`,
  `Unknown freePath: ${report.unknownFreePath.length}`,
  `Malformed URLs: ${report.malformedUrls.length}`,
  `Listings with no source at all: ${report.listingsWithoutAnySource.length}`,
  `Listings with no OFFICIAL source (UNVERIFIED, prize shown blank): ${report.listingsWithoutOfficialSource.length}`,
  ``,
  `## Unverified listings`,
  ``,
  `| id | name | sources present |`,
  `|---|---|---|`,
  ...report.listingsWithoutOfficialSource.map(
    (r) => `| ${r.id} | ${r.name} | ${r.allSources.map((s) => `${s.tier}: ${s.url}`).join("<br>")} |`
  ),
  ``,
].join("\n");
writeFileSync(join(root, "reports", "data-audit.md"), md);

console.log(`Listings: ${report.listingCount}`);
console.log(`Unverified (no official source): ${report.listingsWithoutOfficialSource.length}`);
console.log(`Malformed URLs: ${report.malformedUrls.length}`);
if (dupIds.length || unknownType.length || unknownStatus.length || unknownFreePath.length || badUrls.length) {
  console.error("STRUCTURAL PROBLEMS FOUND — see reports/data-audit.json");
  process.exit(2);
}
console.log("OK: structural audit clean (unverified rows are expected and flagged).");
