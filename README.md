# Competition Checker

A Claude Code plugin for founders. Reviews startup competition T&Cs and produces a neutral, evidence-first scorecard across 7 founder-calibrated dimensions. You decide whether to apply.

## What it does

- **Input-agnostic**: paste a URL, drop a PDF path, attach a screenshot of the T&Cs page, or forward the email body
- **Evidence-first**: every flag quotes the clause verbatim with a source reference (`§7.2, p.4`)
- **Neutral by design**: scores friction per dimension but never says "apply" or "don't apply"
- **Omission detection**: flags what the T&Cs *don't* say — silence in legal documents defaults to the drafter's advantage
- **Investment-term deep dive**: when competitions offer investment as a prize, surfaces SAFE/convertible note terms, valuation caps, pro-rata rights, and flags when terms are left to post-selection negotiation
- **Negotiation context**: identifies which clauses are standard boilerplate vs. bespoke, compares against landscape norms, and cites public reports of founders who negotiated specific terms — all neutral, never prescriptive
- **Cross-competition comparison**: `/compare` puts 2–5 competitions side by side across all 7 dimensions in one view
- **Founder-personalized**: optional profile maps your entity type, stage, location, and goals against each competition's requirements — Fit Analysis shows structural alignment, ROI Factors shows the math
- **Diff over time**: re-checking the same competition surfaces what changed in the T&Cs
- **Community signal** (recurring comps only): themes from Reddit / HN / blogs / past-winner interviews — with source counts and verbatim quotes, never a sentiment score
- **Bypasses bot-blockers**: falls back to browser automation, vision-scroll extraction, and web-search corroboration when sites block AI fetchers
- **Reports surface in chat**: the full scorecard renders directly in the conversation — no file-opening required. Files are saved for archival and diffing.
- **Local**: everything stays on your machine. Nothing uploaded to third-party SaaS.

## Commands

| Command | What |
|---|---|
| `/check <url-or-path-or-text>` | Full review → scorecard + findings + omissions + negotiation context + fit/ROI (if profile exists) |
| `/compare <slug-a> <slug-b> [...]` | Side-by-side comparison of 2–5 competitions across all dimensions |
| `/sentiment <competition-name>` | Community signal only (themes + sources), no T&C analysis |
| `/diff <competition-name>` | Compare the two most recent checks of the same competition |
| `/watch <name> --deadline <date>` | Weekly T&C monitoring across multiple URLs; auto-deprecates after the deadline |
| `/unwatch <slug>` | Stop a watch early; applies the retention policy you chose at setup |
| `/watches` | List all active, paused, and archived watches |
| `/list` | Show all stored competition checks and dates |
| `/prune <slug> [--keep N]` | Remove older stored reports for a slug, keeping the N most recent (default 10) |

## Watch feature at a glance

- **Competition-centric**: `/watch "TechCrunch Disrupt 2026" --deadline 2026-10-15` watches every associated T&C URL weekly until the day after the deadline, then auto-archives.
- **Multiple URLs per competition**: rules PDF + FAQ + announcements page all tracked together. Notification specifies which URL changed.
- **Material changes only**: score shift ≥1 in any dimension, or any clause added/removed/reworded. Whitespace-only diffs stay silent.
- **Notifications** (you pick at setup): stdout (always), macOS/Linux desktop banner, Slack webhook, and/or drafted Gmail via MCP. Drafts only — the plugin never sends email autonomously.
- **Retention** (you pick at setup): keep archive indefinitely, keep for N days, or delete on expiry.

You can also just chat: *"review these T&Cs"*, *"is this pitch comp worth applying to"*, *"check this competition"* — the skill triggers automatically.

## The 7 dimensions

See `skills/competition-checker/RUBRIC.md` for full detail.

1. IP & ownership
2. Equity & financial (+ investment-term sub-rubric for SAFE/convertible note analysis)
3. Exclusivity & restraint
4. Publicity & data
5. Commitment cost
6. Jurisdiction & disputes
7. Prize mechanics

Each dimension includes **expected clauses** that are flagged when absent from the T&Cs.

## Founder profile (optional)

Set up once, use across all checks. See `skills/competition-checker/PROFILE.md`.

Your profile enables two extra report sections:
- **Fit Analysis**: structural alignment between your company and competition requirements (entity type, location, stage, team size)
- **ROI Factors**: time cost, financial cost, equity exposure, and prize expected value for your specific situation

Profile stays local. Override any field per-check with flags like `--stage funded --team-size 4`.

## Install

1. Clone or copy this directory into your Claude Code plugins location.
2. Install the PDF generator's Python deps:
   ```
   pip install -r scripts/requirements.txt
   ```
   (Requires Python 3.9+. WeasyPrint pulls in cairo/pango — on macOS: `brew install pango`.)
3. Restart Claude Code. Run `/check <competition-url>` in any workspace.

Reports render in chat and are saved to `./competition-reports/` in your current working directory.

## See it in action

Here's a real check run on **Perplexity's "Billion Dollar Build"** — a $1M seed investment competition announced April 2026. The T&Cs were embedded in a sandboxed iframe that blocked programmatic access; the tool fell back to vision extraction and web-search corroboration automatically.

### Scorecard

| # | Dimension | Score | Headline |
|---|-----------|:-----:|----------|
| 1 | IP & Ownership         | 7? | Worldwide royalty-free promotional license covering code, concepts, workflows, and founder likenesses; no restriction on sponsor building competing products |
| 2 | Equity & Financial     | 7 | Investment framed as prize but is not a prize; requires Delaware C-Corp incorporation; acceptance of equity terms is a condition of receiving funds |
| 3 | Exclusivity & Restraint| 4? | Mandatory use of Perplexity Computer platform during competition; no explicit non-compete or fundraising freeze identified |
| 4 | Publicity & Data       | 8 | Perpetual royalty-free license over founder likenesses, demos, and company name for marketing; full access to all participant queries and workflow data during competition |
| 5 | Commitment Cost        | 5 | 8-week commitment; live-streamed pitch event; all participant costs unreimbursed unless separate written agreement |
| 6 | Jurisdiction & Disputes| 6? | Class action waiver; indemnification obligations on entrant; sponsor may disqualify at sole discretion |
| 7 | Prize Mechanics        | 8 | Investment at sponsor's sole discretion (zero to three+ winners); credits at Perplexity's discretion; no obligation to invest in any participant |

### What the tool caught

Every flag includes the verbatim clause and a location reference. Some highlights:

> *"does not restrict Perplexity, Perplexity Fund, or their affiliates from independently developing, creating, investing in, or pursuing products, services, companies, or ideas similar to or competitive with any submission."*

> *"a worldwide, royalty-free promotional licence to use their company name, product, code, concepts, workflows, founder likenesses and demo footage for marketing, investor relations, and other commercial purposes without further consent or compensation."*

> *"retains the right to access and review all Perplexity Computer queries, prompts, task outputs, workflow data and related account activity of registered participants during the competition period."*

> *"Perplexity Fund is under no obligation to invest in any participant."*

The tool flagged this as structurally unusual: the investment is explicitly "not a prize, grant, or gift" while being positioned as the headline reward. The founder competes for 8 weeks for an offer whose equity terms they cannot evaluate until after winning.

No verdict. No "don't apply." Just the clauses, the scores, and the structural notes. You decide.

[Full report →](competition-reports/examples/the-billion-dollar-build-2026-04-12.md)

---

## Neutrality guarantee

The skill is instructed — structurally — never to prescribe. It will not say "aggressive," "concerning," "unacceptable," "you should," "we recommend," or equivalent. Neutral descriptors like "broader than typical" or "perpetual term" are allowed. The negotiation context section surfaces landscape facts and public reports — it never says "negotiate this." The scorecard surfaces facts; you decide.
