import json
import re

import requests
from bs4 import BeautifulSoup

from infrastructure.logger import create_logger
from scrappers.espn.espn_config import EspnConfig

LOGGER = create_logger(__name__)


class EspnScrapperHTML:

    def __init__(self):
        self.log = create_logger(__name__)
        self.log.info("Initializing EspnScrapperHTML")
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
        self.base_url = "https://www.espn.com"

    def get_data(self, team: str):
        """
        Fallback method to scrape matches from HTML.
        This might not work well due to JavaScript rendering.
        """
        log = self.log.getChild("get_matches")
        url = self.config.get_website_url(team)
        if not url:
            log.error(f"No URL found for team {team}")
            return {}
        log.info(f"Getting matches for team {team}, {url}")
        try:
            response = self.session.get(url)
            log.info(f"HTML Response status: {response.status_code}")
            if response.status_code != 200:
                return {}
            # Save the response for debugging
            with open("espn_response_html.html", "w", encoding="utf-8") as f:
                f.write(response.text)

            soup = BeautifulSoup(response.text, "html.parser")
            # Look for any JSON data in script tags
            scripts = soup.find_all("script")
            result = {}
            for script in list(scripts):
                # Matches JSON data
                if script.string is None:
                    continue
                if "window['__CONFIG__']" in script.string:
                    log.info("Found matches JSON data in script")
                    try:
                        dtypes = re.findall(r"window\['.*?'\]", script.string)
                        data = re.findall(r"{.*?};", script.string)
                        for i, d in enumerate(data):
                            dt = dtypes[i].replace("window['", "").replace("']", "")
                            d = d.replace("};", "}")
                            result[dt] = json.loads(d)
                    except Exception as e:
                        log.error(f"Error in JSON loading: {e}")
                        continue
        except Exception as e:
            log.error(f"Error in HTML scraping: {e}")
        return result

    def parse_matches(self, data: dict) -> list:
        """Parse matches from HTML data."""
        log = self.log.getChild("parse_matches")
        espn_fitt = data.get("__espnfitt__", {})
        page = espn_fitt.get("page", {})
        content = page.get("content", {})
        fixtures = content.get("fixtures", {})
        events = fixtures.get("events", [])
        matches = []
        for event in events:
            home_team = {}
            away_team = {}
            for competitor in event.get("competitors", []):
                link = competitor.get("links", None)
                team = {
                    "abbrev": competitor.get("abbrev", ""),
                    "display_name": competitor.get("displayName", ""),
                    "link": f"{self.base_url}{link}" if link else None,
                    "logo": competitor.get("logo", None),
                }
                if competitor.get("isHome", False):
                    home_team = team
                else:
                    away_team = team

            link = event.get("link", None)
            match = {
                "date": event.get("date", ""),
                "date_detail": event.get("status", {}).get("detail", None),
                "completed": event.get("completed", False),
                "competition": event.get("league", ""),
                "home_team": home_team,
                "away_team": away_team,
                "stadium": event.get("venue", {}).get("fullName", ""),
                "link": f"{self.base_url}{link}" if link else None,
            }
            matches.append(match)
        log.info(f"Found {len(matches)} matches")
        return matches
