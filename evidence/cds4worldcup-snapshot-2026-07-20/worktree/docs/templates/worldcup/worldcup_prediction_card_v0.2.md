# World Cup MVP-A Prediction Card Request

## Match Package

- match_id: {match_id}
- competition: {competition}
- stage: {stage}
- kickoff_time_utc: {kickoff_time_utc}
- home_team: {home_team}
- away_team: {away_team}
- venue: {venue}
- city: {city}
- source_cutoff_utc: {source_cutoff_utc}

## Green Sources Available To Model

{green_sources}

## Red Sources Excluded From Model

{red_sources}

## Simple Statistical Baseline

{simple_baseline}

## Methodology Constraints

{methodology_constraints}

## Required JSON Output

Return a JSON object with exactly these top-level keys:

```json
{{
  "prediction_card": {{
    "probabilities": {{
      "home_win_90m": 0.0,
      "draw_90m": 0.0,
      "away_win_90m": 0.0
    }},
    "baselines": {{
      "simple_statistical": {{}},
      "market_or_odds": {{"status": "missing_with_reason", "reason": "string"}},
      "public_ai": {{"status": "not_applicable", "reason": "string"}}
    }},
    "uncertainty_notes": ["string"]
  }},
  "factors": [
    {{
      "factor_id": "wc2026-a-m01-mex-rsa-f01-short-name",
      "origin": "cds_generated",
      "event_relation": "precursor|inhibitor|branch|counterevidence",
      "direction": "string",
      "observable_proxy": "string",
      "quantified_threshold": "string",
      "settlement_rule": "string",
      "counter_signal": "string",
      "data_sources": ["official_schedule_snapshot"],
      "adjudicator": {{
        "required_independence": "not the same agent/person who generated the factor",
        "status": "pending",
        "confidence_0_10": null
      }},
      "calibration_status": "tracking"
    }}
  ]
}}
```

Generate exactly 3 tracked factors.
