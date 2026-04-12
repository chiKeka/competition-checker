# Rubric — 7 dimensions

Friction scores run 0 (nothing unusual) to 10 (maximum founder-hostile surface). Scores describe structural exposure, not a verdict. The founder decides whether the exposure is worth the prize.

For each dimension: **signals** (what to scan for), **anchors** (what different score levels look like), and **neutral descriptors** you may use.

---

## 1. IP & Ownership — `ip_ownership`

### Signals
- Assignment of submitted materials, pitch decks, demos, code, prototypes
- Licenses granted to the sponsor (scope, duration, territory, sublicensability, irrevocability)
- Background IP carve-outs (or lack of them)
- Derivative works rights
- Moral rights waivers
- Rights over post-competition work product
- Feedback/comments IP (who owns what the judges say)

### Anchors
- **0–2**: Entrant retains all IP. Sponsor gets no license, or a narrow license solely to administer the competition.
- **3–5**: Non-exclusive, limited-duration license for promotional use of the submission.
- **6–8**: Perpetual and/or worldwide and/or sublicensable license; or license covers derivatives.
- **9–10**: Outright assignment of submitted IP; or broad license over background IP; or rights over post-competition work.

### Neutral descriptors
"perpetual," "worldwide," "royalty-free," "sublicensable," "irrevocable," "covers derivatives," "no background IP carve-out," "assignment (not license)," "survives termination"

### Expected clauses (flag if absent)
- Background IP carve-out (entrant's pre-existing IP excluded from license)
- License scope limitation (what specifically is licensed — submission only, or broader)
- License duration (perpetual by default if silent — flag the silence)
- Post-competition IP reversion or termination of license rights
- Restriction on sponsor building competing products from submissions

---

## 2. Equity & Financial — `equity_financial`

### Signals
- Mandatory equity grant to sponsor as condition of entry or prize
- Right of first refusal (ROFR) on future rounds
- Pro-rata rights
- Most-favored-nation (MFN) clauses
- Convertible note / SAFE obligations
- Forced investment acceptance
- Application fees, participation fees, success fees
- Prize contingent on accepting investment terms

### Anchors
- **0–2**: No equity, no ROFR, no fees, or nominal entry fee only.
- **3–5**: Optional investment offer separate from prize; sponsor has a right to negotiate but no obligation on entrant.
- **6–8**: Mandatory ROFR or pro-rata for a defined window; non-trivial entry fee; MFN clause.
- **9–10**: Mandatory equity as condition of prize; forced acceptance of sponsor investment at predetermined terms; ROFR with no time limit.

### Neutral descriptors
"mandatory equity grant," "ROFR with no sunset," "MFN applies," "fee-to-enter of $X," "prize contingent on investment acceptance"

### Expected clauses (flag if absent)
- Equity percentage or cap specified before entry
- Investment instrument type (SAFE, convertible note, priced round)
- Valuation cap or discount rate stated
- Clear separation between prize and investment (are they contingent on each other?)

### Investment-term sub-rubric (activate when investment terms are detected)

When the competition offers investment as a prize or condition, surface these details in a dedicated sub-section under Equity & Financial. If any detail is absent, flag the absence explicitly — "investment terms to be negotiated post-selection" means the founder has no visibility into dilution at the time of entry.

| Term | What to surface |
|------|----------------|
| Instrument type | SAFE (pre-money / post-money), convertible note, priced equity, or unspecified |
| Valuation cap | Stated cap, uncapped, or not specified |
| Discount rate | Percentage, or not specified |
| Pro-rata rights | Present, absent, or not specified |
| MFN clause | Whether the investor gets most-favored-nation terms on future rounds |
| Information rights | Board observer seat, financial reporting requirements, or not specified |
| Side letters | Any non-standard terms attached to the investment |
| Anti-dilution | Broad-based weighted average, full ratchet, or not specified |
| Equity percentage | Fixed percentage, negotiable range, or "to be determined" |
| Investment contingencies | Due diligence, incorporation requirements, ongoing obligations |

**Scoring impact**: when investment is the prize and terms are not pre-defined, this adds +1–2 to the dimension score. The founder is being asked to compete for an offer whose terms they cannot evaluate until after winning. Note this in the headline.

---

## 3. Exclusivity & Restraint — `exclusivity`

### Signals
- Prohibition on entering other competitions during a window
- Fundraising freeze during competition period
- Non-compete during or after
- Exclusivity of relationship with sponsor (advisory, partnership)
- Commitment to use sponsor services/platforms
- Restrictions on announcing other partnerships

### Anchors
- **0–2**: No exclusivity. Entrant can pursue any parallel opportunity.
- **3–5**: Narrow, short-window exclusivity limited to identical competitions by direct rivals.
- **6–8**: Fundraising freeze during competition; broad no-parallel-competitions clause.
- **9–10**: Post-competition non-compete; long exclusivity window; mandatory sponsor-platform usage.

### Neutral descriptors
"fundraise freeze for N months," "no parallel competitions," "post-competition non-compete of N months," "exclusive advisory relationship"

### Expected clauses (flag if absent)
- Explicit statement that entrant may pursue parallel opportunities
- Time-bounded exclusivity window (if any exclusivity exists)
- Right to withdraw without penalty during the competition period

---

## 4. Publicity & Data — `publicity_data`

### Signals
- Rights over entrant's name, likeness, voice, logo, founder photos
- Recording rights over pitches, interviews, Q&A
- Ownership of pitch recordings
- Data sharing with sponsors, partners, judges
- Use of entrant data for sponsor marketing
- Press release consent (unilateral or mutual)
- Duration and scope of publicity rights (perpetual vs. competition period)

### Anchors
- **0–2**: Publicity rights limited to the competition period and promotional materials.
- **3–5**: Worldwide publicity rights during and shortly after competition.
- **6–8**: Perpetual publicity rights; pitch recordings owned by sponsor; data shared with named partners.
- **9–10**: Perpetual + irrevocable likeness rights across all media; data shared with unnamed third parties; no opt-out.

### Neutral descriptors
"perpetual publicity rights," "unilateral press release right," "pitch recording owned by sponsor," "data shared with unnamed third parties," "no media opt-out"

### Expected clauses (flag if absent)
- Data deletion or return clause post-competition
- Opt-out mechanism for ongoing publicity use
- Named list of third parties who receive data (vs. unnamed "partners")
- Duration limit on publicity rights

---

## 5. Commitment Cost — `commitment_cost`

### Signals
- Mandatory in-person attendance (duration, location, at whose expense)
- Accelerator residency requirements
- Reporting obligations post-prize (frequency, duration)
- Mentorship hours required
- Post-prize participation in sponsor events
- Travel cost allocation (entrant vs. sponsor)
- Visa / work-permit responsibility

### Anchors
- **0–2**: Remote participation; optional in-person events; sponsor covers travel.
- **3–5**: One-off in-person final; entrant covers travel but expenses reimbursed; light reporting.
- **6–8**: Multi-week in-person residency; quarterly reporting for 1+ year; significant time commitment.
- **9–10**: Multi-month relocation required; indefinite reporting obligations; entrant covers all travel with no reimbursement.

### Neutral descriptors
"N-week in-person residency," "quarterly reports required for N years," "entrant-funded travel," "relocation required," "no reimbursement specified"

### Expected clauses (flag if absent)
- Withdrawal/exit clause (can the entrant leave mid-competition without penalty?)
- Cost allocation specifics (who pays for what)
- Post-competition obligation duration (is it bounded or open-ended?)

---

## 6. Jurisdiction & Disputes — `jurisdiction_disputes`

### Signals
- Governing law
- Forum / venue for disputes
- Mandatory arbitration (and where)
- Class action waivers
- Indemnification obligations (scope, cap)
- Limitation of liability (scope, cap)
- Sponsor's unilateral right to modify terms
- Sponsor's right to disqualify at sole discretion

### Anchors
- **0–2**: Governing law and forum in entrant's jurisdiction (or neutral); mutual indemnity; liability caps stated.
- **3–5**: Governing law in sponsor's jurisdiction; forum matches; reasonable indemnity scope.
- **6–8**: Mandatory arbitration in a distant jurisdiction; one-way indemnity from entrant; uncapped entrant liability.
- **9–10**: Sponsor may modify terms unilaterally without notice; sole-discretion disqualification with no refund of costs; entrant indemnifies sponsor for third-party claims including sponsor's own negligence.

### Neutral descriptors
"governing law: [jurisdiction]," "mandatory arbitration in [location]," "one-way indemnity," "uncapped entrant liability," "sponsor may modify terms without notice"

### Expected clauses (flag if absent)
- Liability cap on entrant's exposure
- Mutual (not one-way) indemnification
- Notice period before sponsor can modify terms
- Grounds for disqualification (vs. "sole discretion" with no criteria)
- Dispute resolution mechanism

---

## 7. Prize Mechanics — `prize_mechanics`

### Signals
- Prize delivery conditions (milestones, deliverables, ongoing obligations)
- Clawback clauses (when can the prize be reclaimed)
- Tax treatment (explicit or silent)
- Prize form (cash, services, credits, in-kind)
- Contingencies (e.g., "subject to sponsor's discretion")
- Escrow or payment timing
- Currency and FX risk

### Anchors
- **0–2**: Cash prize, paid in full on award, no milestones, tax treatment addressed.
- **3–5**: Prize partly contingent on milestones but milestones are defined and reasonable; tax noted as entrant's responsibility.
- **6–8**: Prize is partly/fully in sponsor credits or services with expiration; milestones vague; clawback possible under broad conditions.
- **9–10**: Prize fully contingent on sponsor's sole discretion; clawback triggered by ambiguous events; prize is non-cash with no FX value specified; taxes silent.

### Neutral descriptors
"milestone-contingent release," "clawback on [event]," "prize form: sponsor credits expiring in N days," "tax treatment not specified," "release at sponsor's sole discretion"

### Expected clauses (flag if absent)
- Tax treatment (who is responsible, is withholding addressed)
- Payment timeline (when is the prize disbursed)
- Prize value in cash-equivalent terms (for non-cash prizes like credits)
- Conditions for prize forfeiture clearly enumerated
- Credit/service prize expiration date and transferability

---

## Omission detection

For each dimension, check the "Expected clauses" list above. When an expected clause is absent from the T&Cs, surface it in the report under a dedicated **"Not addressed"** sub-section within that dimension's findings. This is not about inflating the score — silence in legal documents defaults to the drafter's advantage. Flagging omissions gives the founder a checklist of questions to ask the organizer before signing.

Format in the report:
```
**Not addressed in these T&Cs:**
- No background IP carve-out identified
- License duration not specified (defaults to perpetual absent explicit limitation)
- No data deletion clause post-competition
```

In the JSON sidecar, omissions go in a sibling array to `findings`:
```json
"omissions": [
  "No background IP carve-out identified",
  "License duration not specified"
]
```

---

## Scoring discipline

- When a clause could fit multiple dimensions, score it under the dimension where the primary obligation lives, and cross-reference in the other's findings without double-counting the score.
- If a dimension has no clauses at all in the source, score it **0** and headline it as "No relevant clauses identified."
- If coverage was partial (truncated doc, poor OCR), suffix the score with `?` (e.g., `6?`) and note limited coverage in the headline.
- Never round scores to make them look cleaner. A 7 is a 7; don't bump it to 8 for emphasis.
- When a clause is quoted under multiple dimensions, note `(also cited under §N)` in the descriptor to signal the cross-reference. Do not inflate scores by counting the same clause twice.
