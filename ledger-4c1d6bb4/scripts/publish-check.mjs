#!/usr/bin/env node
/**
 * publish-check.mjs — reads reports/link-check.json and publishes a GitHub
 * check-run summary via the API (api.github.com), so link results are readable
 * even where Actions log/artifact hosts are unreachable.
 *
 * Env: GITHUB_TOKEN (or GH_TOKEN), GITHUB_REPOSITORY, GITHUB_SHA
 */
import { readFileSync, writeFileSync } from "node:fs";
import { execSync } from "node:child_process";

const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
const repo = process.env.GITHUB_REPOSITORY;
const sha = process.env.GITHUB_SHA;
if (!token || !repo || !sha) {
  console.log("Missing env; skipping check-run publish.");
  process.exit(0);
}

let title = "Link check report";
let summary = "No report generated.";
let conclusion = "neutral";
try {
  const r = JSON.parse(readFileSync("reports/link-check.json", "utf8"));
  const c = r.counts || {};
  const broken = (r.results || []).filter((x) => x.status === "blocked" ? false : x.status === "broken");
  const blocked = (r.results || []).filter((x) => x.status === "blocked");
  title = `Link check: ${c.ok || 0} ok · ${c.redirect || 0} redirect · ${blocked.length} blocked · ${broken.length} broken`;
  conclusion = broken.length === 0 ? "success" : "neutral"; // broken links are published on /flagged, not fatal
  summary = [
    `Checked **${r.results.length}** unique URLs on ${r.generatedAt}.`,
    "",
    "| status | count |",
    "|---|---|",
    ...["ok", "redirect", "blocked", "broken"].map((s) => `| ${s} | ${c[s] || 0} |`),
    "",
    "## Broken links (published on the Flagged for Review page)",
    "",
    ...(broken.length
      ? broken.map((b) => `- ${b.url} — \`${b.code || b.error || "?"}\` — ${(b.what || []).join(", ")} — listing: \`${b.listingId || "-"}\``)
      : ["- none"]),
    "",
    "## Blocked (server refused the checker; may work in a browser)",
    "",
    ...(blocked.length
      ? blocked.map((b) => `- ${b.url} — HTTP ${b.code}`)
      : ["- none"]),
  ].join("\n");
} catch (e) {
  title = "Link check failed to run";
  summary = String(e);
  conclusion = "failure";
}

writeFileSync("/tmp/check-summary.md", summary);
const fields = [
  "name=Link check report",
  `head_sha=${sha}`,
  "status=completed",
  `conclusion=${conclusion}`,
  `output[title]=${title}`,
];
execSync(
  `gh api repos/${repo}/check-runs ${fields.map((f) => `-f '${f}'`).join(" ")} -F output[summary]=@/tmp/check-summary.md`,
  { stdio: "inherit" }
);
console.log(title);
