#!/usr/bin/env node
/**
 * check-links.mjs — verifies every URL referenced by the site (T8).
 *
 * Sources of URLs:
 *   1. assets/data.js  — signupUrl, iosUrl, tosUrl, rulesUrl, sources[].url
 *   2. built *.html    — href="..." external links
 *
 * Classification:
 *   ok      2xx
 *   redirect 3xx (final URL recorded)
 *   blocked 401/403/405/429/999 — server refused the checker (may work in a
 *            browser); NOT counted as broken, listed for manual review
 *   broken  4xx (other), 5xx, DNS failure, timeout, malformed
 *
 * Writes reports/link-check.json (+ prints a summary).
 * Exit code: 0 always for `--report` mode; 1 if --strict and broken > 0.
 *
 * Usage: node scripts/check-links.mjs [--strict] [--timeout=15000] [--concurrency=8]
 */
import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const strict = args.includes("--strict");
const timeoutMs = Number((args.find((a) => a.startsWith("--timeout=")) || "").split("=")[1]) || 15000;
const concurrency = Number((args.find((a) => a.startsWith("--concurrency=")) || "").split("=")[1]) || 8;

/* ---------------- collect URLs ---------------- */
const urlMap = new Map(); // url -> { what: [labels], listingId }

function addUrl(url, what, listingId) {
  if (!url || typeof url !== "string") return;
  if (!/^https?:\/\//i.test(url.trim())) return; // mailto:, anchors, relative — not checked here
  const u = url.trim();
  if (!urlMap.has(u)) urlMap.set(u, { what: [], listingId: listingId || null });
  const e = urlMap.get(u);
  if (what && !e.what.includes(what)) e.what.push(what);
  if (listingId && !e.listingId) e.listingId = listingId;
}

// 1. data.js
{
  const src = readFileSync(join(root, "assets", "data.js"), "utf8");
  const ledger = new Function("window", src + "\n;return window.LEDGER;")({});
  for (const l of ledger.listings || []) {
    addUrl(l.signupUrl, "signupUrl", l.id);
    addUrl(l.iosUrl, "iosUrl", l.id);
    addUrl(l.tosUrl, "tosUrl", l.id);
    addUrl(l.rulesUrl, "rulesUrl", l.id);
    for (const s of l.sources || []) addUrl(s.url, `source(${s.tier})`, l.id);
  }
}

// 2. html files
for (const f of readdirSync(root).filter((n) => n.endsWith(".html"))) {
  const html = readFileSync(join(root, f), "utf8");
  for (const m of html.matchAll(/href="(https?:\/\/[^"]+)"/g)) addUrl(m[1], `page:${f}`);
  for (const m of html.matchAll(/src="(https?:\/\/[^"]+)"/g)) addUrl(m[1], `page:${f}`);
}

/* ---------------- check ---------------- */
const BLOCKED_CODES = new Set([401, 403, 405, 407, 429, 451, 999]);
const results = [];

async function checkOne(url, meta) {
  const started = Date.now();
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    let res = await fetch(url, {
      method: "GET",
      redirect: "follow",
      signal: ctrl.signal,
      headers: {
        "user-agent":
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36 (FreeContestLedger-LinkCheck/1.0)",
        accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      },
    });
    const code = res.status;
    // drain body so sockets free up
    try { await res.arrayBuffer(); } catch { /* ignore */ }
    let status = "ok";
    if (code >= 300 && code < 400) status = "redirect";
    else if (BLOCKED_CODES.has(code)) status = "blocked";
    else if (code >= 400) status = "broken";
    return {
      url, ...meta, status, code,
      finalUrl: res.url && res.url !== url ? res.url : undefined,
      ms: Date.now() - started,
    };
  } catch (err) {
    const msg = String((err && err.cause && err.cause.code) || (err && err.name) || err);
    const netErr = String((err && err.cause && err.cause.message) || err);
    // DNS/ENOTFOUND/ECONNREFUSED/timeout => broken
    return { url, ...meta, status: "broken", error: `${msg}: ${netErr}`.slice(0, 200), ms: Date.now() - started };
  } finally {
    clearTimeout(t);
  }
}

const entries = [...urlMap.entries()];
let i = 0;
async function worker() {
  while (i < entries.length) {
    const idx = i++;
    const [url, meta] = entries[idx];
    results.push(await checkOne(url, meta));
    if (results.length % 25 === 0) console.log(`checked ${results.length}/${entries.length}`);
  }
}
await Promise.all(Array.from({ length: concurrency }, worker));

results.sort((a, b) => a.url.localeCompare(b.url));
const counts = results.reduce((m, r) => ((m[r.status] = (m[r.status] || 0) + 1), m), {});
const report = { generatedAt: new Date().toISOString(), timeoutMs, counts, results };

mkdirSync(join(root, "reports"), { recursive: true });
writeFileSync(join(root, "reports", "link-check.json"), JSON.stringify(report, null, 2));

const md = [
  `# Link check (${report.generatedAt})`,
  ``,
  `Checked: ${results.length} · ok: ${counts.ok || 0} · redirect: ${counts.redirect || 0} · blocked: ${counts.blocked || 0} · broken: ${counts.broken || 0}`,
  ``,
  `## Broken`,
  ``,
  ...(results.filter((r) => r.status === "broken").map((r) => `- ${r.url} — ${r.code || r.error} — ${r.what.join(", ")} — listing: ${r.listingId || "-"}`)),
  ``,
  `## Blocked (manual review)`,
  ``,
  ...(results.filter((r) => r.status === "blocked").map((r) => `- ${r.url} — HTTP ${r.code} — ${r.what.join(", ")}`)),
].join("\n");
writeFileSync(join(root, "reports", "link-check.md"), md);

console.log(`\nChecked ${results.length}:`, counts);
if (strict && (counts.broken || 0) > 0) process.exit(1);
