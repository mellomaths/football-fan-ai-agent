import json
import os

from typing import Union

from src.infrastructure.custom_logger import create_logger

LOGGER = create_logger(__name__)


class FileSystemDatabase:
    """Class to handle file system database operations for storing and retrieving football match data."""

    matches_filename = "matches.json"
    competitions_filename = "competitions.json"

    def __init__(self, database_dir: str):
        self.log = LOGGER.getChild("__init__")
        self.log.info("Initializing FileSystemDatabase")
        self.__load_database(database_dir)
        self.log.info("FileSystemDatabase initialized")

    def __load_database(self, database_dir: str):
        """Create a database directory if it does not exist."""
        log = self.log.getChild("__create_database")
        self.db_path = database_dir
        if not os.path.exists(self.db_path):
            log.debug(f"Creating database {self.db_path}")
            os.makedirs(self.db_path)
        log.debug(f"Database path {self.db_path} created")

        self.__load_matches()
        self.__load_competitions()


    def __load_entity(self, entity_filename: str) -> Union[list, dict, None]:
        """Load an entity from a JSON file."""
        log = self.log.getChild("__load_entity")
        file_path = os.path.join(self.db_path, entity_filename)
        log.debug(f"Loading entity from {file_path}")
        if not os.path.exists(file_path):
            log.debug(f"Entity file {file_path} does not exist, initializing with empty list")
            return None
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        log.info(f"Entity loaded successfully from {file_path}")
        return data


    def __load_competitions(self):
        """Load competitions from the JSON file."""
        log = self.log.getChild("__load_competitions")
        competitions = self.__load_entity(self.competitions_filename)
        if competitions is None:
            log.debug(
                f"Competitions file {self.competitions_filename} does not exist, initializing with empty list"
            )
            competitions = []
        self.competitions = competitions
        log.info(f"Competitions loaded successfully")

    def __load_matches(self):
        """Load matches from the JSON file."""
        log = self.log.getChild("__load_matches")
        self.matches = {}
        matches = self.__load_entity(self.matches_filename)
        if matches is None:
            log.debug(
                f"Matches file {self.matches_filename} does not exist, initializing with empty dict"
            )
            matches = {}
        self.matches = matches
        log.info(f"Matches loaded successfully")

    def _save_data(self, data: Union[list, dict], file_name: str):
        """Save data to a JSON file."""
        log = self.log.getChild("_save_data")
        file_path = os.path.join(self.db_path, file_name)
        log.debug(f"Saving data to {file_path}")
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        log.debug(f"Data saved to {file_path}")

    def save_matches(self, matches: list, competition_id: str):
        """Save matches to a JSON file."""
        log = self.log.getChild("save_matches")
        log.info(
            f"Saving matches for competition {competition_id} to {self.matches_filename}"
        )
        self.__load_matches()
        self.matches[competition_id] = matches
        self._save_data(self.matches, self.matches_filename)
        log.info("Matches successfully saved")

    def save_competitions(self, competitions: list):
        """Save competitions to a JSON file."""
        log = self.log.getChild("save_competitions")
        self._save_data(competitions, self.competitions_filename)
        log.info("Competitions successfully saved")

    def get_matches_from_team(self, team: str) -> list:
        """Get matches from a specific team."""
        log = self.log.getChild("get_matches_from_team")
        log.info(f"Getting matches for team {team}")
        self.__load_competitions()
        self.__load_matches()
        team_matches = []
        for competition in self.competitions:
            competition_name = competition.get("name", "")
            competition_id = competition.get("id", "")
            if not competition_name or not competition_id:
                log.warning(f"Skipping competition with missing name or id: {competition}")
                continue
            competition_id = str(competition_id)
            log.info(f"Searching for matches involving team {team} in competition ({competition_id}) {competition_name}")
            if competition_id not in list(self.matches.keys()):
                log.info(f"No matches found for competition {competition_id}")
                continue
            for match in self.matches.get(competition_id, []):
                home_team = match.get("homeTeam", {}).get("name", "").lower()
                away_team = match.get("awayTeam", {}).get("name", "").lower()
                team = team.lower()
                utc_date = match.get("utcDate", "")
                if team in home_team or team in away_team:
                    log.info(f"Match found {utc_date} {competition_name} - {home_team} x {away_team}")
                    team_matches.append(match)
        log.info(f"Found {len(team_matches)} matches for team {team}")
        return team_matches
