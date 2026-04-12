# Community signal scan

For **recurring competitions**, lived experience from past cohorts surfaces what the T&Cs cannot — delayed prize payments, mentor quality, judging fairness, post-competition support, hidden obligations that only appeared in practice. This file defines how the skill gathers and presents that signal neutrally.

## When to run

Trigger the community scan automatically when the source or user input contains recurring-competition cues:

- "Nth annual" / "Xth edition"
- A year suffix in the official name (e.g., "Disrupt 2026")
- References to past winners, past cohorts, prior editions
- The founder explicitly requests a sentiment check, or invokes `/sentiment`

If the competition is first-run or ambiguous, **skip the community section entirely** and note in the report's Notes: *"Competition appears to be first-run; community signal scan not applicable."* Do not speculate from thin sources.

## Sources (priority order)

1. **Reddit** — `r/startups`, `r/Entrepreneur`, `r/ycombinator`, competition-specific threads, city/country startup subs
2. **Hacker News** — past Show HN / Ask HN / comment threads
3. **Twitter / X** — public posts from past participants, judges, organizers
4. **Medium, Substack, personal blogs** — founder write-ups ("My experience at <comp>")
5. **Podcast / YouTube interviews** with past winners (use transcripts or show notes where available)
6. **Aggregators** — F6S reviews, startup-review sites if the competition is listed
7. **Wayback Machine snapshots** of past T&Cs — useful for detecting silent year-over-year clause changes when the official site only shows the current version

## Process

1. **Search** via WebSearch for these query variants (substitute the competition name):
   - `"<comp>" review`
   - `"<comp>" reddit`
   - `"<comp>" hackernews`
   - `"<comp>" experience`
   - `"<comp>" winner interview`
   - `"<comp>" scam` *(deliberately included — if founders are describing a competition this way, you need to see it; if no results, that's useful signal of absence)*
   - `site:news.ycombinator.com "<comp>"`
   - `site:reddit.com "<comp>"`

2. **Fetch** each candidate source. Use the FETCH.md fallback chain if a source is blocked. Community-source caching: 7-day TTL via the same cache convention as T&C fetches (see FETCH.md). On the second weekly run for the same competition, most sources will be cache hits — only re-search for *new* results since the last scan, don't re-fetch every URL.

3. **Target 10–25 unique sources.** Stop earlier if signal converges strongly; stop earlier if the competition is niche and coverage is thin. Never pad with low-relevance hits to hit a count.

4. **Cluster into themes.** Aim for 3–7 themes with descriptive neutral labels. Examples:
   - *"Prize disbursement timing"*
   - *"Mentor access after demo day"*
   - *"Judging transparency"*
   - *"Post-competition equity negotiations"*
   Don't force clusters — if only two themes emerge, list two.

5. **Per theme, record:**
   - **Source count**: how many independent sources mention it
   - **Volume indicator**: `low` (1–2 sources), `medium` (3–6), `high` (7+)
   - **Date range**: earliest–latest mention
   - **Representative quote**: one verbatim excerpt, with the source URL and poster/date where available
   - **Neutral headline**: one line describing what the theme contains, not whether it's good or bad

6. **Signal quality block** — a short sub-section noting:
   - Total unique sources found
   - Date range of sources
   - Obvious bias sources excluded (e.g., the sponsor's own testimonial page — note that it exists but was not counted as independent signal)
   - Whether the scan reached paywalled/login-walled platforms or skipped them

## Hard rules

- **No sentiment score.** Do not produce "70% positive", "4.2/5 stars", or a 0–10 community friction score. Sentiment reduction is lossy and nudges the founder toward a prescribed view.
- **No characterization of organizer intent.** You can quote "several 2023 participants reported delayed prize payments" with sources. You cannot say "the organizers are unreliable" or "the competition has integrity issues."
- **Every theme needs at least one verbatim quote with a real URL.** No paraphrased themes. No "sources say" without a source.
- **No undated signal.** If a source has no identifiable date, exclude it — stale grievances may be resolved.
- **No anonymous voices presented as authoritative.** A `u/throwaway123` comment is one voice; label it as such.
- **No fabricated URLs.** If WebFetch returned a page you can quote, include its real URL. If you can't quote verbatim from a fetched page, do not include that source.
- **Acknowledge absence as signal.** If searches returned almost nothing, that is itself worth noting (low profile, niche audience, or simply little public discussion). Say so — do not fill the section with weak hits.

## Output shape in the report

The community signal goes in its own section (see OUTPUT.md). It sits *after* the 7 dimensions and Unusual clauses, *before* Notes. It does not receive a friction score and does not roll into any aggregate — structurally separate from the legal-surface scorecard.
