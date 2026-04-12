# Competition Checker

A Claude Code plugin for founders. Reviews startup competition T&Cs and produces a neutral, evidence-first scorecard across 7 founder-calibrated dimensions. You decide whether to apply.

## What it does

- **Input-agnostic**: paste a URL, drop a PDF path, attach a screenshot of the T&Cs page, or forward the email body
- **Evidence-first**: every flag quotes the clause verbatim with a source reference (`§7.2, p.4`)
- **Neutral by design**: scores friction per dimension but never says "apply" or "don't apply"
- **Three outputs every run**: markdown scorecard, JSON sidecar, and a styled PDF
- **Diff over time**: re-checking the same competition surfaces what changed in the T&Cs
- **Community signal** (recurring comps only): themes from Reddit / HN / blogs / past-winner interviews — with source counts and verbatim quotes, never a sentiment score
- **Bypasses bot-blockers**: falls back to browser automation (via `browse` / `gstack` / Computer Use) when sites serve Cloudflare challenges or JS walls to plain fetchers
- **Local**: everything stays on your machine. Nothing uploaded to third-party SaaS.

## Commands

| Command | What |
|---|---|
| `/check <url-or-path-or-text>` | Full review → markdown + JSON + PDF (includes community scan if recurring) |
| `/sentiment <competition-name>` | Community signal only (themes + sources), no T&C analysis |
| `/diff <competition-name>` | Compare the two most recent checks of the same competition |
| `/watch <name> --deadline <date>` | Weekly T&C monitoring across multiple URLs; auto-deprecates after the deadline |
| `/unwatch <slug>` | Stop a watch early; applies the retention policy you chose at setup |
| `/watches` | List all active, paused, and archived watches |
| `/list` | Show all stored competition checks and dates |
| `/prune <slug> [--keep N]` | Remove older stored reports for a slug, keeping the N most recent (default 10). Never deletes sidecars referenced by active watches. |

## Watch feature at a glance

- **Competition-centric**: `/watch "TechCrunch Disrupt 2026" --deadline 2026-10-15` watches every associated T&C URL weekly until the day after the deadline, then auto-archives.
- **Multiple URLs per competition**: rules PDF + FAQ + announcements page all tracked together. Notification specifies which URL changed.
- **Material changes only**: score shift ≥1 in any dimension, or any clause added/removed/reworded. Whitespace-only diffs stay silent.
- **Notifications** (you pick at setup): stdout (always), macOS/Linux desktop banner, Slack webhook, and/or drafted Gmail via MCP. Drafts only — the plugin never sends email autonomously.
- **Retention** (you pick at setup): keep archive indefinitely, keep for N days, or delete on expiry. File-deletion opt-in is separate from record deletion.
- **URL-only fallback**: `/watch <url>` for rolling programs without a fixed deadline.

You can also just chat: *"review these T&Cs"*, *"is this pitch comp worth applying to"*, *"check this competition"* — the skill triggers automatically.

## The 7 dimensions

See `skills/competition-checker/RUBRIC.md` for full detail.

1. IP & ownership
2. Equity & financial
3. Exclusivity & restraint
4. Publicity & data
5. Commitment cost
6. Jurisdiction & disputes
7. Prize mechanics

## Install

1. Clone or copy this directory into your Claude Code plugins location.
2. Install the PDF generator's Python deps:
   ```
   pip install -r scripts/requirements.txt
   ```
   (Requires Python 3.9+. WeasyPrint pulls in cairo/pango — on macOS: `brew install pango`.)
3. Restart Claude Code. Run `/check <competition-url>` in any workspace.

Reports are saved to `./competition-reports/` in your current working directory.

## Neutrality guarantee

The skill is instructed — structurally — never to prescribe. It will not say "aggressive," "concerning," "unacceptable," "you should," "we recommend," or equivalent. Neutral descriptors like "broader than typical" or "perpetual term" are allowed. The scorecard surfaces facts; you decide.

## Scope

v0.1 covers T&C analysis + diff. A future version may add competition-metadata enrichment (prize size, deadlines, past winners) but the legal-surface read is the core differentiator.
