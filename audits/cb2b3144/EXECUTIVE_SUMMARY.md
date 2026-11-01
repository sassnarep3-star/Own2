# Executive summary — official-source competition supplement

**Audit date:** 2026-11-01 UTC · **Session:** cb2b3144

## Decision

The existing repository already contains a live, mobile-friendly main dashboard and a separate parallel dashboard. This session did not overwrite either. It adds ten event-level findings in an isolated supplement, with official source links on every row and blank fields where the organizer did not establish a fact.

For an AI coding-agent workflow, the strongest **new** targets are:

1. **Kiroween 2026** — $100,000 cash across USD award rows; December 4, 2026 at 2 p.m. Pacific. Kiro is mandatory, the repository must be public and open source, and the `/.kiro` directory must be included. Best longer-runway fit when those constraints are acceptable. [Official rules](https://kiroween.devpost.com/rules).
2. **Codegeist 2026** — $120,000 cash across USD award rows; December 22, 2026 at noon Pacific. Requires Atlassian Forge; agent, MCP, Teamwork Graph, and Marketplace bonus tracks. Confirm coding-assistant permission before relying on an autonomous agent. [Official rules](https://codegeist2026.devpost.com/rules).
3. **PayPal AI Hackathon** — $67,500 cash, excluding Render credits; November 12, 2026 at noon Pacific. Requires a working PayPal integration plus AI, a public open-source repository, and a demo. [Official rules](https://paypalaihackathon.devpost.com/rules).
4. **UGREEN AI NAS** — $46,000 cash; November 15, 2026 at 11:45 p.m. Pacific. No NAS purchase is required. Round 1 is a proposal/pre-test Skill package; up to 30 finalists receive free remote testing access. Arbitrary executables and scripts are not supported in the submitted Skill. [Official rules](https://ugreenhackathon.devpost.com/rules).
5. **Codex x TwitchCon** — $25,000 cash; November 2, 2026 at 2 p.m. Pacific. Explicitly requires Codex and a Codex session ID. Only pursue if a complete submission is feasible immediately. Missing the TwitchCon appearance does not forfeit the monetary award. [Official rules](https://twitchcon-codex.devpost.com/rules).

These are editorial fit recommendations, **not estimates of win probability or expected earnings**. The rules do not provide a reliable basis for calculating either.

## Important qualifications

- **Meta VR Start:** up to $1 million, but the submitting representative must be a Start member. Membership approval, practical hardware costs, and detailed coding-agent permission remain unverified. Do not treat the headline amount as an unrestricted opportunity. [Rules](https://start-developer-competition-26.devpost.com/rules).
- **NIH/NIDDK Kidney AI Discovery Challenge:** $100,000 cash; submissions open November 5, 2026 and end April 29, 2027. U.S. citizenship/permanent residency is required for an individual or team captain to receive cash. The announcement says final submission requirements are still being finalized; an explicit free-entry clause was not located. [Official challenge](https://www.herox.com/KidneyAI), [NIH challenge directory](https://www.nih.gov/challenges).
- **Blaise xTech Phase I:** ten $5,000 cash awards plus developer kits; extended to December 14, 2026. Valid Blaise-generated spectra are required. Phase I entry cost and payout mechanics remain unverified; 90 Phase II invitees face registration and shipping costs. [Official challenge](https://www.herox.com/xTechIdeaCompetition).
- **XPRIZE Quantum Applications:** the $5 million active competition has already selected seven finalists. New registration availability was not confirmed; exclude it from the active-entry shortlist. [Official competition](https://www.xprize.org/competitions/qc-apps).
- **HeroX link issue:** `/crowdsolve` returned page-not-found content. The retrieved working directory is `/crowdsourcing-projects`. Directory listings remain leads, not verified competitions. [Working directory](https://www.herox.com/crowdsourcing-projects).

## Repository and reference-site findings

The initial Own2 checkout contained only a six-byte README. Concurrent sessions subsequently built the main dashboard, category pages, review queue, and executive summary. Their work and claims were preserved. The reference ledger contains 206 listings, but its platform-level and inherited claims are not equivalent to event-level official verification.

This supplement does **not** claim that all 206 inherited entries or all external links have been verified. It checks the ten records listed here against organizer/administrator sources, records exact evidence in `evidence.json`, and publishes unresolved items on `flagged.html`.

## Recommended operating process

1. Choose one primary competition based on tool fit and available time, not the largest purse.
2. Read the complete current rules and confirm the live submission form before development.
3. Record required tool usage, original work, third-party licenses, and any AI assistance.
4. Build a functional demo and test it from clean setup instructions.
5. Check repository visibility, video visibility, deadline time zone, and team/entry limits.
6. Submit early and retain the submission receipt. Do not automate account creation, eligibility certification, or prize affidavits without the entrant's authorization.

## Deliverables and validation

- `index.html`: decision brief and shortlist.
- `all.html`: searchable findings table.
- `tech.html`, `research.html`, `directory.html`: category subpages.
- `flagged.html`: flags, source excerpts, and manual-review links.
- `methodology.html`: verification boundaries.
- `evidence.json`, `findings.csv`: machine-readable findings.
- `build.py`, `test.py`: deterministic static build and data/internal-link checks.

Build with `python audits/cb2b3144/build.py`; validate with `python audits/cb2b3144/test.py`. The final integration log in `COORDINATION.md` records the actual test, PR, merge, and deployment results.
