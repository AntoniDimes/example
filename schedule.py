import requests
from datetime import datetime, timezone
from team_id import get_team_id

def get_team_schedule(team_name):
    base_url = "https://api.football-data.org/v4"
    api_key = "0fc9371f535a41428c2c98e9e546ac2d"

    try:
        # Get the team id from the team name
        team_id = get_team_id(team_name)
        if not team_id:
            print("Team not found.")
            return None

        # Get the matches for the team by using the id
        matches_url = f"{base_url}/teams/{team_id}/matches"
        headers = {
            "X-Auth-Token": api_key
        }
        matches_response = requests.get(matches_url, headers=headers)
        matches_response.raise_for_status()
        matches_data = matches_response.json()

        if not matches_data.get("matches"):
            print("No upcoming matches found.")
            return None

        schedule = []
        current_time = datetime.now(timezone.utc)
        for match in matches_data["matches"]:
            match_date = datetime.fromisoformat(match["utcDate"].replace("Z", "+00:00"))
            match_time = match_date.strftime("%H:%M:%S")
            if match_date > current_time:
                status = "Match not started"
                score = ""
            else:
                status = "Match finished"
                score = f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}"

            schedule.append({
                "date": match_date.strftime("%Y-%m-%d"),
                "time": match_time,
                "home_team": match["homeTeam"]["name"],
                "away_team": match["awayTeam"]["name"],
                "competition": match["competition"]["name"],
                "status": status,
                "score": score
            })

        return schedule

    except requests.RequestException as e:
        print(f"Request error: {e}")
    except KeyError as e:
        print(f"Data parsing error: Missing key {e}")
    except ValueError as e:
        print(f"Data parsing error: {e}")

    return None
