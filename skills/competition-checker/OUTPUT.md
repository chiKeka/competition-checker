# Output template

Every markdown report follows this template exactly. Do not add sections. Do not remove sections. Do not write an executive summary, "key takeaways," or "our recommendation." The scorecard is the report.

---

```markdown
# Competition Checker — {{COMPETITION_NAME}}

**Source**: {{SOURCE_URL_OR_PATH}}
**Checked**: {{ISO_DATE}}
**Slug**: `{{SLUG}}`

{{OPTIONAL_COVERAGE_NOTE}}

---

## Scorecard

Friction scores run 0 (nothing unusual) to 10 (maximum founder-facing exposure). Scores describe structural surface area, not a verdict.

| # | Dimension | Score | Headline |
|---|-----------|:-----:|----------|
| 1 | IP & Ownership         | {{S1}} | {{H1}} |
| 2 | Equity & Financial     | {{S2}} | {{H2}} |
| 3 | Exclusivity & Restraint| {{S3}} | {{H3}} |
| 4 | Publicity & Data       | {{S4}} | {{H4}} |
| 5 | Commitment Cost        | {{S5}} | {{H5}} |
| 6 | Jurisdiction & Disputes| {{S6}} | {{H6}} |
| 7 | Prize Mechanics        | {{S7}} | {{H7}} |

Scores with partial coverage show a `?` suffix (e.g., `7?`). See the findings section for details on what could not be verified.

---

## Findings

### 1. IP & Ownership — {{S1}}/10
{{H1}}

- > "{{VERBATIM_QUOTE_1}}"
  `[{{LOCATION_1}}]` — {{OPTIONAL_NEUTRAL_DESCRIPTOR}}
- > "{{VERBATIM_QUOTE_2}}"
  `[{{LOCATION_2}}]`

### 2. Equity & Financial — {{S2}}/10
{{H2}}

- > "{{VERBATIM_QUOTE}}"
  `[{{LOCATION}}]`

### 3. Exclusivity & Restraint — {{S3}}/10
{{H3}}

- (same pattern)

### 4. Publicity & Data — {{S4}}/10
{{H4}}

- (same pattern)

### 5. Commitment Cost — {{S5}}/10
{{H5}}

- (same pattern)

### 6. Jurisdiction & Disputes — {{S6}}/10
{{H6}}

- (same pattern)

### 7. Prize Mechanics — {{S7}}/10
{{H7}}

- (same pattern)

---

## Unusual clauses

Clauses that do not fit the 7 dimensions but stand out.

- > "{{VERBATIM_QUOTE}}"
  `[{{LOCATION}}]` — {{NEUTRAL_DESCRIPTOR}}

(Omit this section entirely if empty. Do not write "none found" — just leave the section out.)

---

## Fit Analysis

*Structural alignment between your profile and competition requirements. Not a verdict.*

| Factor | Competition requires | Your profile | Status |
|--------|---------------------|--------------|--------|
| Entity type | {{REQUIRED_ENTITY}} | {{CURRENT_ENTITY}} | {{MATCH / MISMATCH / PARTIAL}} |
| Location | {{REQUIRED_LOCATION}} | {{FOUNDER_LOCATION}} | {{STATUS}} |
| Stage / traction | {{REQUIRED_TRACTION}} | {{CURRENT_STAGE}} | {{STATUS}} |
| Team size | {{REQUIRED_TEAM}} | {{CURRENT_TEAM}} | {{STATUS}} |
| Required subscription | {{REQUIRED_SUB}} | {{HAS_SUB}} | {{STATUS}} |

(Include only factors where the competition specifies a requirement. Omit this entire section — including the header — if no founder profile is available. In that case, add a note in the Notes section: *"Run `/check` with a founder profile to see Fit Analysis and ROI Factors. See `PROFILE.md` for setup."*)

---

## ROI Factors

*Commitment math for your situation. Numbers, not a verdict.*

| Factor | Value |
|--------|-------|
| Time commitment | {{N}} weeks, ~{{H}} hrs/week |
| Financial cost | {{ITEM}}: ${{AMOUNT}}/{{PERIOD}} |
| Equity exposure | {{EQUITY_TERMS_OR_TBD}} |
| Prize stated value | ${{PRIZE_VALUE}} ({{CONDITIONS}}) |
| Selectivity | {{KNOWN_OR_UNKNOWN}} |

(Omit this entire section — including the header — if no founder profile is available.)

---

## Community signal

*Lived-experience themes from past editions. Not a score. Surface, not verdict.*

### {{THEME_HEADLINE_1}}
- **Sources**: {{N}} ({{VOLUME_LOW_MEDIUM_HIGH}})
- **Date range**: {{EARLIEST}} – {{LATEST}}
- > "{{REPRESENTATIVE_QUOTE}}"
  — {{POSTER_OR_AUTHOR}}, {{DATE}}, [{{SOURCE_URL}}]({{SOURCE_URL}})

### {{THEME_HEADLINE_2}}
(same pattern)

### Signal quality
- **Total unique sources**: {{N}}
- **Date range covered**: {{EARLIEST}} – {{LATEST}}
- **Excluded as non-independent**: {{LIST_OR_NONE}} (e.g., sponsor's own testimonial page)
- **Access-limited platforms**: {{LIST_OR_NONE}} (e.g., X/Twitter requiring login)

(If the competition is first-run, omit this entire Community signal section — but note that fact in the Notes section below.)

---

## Notes

{{FREEFORM_NEUTRAL_NOTES}}

Examples: "T&Cs fetched from linked PDF at URL X." "Sections 1–4 analyzed; section 5 appeared truncated in source." "Governing-law clause references a schedule not included in the provided document."

(Omit this section if there is nothing to note.)

---

## Diff vs previous check ({{PRIOR_DATE}})

(Only include this section if a prior JSON sidecar exists for the same slug.)

### Score changes
- **IP & Ownership**: {{OLD_SCORE}} → {{NEW_SCORE}}
- (list only dimensions whose score changed)

### New clauses
- > "{{VERBATIM_QUOTE}}"
  `[{{LOCATION}}]` — appeared since previous check

### Removed clauses
- > "{{PRIOR_VERBATIM_QUOTE}}"
  `[{{PRIOR_LOCATION}}]` — absent from current version

### Reworded clauses
- **Then**: > "{{OLD_QUOTE}}" `[{{OLD_LOCATION}}]`
  **Now**:  > "{{NEW_QUOTE}}" `[{{NEW_LOCATION}}]`

---

*This report surfaces facts. It does not recommend action. The decision is yours.*
```

---

## Formatting rules

- Scores rendered as `{{SCORE}}/10`. Append `?` if coverage was partial (e.g., `6?/10`).
- Quotes use markdown blockquotes (`>`) inside a bulleted list so they render cleanly in both markdown viewers and the PDF.
- Location references use backticks so they stand out as references rather than prose.
- Dimension sections always appear in numerical order 1–7, even if a dimension scored 0 (write the section with a single line: "No relevant clauses identified.").
- If a dimension scored 0, the findings list for that dimension is empty (no bullets). The section header and the one-line headline still appear.
- The closing italic line (`*This report surfaces facts…*`) is mandatory — it is the structural reminder that this is not advice.
