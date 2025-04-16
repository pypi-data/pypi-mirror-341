from rapidfuzz import fuzz
from ps3838api import ROOT_DIR
from ps3838api.logic import normalize_to_set
from ps3838api.models.event import (
    Failure,
    MatchedLeague,
    NoSuchEvent,
    NoSuchLeague,
    NoSuchLeagueFixtures,
    NoSuchLeagueMatching,
    WrongLeague,
)

import ps3838api.api as ps

import json
from typing import Final

from ps3838api.models.fixtures import FixturesLeagueV3, FixturesResponse
from ps3838api.models.tank import EventInfo


with open(ROOT_DIR / "out/matched_leagues.json") as file:
    MATCHED_LEAGUES: Final[list[MatchedLeague]] = json.load(file)

with open(ROOT_DIR / "out/ps3838_leagues.json") as file:
    ALL_LEAGUES: Final[list[ps.LeagueV3]] = json.load(file)['leagues']


def match_league(
    *,
    league_betsapi: str,
    leagues_mapping: list[MatchedLeague] = MATCHED_LEAGUES,
) -> MatchedLeague | NoSuchLeagueMatching | WrongLeague:
    for league in leagues_mapping:
        if league["betsapi_league"] == league_betsapi:
            if league["ps3838_id"]:
                return league
            else:
                return NoSuchLeagueMatching(league_betsapi)
    return WrongLeague(league_betsapi)


def find_league_by_name(
    league: str, leagues: list[ps.LeagueV3] = ALL_LEAGUES
) -> ps.LeagueV3 | NoSuchLeague:
    normalized = normalize_to_set(league)
    for leagueV3 in leagues:
        if normalize_to_set(leagueV3["name"]) == normalized:
            return leagueV3
    return NoSuchLeagueMatching(league)


def find_event_in_league(
    league_data: FixturesLeagueV3, league: str, home: str, away: str
) -> EventInfo | NoSuchEvent:
    """
    Scans `league_data["events"]` for the best fuzzy match to `home` and `away`.
    Returns the matching event with the highest sum of match scores, as long as
    that sum >= 75 (which is 37.5% of the max possible 200).
    Otherwise, returns NoSuchEvent.
    """
    best_event = None
    best_sum_score = 0
    for event in league_data["events"]:
        # Compare the user-provided home and away vs. the fixture's home and away.
        # Using token_set_ratio (see below for comparison vs token_sort_ratio).
        score_home = fuzz.token_set_ratio(home, event.get("home", ""))
        score_away = fuzz.token_set_ratio(away, event.get("away", ""))
        total_score = score_home + score_away
        if total_score > best_sum_score:
            best_sum_score = total_score
            best_event = event
    # If the best event's combined fuzzy match is < 37.5% of the total possible 200,
    # treat it as no match:
    if best_event is None or best_sum_score < 75:
        return NoSuchEvent(league, home, away)
    return {"eventId": best_event["id"], "leagueId": league_data["id"]}


def magic_find_event(
    fixtures: FixturesResponse, league: str, home: str, away: str
) -> EventInfo | Failure:
    """
    1. Tries to find league by normalizng names;
    2. If don't, search for a league matching
    3. Then `find_event_in_league`
    """

    leagueV3 = find_league_by_name(league)
    if isinstance(leagueV3, NoSuchLeague):
        match match_league(league_betsapi=league):
            case {"ps3838_id": int()} as value:
                league_id: int = value["ps3838_id"]  # type: ignore
            case _:
                return NoSuchLeagueMatching(league)
    else:
        league_id = leagueV3["id"]

    for leagueV3 in fixtures["league"]:
        if leagueV3["id"] == league_id:
            break
    else:
        return NoSuchLeagueFixtures(league)

    return find_event_in_league(leagueV3, league, home, away)
