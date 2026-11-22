
"""Connecteur API-Football pour AZIBAS SPORT ANALYTICS."""

import json
import urllib.parse
import urllib.request
import urllib.error


BASE_URL = "https://v3.football.api-sports.io"


def get_fixtures(api_key, date, timezone="Africa/Abidjan"):
    """Récupère les rencontres d'une date donnée."""

    if not api_key:
        raise ValueError("Clé API-Football absente.")

    params = urllib.parse.urlencode({
        "date": date,
        "timezone": timezone
    })

    url = f"{BASE_URL}/fixtures?{params}"

    request = urllib.request.Request(
        url,
        headers={
            "x-apisports-key": api_key,
            "Accept": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))

        if data.get("errors"):
            raise RuntimeError(str(data["errors"]))

        matches = []

        for item in data.get("response", []):
            fixture = item.get("fixture", {})
            teams = item.get("teams", {})
            league = item.get("league", {})

            matches.append({
                "fixture_id": fixture.get("id"),
                "date": fixture.get("date"),
                "status": fixture.get("status", {}).get("long"),
                "league": league.get("name"),
                "country": league.get("country"),
                "home": teams.get("home", {}).get("name"),
                "away": teams.get("away", {}).get("name"),
                "event": (
                    f"{teams.get('home', {}).get('name')} - "
                    f"{teams.get('away', {}).get('name')}"
                )
            })

        return matches

    except urllib.error.HTTPError as error:
        raise RuntimeError(
            f"Erreur API HTTP {error.code}"
        ) from error

    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Connexion API impossible : {error.reason}"
        ) from error
