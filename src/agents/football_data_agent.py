import requests

from functools import lru_cache
from typing import List, Dict


class FootballDataAgent:
    """Class to handle football data API interactions"""

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"X-Auth-Token": self.api_key} if self.api_key else {}
        self.competitions = []

    @lru_cache
    def get_competitions(self) -> List[Dict]:
        if self.competitions:
            return self.competitions
        response = requests.get(f"{self.base_url}/competitions", headers=self.headers)
        if response.status_code != 200:
            raise ValueError(
                f"Failed to fetch competitions: {response.status_code} - {response.text}"
            )
        self.competitions = response.json().get("competitions", [])
        return self.competitions

    @lru_cache
    def get_matches_from_month(
        self, competition_name: str, month: int, year: int
    ) -> List[Dict]:
        """Get matches from a specific competition and month"""
        assert 1 <= month <= 12, "Month must be between 1 and 12"
        month = f"{month:02d}"  # Format month to two digits
        if not self.competitions:
            self.get_competitions()
        competition = next(
            (comp for comp in self.competitions if comp["name"] == competition_name),
            None,
        )
        if not competition:
            raise ValueError(f"Competition '{competition_name}' not found.")

        response = requests.get(
            f"{self.base_url}/competitions/{competition['id']}/matches",
            headers=self.headers,
            params={
                "season": f"{year}",
                "dateFrom": f"{year}-{month}-01",
                "dateTo": f"{year}-{month}-31",
            },
        )
        if response.status_code != 200:
            raise ValueError(
                f"Failed to fetch matches: {response.status_code} - {response.text}"
            )
        return response.json().get("matches", [])
