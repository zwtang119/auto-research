# Source Ledger

> Status: Phase 0
> Last updated: 2026-06-10

## Green Sources

| source_id | source_type | url_or_path | captured_at_utc | allowed_use |
|---|---|---|---|---|
| official_schedule_snapshot | FIFA official schedule snapshot (via ESPN) | https://www.espn.com/soccer/schedule/_/league/FIFA.WORLD/date/20260611 | 2026-06-10T12:00:00Z | match_package |
| wikipedia_2022_wc_group_c | Wikipedia match report | https://en.wikipedia.org/wiki/2022_FIFA_World_Cup#Group_C | 2026-06-10 | match_package / factor_adjudication |
| wikipedia_2022_wc_seeding | Wikipedia ranking data | https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_seeding | 2026-06-10 | match_package |
| wikipedia_mexico_national_football_team_fifa_ranking | Wikipedia team ranking | https://en.wikipedia.org/wiki/Mexico_national_football_team | 2026-06-10 | match_package |
| wikipedia_south_africa_national_football_team_fifa_ranking | Wikipedia team ranking | https://en.wikipedia.org/wiki/South_Africa_national_football_team | 2026-06-10 | match_package |
| fifa_match_report_wc2022_group_c | FIFA official match report | pending | pending | factor_adjudication |
| fifa_match_report_wc2026_group_a | FIFA official match report | pending | pending | factor_adjudication |

## Red Sources

| source_id | source_type | url_or_path | captured_at_utc | allowed_use |
|---|---|---|---|---|
| kimi_public_artifact_snapshot | Public AI artifact | worldcup-kimi/ | 2026-06-10T12:00:00Z | baseline/candidate_seed/parser_fixture |

## Parser Blacklist

| pattern | reason | allowed_use |
|---|---|---|
| LLM-generated fact summaries | no primary source guarantee | candidate_seed |
| Kimi probability/ranking/win-rate fields | probability anchoring risk | public_ai_baseline |
| Excel/PDF fields without row-level URL | lineage missing | parser_fixture |
| social media summaries | weak provenance | manual_review |
| sources with known parser errors | format instability | pending_manual_review |
