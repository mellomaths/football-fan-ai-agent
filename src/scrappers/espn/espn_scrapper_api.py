from datetime import datetime

import requests

from infrastructure.logger import create_logger
from scrappers.espn.espn_config import EspnConfig

LOGGER = create_logger(__name__)


class EspnScrapperApi:

    def __init__(self):
        self.log = LOGGER.getChild("__init__")
        self.log.info("Initializing EspnScrapperApi")
        self.config = EspnConfig()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
        )

    def get_data(self, team: str):
        log = self.log.getChild("get_matches")
        url = self.config.get_api_url(team)
        log.info(f"Getting matches for team {team}, {url}")
        response = self.session.get(url)
        log.info(f"Response status: {response.status_code}")
        if response.status_code != 200:
            log.error(f"Failed to get matches for team {team}, {response.status_code}")
            return []
        return response.json()

    def parse_matches(self, data: dict) -> list:
        """Parse match data from ESPN API response."""
        matches = []
        try:
            events = data.get("events", [])
            print(f"Found {len(events)} events in API response")

            for event in events:
                try:
                    # Extract match information
                    date_str = event.get("date", "")
                    if not date_str:
                        continue

                    # Parse the date
                    match_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    # Get competition info
                    competition = event.get("competitions", [{}])[0]
                    competition_name = competition.get("name", "Unknown")
                    # Get teams
                    competitors = competition.get("competitors", [])
                    if len(competitors) < 2:
                        continue

                    home_team = (
                        competitors[0].get("team", {}).get("displayName", "Unknown")
                    )
                    away_team = (
                        competitors[1].get("team", {}).get("displayName", "Unknown")
                    )
                    # Get venue
                    venue = competition.get("venue", {})
                    venue_name = venue.get("fullName", "TBD")
                    # Get status
                    status = (
                        event.get("status", {}).get("type", {}).get("name", "Scheduled")
                    )
                    match_info = {
                        "date": match_date,
                        "home_team": home_team,
                        "away_team": away_team,
                        "competition": competition_name,
                        "venue": venue_name,
                        "status": status,
                        "raw_date": date_str,
                    }
                    matches.append(match_info)
                except Exception as e:
                    print(f"Error parsing event: {e}")
                    continue
        except Exception as e:
            print(f"Error parsing API data: {e}")

        return matches
