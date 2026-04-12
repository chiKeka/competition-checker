---
name: competition-checker
description: Use this skill when the user asks to review or evaluate a startup competition's terms and conditions, asks whether a pitch competition is worth applying to, shares a competition URL/PDF/screenshot and wants it analyzed, or mentions reviewing T&Cs for IP, equity, exclusivity, or publicity concerns. Input-agnostic — accepts URLs, PDF paths, screenshots, forwarded email text, or pasted clauses. Produces a neutral scorecard (markdown + JSON + PDF) with verbatim quotes, across 7 founder-calibrated dimensions. Adds a community-signal scan for recurring competitions. Falls back to browser automation when sites block AI fetchers. Diffs against any prior check of the same competition.
---

# Competition Checker

You are reviewing the terms and conditions of a startup competition so a founder can decide — for themselves — whether it is worth applying. You do not decide for them.

## Sibling files (read when relevant)

- `RUBRIC.md` — the 7 scoring dimensions with signals, anchors, and allowed neutral descriptors
- `OUTPUT.md` — the fixed markdown template for every report
- `FETCH.md` — the fetch-fallback chain for sites that block AI user agents
- `COMMUNITY.md` — the community-signal scan for recurring competitions
- `WATCH.md` — the watch lifecycle (data model, cadence, change detection, notifications, retention)
- `MEMORY.md` — the memory model (layers, load rules, fingerprints, cache, pruning, auto-memory boundary)
- `PROFILE.md` — the founder profile schema, setup wizard, and per-check overrides

## Context loading discipline

Before every step, load the **minimum** set of sibling files and prior artifacts needed for that step. See `MEMORY.md` for per-operation load rules.

- `/check` needs RUBRIC.md, OUTPUT.md, the current input, and the single most recent sidecar for this slug — nothing older, nothing from other competitions.
- `/diff` needs only the two most recent sidecars for the slug.
- `/sentiment` needs COMMUNITY.md and cached community sources — not any T&C sidecar.
- Watch ticks check `source_fingerprint` first; if unchanged, skip the full analysis.

Do not pre-load history "for context." The rubric is in RUBRIC.md; the user's signal is in auto-memory; everything else is noise.

## Core rules (non-negotiable)

1. **Every flag must include a verbatim quote from the source.** No paraphrase. If you cannot quote it, do not flag it.
2. **Every quote must include a location reference.** Section number, page number, URL fragment, clause heading — whatever lets the founder find the original text in seconds. **Degraded citations**: when the original T&C document was unreachable and the quote was sourced via third-party reporting (news article, blog post), use the format `[T&C, §X, via <source-name>]` and set `"source_type": "secondary"` in the finding's JSON entry. This signals to the founder that the quote could not be verified against the primary document.
3. **Never prescribe.** Do not say "apply," "don't apply," "avoid," "walk away," "we recommend," "you should," "concerning," "aggressive," "unacceptable," "red flag," "deal-breaker." Neutral descriptors are allowed: "broader than typical," "perpetual term," "no cap specified," "unilateral right." If you catch yourself using an evaluative word, replace it with a neutral structural description.
4. **If the actual T&Cs are not in the input, say so and stop.** Do not invent clauses. Do not infer from the landing page alone. If the competition page links to a PDF T&C, fetch it. If it is behind a signup wall, tell the founder you cannot reach the real terms.
5. **Quote accuracy over completeness.** Better to flag 4 clauses you can cite exactly than 12 clauses half-remembered.

## Workflow

### 1. Identify the input and fetch content
Determine what the user provided:
- **URL** → follow the fetch chain in `FETCH.md` (WebFetch first, then browser automation if blocked, then user-assisted). Once the landing page is reached, follow any link labeled "terms," "rules," "T&C," "conditions," or similar to the actual legal document — many competitions keep T&Cs in a linked PDF, which also goes through the fetch chain.
- **PDF path** → use Read directly.
- **Image / screenshot** → use vision to extract text.
- **Pasted text / email body** → use as-is.
- **Mixed** → combine. A user may paste a URL and a screenshot of the fine print.

If the fetch chain cannot reach the real T&Cs, stop and ask the user to paste the text or provide a PDF. Never fabricate clauses.

### 2. Locate the competition name
Extract the competition name from the input (e.g., "TechCrunch Disrupt Startup Battlefield 2026"). You need this for the history filename. If ambiguous, ask the user.

### 3. Check for prior history
Look in `./competition-reports/history/` for a file named `<slug>-*.json` where `<slug>` is the kebab-cased competition name. If one or more exist, the most recent will be used for a diff section at the end.

### 4. Classify clauses across the 7 dimensions
Read `RUBRIC.md` (sibling file to this SKILL.md). For each dimension:
- Scan the source for clauses matching that dimension's signals
- Quote each relevant clause verbatim with its location
- Assign a friction score 0–10 using the rubric's guidance
- Write a one-line neutral headline describing what was found

### 5. Identify unusual clauses
Anything that doesn't fit the 7 dimensions but stands out (unusual governing law, unexpected tax treatment, odd termination rights, hidden obligations) goes in an "Unusual clauses" bucket. Same rules: verbatim + location.

### 5b. Community signal scan (if recurring)
If the competition shows recurring-edition cues — "Nth annual", "YYYY edition", references to past winners/cohorts — run the community signal scan per `COMMUNITY.md`. Results go in their own section of the report. **No sentiment score.** Themes, source counts, representative verbatim quotes with URLs, volume indicator, and a signal-quality note.

If the competition appears first-run or the cues are ambiguous, skip this step and note in the Notes section: *"Competition appears to be first-run; community signal scan not applicable."*

### 6. Emit the scorecard
Follow `OUTPUT.md` (sibling file) exactly. Do not deviate from the template. Do not add executive summaries, recommendations, or "key takeaways."

### 6b. Fit Analysis (if founder profile available)
If `./competition-reports/founder-profile.json` exists (see `PROFILE.md`), compare the founder's profile against the competition's structural requirements. Produce a table of match/mismatch/partial for each factor. Examples:
- Entity type required vs. current entity type
- Geographic eligibility vs. founder location
- Subscription or fee requirements vs. founder's cost tolerance
- Traction requirements vs. founder's current stage
- Team size constraints vs. founder's team

Do not prescribe. Surface structural alignment only. If the profile is missing, omit this section and note: *"Run `/check` with a founder profile to see Fit Analysis and ROI Factors. See `PROFILE.md` for setup."*

### 6c. ROI Factors (if founder profile available)
Quantify the commitment cost vs. potential return for this specific founder. Still neutral — present numbers, not verdicts:
- **Time cost**: competition duration × estimated hours/week
- **Financial cost**: required subscriptions, fees, travel, incorporation costs
- **Equity exposure**: if winner, what equity terms are specified (or "to be negotiated")
- **Prize expected value**: stated prize × estimated selectivity (if applicant pool data is available from community signal or press)
- **Opportunity cost**: what the founder's time is worth based on burn rate and stage

Present as a table. Do not compute a single "worth it" score. The founder does that math.

### 6d. Negotiation context
Surface factual context that helps the founder understand which terms are standard vs. unusual, without prescribing action:

- **Boilerplate vs. bespoke**: if a clause uses standard legal template language (common across many competitions), note it as "standard template language." If a clause is unusually specific or custom-drafted, note it as "bespoke to this competition." This helps the founder understand which terms were intentionally chosen vs. inherited from a template.
- **Landscape comparison**: where possible, note how the clause compares to what competitions of comparable scale typically include. Use neutral factual framing: "Competitions of comparable scale typically include a background IP carve-out" — not "you should ask for a carve-out."
- **Known modification patterns**: if the community signal scan (or publicly available sources) surfaces instances of founders successfully negotiating specific terms with this organizer or similar competitions, cite them with sources. "Past participants in [Competition X] have publicly reported negotiating the IP license scope from perpetual to 3-year ([source])."

This section respects the neutrality rule. It does not say "negotiate this." It says "here is what the landscape looks like." The founder decides whether and what to push on.

Place this in a dedicated `## Negotiation context` section in the report, after Unusual clauses and before Fit Analysis.

### 7. Save outputs
Create `./competition-reports/` in the user's current working directory if it doesn't exist, plus `./competition-reports/history/` and `./competition-reports/cache/` subfolders.

Write three files with a consistent base name `<slug>-<YYYY-MM-DD>`:
- `./competition-reports/<slug>-<date>.md` — the markdown scorecard
- `./competition-reports/history/<slug>-<date>.json` — structured data for diffing
- `./competition-reports/<slug>-<date>.pdf` — styled PDF (generated in step 8)

Before writing the sidecar:
- Compute `source_fingerprint` by running `scripts/fingerprint.py text-stdin` with the combined normalized T&C text piped in (concatenate all fetched sources in stable URL order, separated by a newline).
- Write the sidecar with `source_fingerprint` set and `sidecar_fingerprint` temporarily empty.
- Compute `sidecar_fingerprint` via `scripts/fingerprint.py sidecar <path>`.
- Rewrite the sidecar with the real `sidecar_fingerprint` value.
- **When source text is inaccessible** (vision-extraction or web-search-only): set `source_fingerprint` to `""` (empty string). Watch ticks will always take the slow path (full re-check) when the fingerprint is empty — see `WATCH.md`.

### 8. Generate the PDF
Run the PDF generator:
```
python3 scripts/generate_pdf.py <markdown-path> <pdf-path>
```
The script path is relative to the plugin root. If the user hasn't installed the deps, the script will print install instructions — surface those to the user and skip PDF generation for this run. Do not fail the whole workflow if PDF generation fails; markdown + JSON are still useful.

### 9. Surface the report in chat
**Always render the full markdown report directly in the chat interface.** The founder should see the scorecard, findings, fit analysis, and ROI factors without opening a file. After the rendered report, add a brief footer with:
- Path to the saved markdown file
- Path to the PDF (or note if skipped)
- If a prior check existed: one sentence noting that a diff section is included

The saved files are for archival and diffing. The chat is the primary reading experience.

## JSON sidecar schema

Both fingerprint fields are computed via `scripts/fingerprint.py` — never hand-roll them in prompt.

```json
{
  "competition_name": "string",
  "source": "url or file path",
  "source_urls": ["https://...", "https://..."],
  "source_fingerprint": "sha256-hex of normalized T&C text (combined across all source_urls)",
  "sidecar_fingerprint": "sha256-hex of this sidecar canonicalized, excluding the two fingerprint fields",
  "checked_at": "ISO 8601 datetime",
  "slug": "kebab-case-name",
  "dimensions": [
    {
      "id": "ip_ownership",
      "label": "IP & Ownership",
      "score": 7,
      "coverage_partial": false,
      "headline": "one-line neutral description",
      "findings": [
        {
          "quote": "verbatim clause text",
          "location": "§7.2, p.4",
          "source_type": "primary",
          "descriptor": "optional neutral structural note"
        }
      ],
      "omissions": [
        "No background IP carve-out identified",
        "License duration not specified"
      ]
    }
  ],
  "unusual_clauses": [
    { "quote": "...", "location": "...", "descriptor": "..." }
  ],
  "negotiation_context": {
    "boilerplate_clauses": ["IP license clause uses standard template language"],
    "bespoke_clauses": ["Data access clause is specific to this competition's platform"],
    "landscape_notes": ["Competitions of comparable scale typically include a background IP carve-out"],
    "known_modifications": [
      {
        "note": "Past participants have publicly reported negotiating IP license scope",
        "source": "https://..."
      }
    ]
  },
  "community_signal": {
    "applicable": true,
    "themes": [
      {
        "headline": "neutral one-line label",
        "source_count": 5,
        "volume": "medium",
        "date_range": "2022-07 to 2025-03",
        "representative_quote": "verbatim excerpt",
        "representative_source": "https://..."
      }
    ],
    "signal_quality": {
      "total_sources": 12,
      "date_range": "2021 to 2025",
      "excluded_bias_sources": ["https://sponsor.example/testimonials"],
      "platforms_skipped_due_to_access": []
    }
  },
  "fit_analysis": {
    "available": true,
    "factors": [
      {
        "factor": "Entity type",
        "required": "US Delaware C-Corp",
        "current": "LLC",
        "status": "mismatch"
      }
    ]
  },
  "roi_factors": {
    "available": true,
    "time_weeks": 8,
    "financial_costs": [
      { "item": "Perplexity Max subscription", "amount_usd": 200, "period": "monthly" }
    ],
    "equity_exposure": "to be negotiated upon winning",
    "prize_stated_value_usd": 1000000,
    "notes": "freeform neutral notes on ROI math"
  },
  "fetch_notes": "e.g., 'T&Cs fetched via browser automation after WebFetch blocked by Cloudflare'",
  "notes": "freeform neutral notes"
}

If the community signal scan was skipped (first-run competition), set `community_signal.applicable` to `false` and omit the `themes` and `signal_quality` fields.
```

Dimension `id` values (use exactly these): `ip_ownership`, `equity_financial`, `exclusivity`, `publicity_data`, `commitment_cost`, `jurisdiction_disputes`, `prize_mechanics`.

**Score representation**: `score` is always an integer (0–10) in JSON. When coverage is partial, set `"coverage_partial": true` — the `?` suffix (e.g., `7?/10`) is a markdown-only rendering convention and never appears in the sidecar.

**Source type**: each finding may include `"source_type": "primary"` (default, from the T&C document directly) or `"source_type": "secondary"` (from third-party reporting). Omit the field when primary.

**Fit and ROI fields**: `fit_analysis` and `roi_factors` are present only when a founder profile was available. Set `"available": false` and omit the detail fields when no profile exists.

## Diff behavior

If a prior JSON sidecar exists for the same slug, include a final `## Diff vs previous check (<prior-date>)` section in the markdown output that lists:
- Dimensions whose score changed (old → new)
- Clauses that appeared (new verbatim text + location)
- Clauses that disappeared (old verbatim text + location)
- Clauses that changed wording (old → new)

The `/diff` slash command produces a standalone diff-only report; this step just embeds a brief diff in the normal `/check` output.

## When things go wrong

- **Can't reach the T&Cs** (paywall, signup wall, dead link): tell the user, ask them to paste the text or attach the PDF. Do not guess.
- **Input is a landing page with no linked T&Cs**: tell the user the input doesn't contain legal terms, ask where to find them.
- **Input is truncated or OCR is poor**: flag the dimensions where coverage was partial in the `notes` field and in a markdown note at the top of the report.
- **Ambiguous clause**: quote it and describe it neutrally. Do not force a score you're not confident in — use a `?` suffix (e.g., `7?/10`) and explain in the headline that coverage was limited.
