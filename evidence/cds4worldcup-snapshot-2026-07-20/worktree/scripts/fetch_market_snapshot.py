#!/usr/bin/env python3
"""Fetch a public Polymarket World Cup winner snapshot for static site display."""

import csv
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEAM_NAME_MAP = ROOT / "data" / "processed" / "team_name_map.csv"
TEAM_REGISTRY = ROOT / "data" / "processed" / "team_registry.csv"
DEFAULT_OUT = ROOT / "data" / "processed" / "market_public_snapshot.json"
DEFAULT_SEARCH_QUERY = "FIFA World Cup 2026 winner"
DEFAULT_EVENT_SLUG = "world-cup-winner"


ALIASES = {
    "USA": "united-states",
    "United States": "united-states",
    "Turkiye": "turkey",
    "Türkiye": "turkey",
    "Turkey": "turkey",
    "Ivory Coast": "côte-divoire",
    "Côte d'Ivoire": "côte-divoire",
    "South Korea": "south-korea",
    "Korea Republic": "south-korea",
}


def extract_team_name(question):
    match = re.match(r"^Will\s+(.+?)\s+win\s+the\s+2026\s+FIFA\s+World\s+Cup\??$", str(question or "").strip())
    if not match:
        return None
    name = match.group(1).strip()
    if name.lower() in {"any other team", "team am", "team ai"}:
        return None
    return name


def slugify(value):
    text = str(value or "").strip().lower()
    text = text.replace("'", "").replace(".", "")
    text = re.sub(r"\s+", "-", text)
    return re.sub(r"[^a-z0-9\-à-ž]", "", text)


def load_team_name_map():
    mapping = {}
    if TEAM_NAME_MAP.exists():
        with TEAM_NAME_MAP.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                slug = slugify(row.get("canonical_team") or row.get("en_name"))
                for key in [row.get("canonical_team"), row.get("en_name"), row.get("zh_name")]:
                    if key:
                        mapping[key] = slug
                for alias in str(row.get("aliases", "")).split("|"):
                    if alias.strip():
                        mapping[alias.strip()] = slug
    if TEAM_REGISTRY.exists():
        with TEAM_REGISTRY.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                slug = slugify(row.get("canonical_team"))
                for key in [row.get("canonical_team"), row.get("en_name"), row.get("zh_name")]:
                    if key:
                        mapping[key] = slug
    mapping.update(ALIASES)
    return mapping


def parse_jsonish(value):
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except (TypeError, json.JSONDecodeError):
        return []


def yes_price_from_market(market):
    outcomes = parse_jsonish(market.get("outcomes"))
    prices = parse_jsonish(market.get("outcomePrices"))
    for index, outcome in enumerate(outcomes):
        if str(outcome).lower() == "yes" and index < len(prices):
            try:
                return float(prices[index])
            except (TypeError, ValueError):
                return None
    return None


def iter_events(search_payload):
    if isinstance(search_payload, dict):
        for key in ("events", "results", "data"):
            value = search_payload.get(key)
            if isinstance(value, list):
                yield from value
        if search_payload.get("slug"):
            yield search_payload
    elif isinstance(search_payload, list):
        yield from search_payload


def build_snapshot_from_search(search_payload, name_map, event_slug=DEFAULT_EVENT_SLUG):
    target = None
    for event in iter_events(search_payload):
        if isinstance(event, dict) and event.get("slug") == event_slug:
            target = event
            break
    if not target:
        raise ValueError(f"Polymarket event not found: {event_slug}")

    teams = {}
    unmapped = []
    for market in target.get("markets", []) or []:
        if not isinstance(market, dict):
            continue
        team_name = extract_team_name(market.get("question"))
        price = yes_price_from_market(market)
        if team_name is None or price is None:
            unmapped.append({
                "question": market.get("question", ""),
                "market_slug": market.get("slug", ""),
                "reason": "unmapped_or_missing_yes_price",
            })
            continue
        slug = name_map.get(team_name) or name_map.get(team_name.replace("''", "'"))
        if not slug:
            unmapped.append({
                "question": market.get("question", ""),
                "market_slug": market.get("slug", ""),
                "reason": "team_name_not_in_registry",
            })
            continue
        teams[slug] = {
            "probability": round(price * 100, 2),
            "market_slug": market.get("slug", ""),
            "question": market.get("question", ""),
            "raw_yes_price": price,
        }

    return {
        "status": "available" if teams else "snapshot_unavailable",
        "source": "polymarket_gamma_public_search",
        "event_slug": target.get("slug", event_slug),
        "event_title": target.get("title", "World Cup Winner"),
        "last_fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "display_rule": "只代表外界怎么看，不作为事实依据，也不是投注建议。",
        "teams": dict(sorted(teams.items())),
        "unmapped_markets": unmapped,
    }


def fetch_public_search(query):
    encoded = urllib.parse.urlencode({"q": query, "limit": 20})
    url = f"https://gamma-api.polymarket.com/public-search?{encoded}"
    request = urllib.request.Request(url, headers={"User-Agent": "cds4worldcup-static-site/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    query = os.environ.get("POLYMARKET_SEARCH_QUERY", DEFAULT_SEARCH_QUERY)
    event_slug = os.environ.get("POLYMARKET_EVENT_SLUG", DEFAULT_EVENT_SLUG)
    out_path = Path(os.environ.get("MARKET_SNAPSHOT_OUT", DEFAULT_OUT))
    payload = fetch_public_search(query)
    snapshot = build_snapshot_from_search(payload, load_team_name_map(), event_slug=event_slug)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_path} with {len(snapshot['teams'])} mapped teams")
    return 0 if snapshot["teams"] else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"market snapshot fetch failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
