# Founder Profile

The founder profile enables the **Fit Analysis** and **ROI Factors** sections of the `/check` report. Without a profile, those sections are omitted and the report covers T&C analysis only.

## Storage

`./competition-reports/founder-profile.json` — one file per workspace. The profile persists across checks. The founder creates it once (via the setup wizard or manually) and updates it as their situation changes.

## Schema

```json
{
  "company_name": "Acme AI",
  "entity_type": "llc",
  "entity_jurisdiction": "Delaware",
  "stage": "pre-revenue",
  "product_category": "developer tools",
  "team_size": 2,
  "location_country": "US",
  "location_state": "CA",
  "monthly_burn_usd": 5000,
  "current_funding_usd": 0,
  "hourly_rate_usd": 150,
  "goals": ["funding", "visibility", "customers"],
  "notes": "freeform context the founder wants the tool to know"
}
```

### Field reference

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `company_name` | string | yes | Company or project name |
| `entity_type` | enum | yes | `"c-corp"`, `"llc"`, `"sole-prop"`, `"not-incorporated"`, `"other"` |
| `entity_jurisdiction` | string | no | State/country of incorporation (e.g., `"Delaware"`) |
| `stage` | enum | yes | `"idea"`, `"building"`, `"pre-revenue"`, `"revenue"`, `"funded"` |
| `product_category` | string | no | Freeform (e.g., `"fintech"`, `"developer tools"`, `"health"`) |
| `team_size` | integer | yes | Number of people on the team (1 = solo) |
| `location_country` | string | yes | ISO 3166-1 alpha-2 or full name |
| `location_state` | string | no | State/province if relevant |
| `monthly_burn_usd` | number | no | Approximate monthly spend in USD. Used for ROI time-cost calculation |
| `current_funding_usd` | number | no | Total funding raised to date |
| `hourly_rate_usd` | number | no | Founder's opportunity cost per hour. If omitted, ROI Factors will note "hourly rate not specified" |
| `goals` | string[] | yes | What the founder wants from competitions. Values: `"funding"`, `"visibility"`, `"mentorship"`, `"customers"`, `"credibility"`, `"network"`, `"other"` |
| `notes` | string | no | Anything else the tool should know |

## Setup wizard

When a founder runs `/check` and no `founder-profile.json` exists, the skill should:

1. Ask: *"I can add Fit Analysis and ROI sections if you tell me a bit about your company. Want to set up a quick profile? (Takes ~30 seconds.)"*
2. If yes, ask for each required field in natural language (not a form dump). Group related questions:
   - "What's your company called, and how is it structured? (LLC, C-Corp, sole prop, not yet incorporated?)"
   - "What stage are you at? (idea / building / pre-revenue / revenue / funded)"
   - "How many people on your team, and where are you based?"
   - "What are you hoping to get from competitions? (funding, visibility, mentorship, customers, credibility, network)"
3. Optional fields: ask as a single follow-up: *"If you want ROI calculations, I'll also need your approximate monthly burn and hourly rate. Otherwise I'll skip those. Want to add them?"*
4. Save to `./competition-reports/founder-profile.json`.
5. Continue with the `/check` workflow.

If the founder says no, skip silently and omit Fit/ROI sections. Do not ask again for 7 days (track the last-asked date in `./competition-reports/cache/.profile-prompt-ts`).

## Per-check overrides

The founder can override any profile field for a single check without changing the saved profile:

```
/check https://example.com/terms --stage funded --team-size 4
```

Overrides apply to the current report only. The saved profile is not modified. Overrides are noted in the report's Notes section: *"Profile overrides applied for this check: stage=funded, team_size=4."*

## Privacy

The profile stays local. It is never sent to any external service, included in fetch requests, or shared with competition sponsors. It is only used to populate the Fit Analysis and ROI Factors sections of the local report.

## Updating the profile

The founder can update their profile at any time:
- Edit `./competition-reports/founder-profile.json` directly, or
- Run `/check --update-profile` to re-trigger the setup wizard with current values as defaults.
