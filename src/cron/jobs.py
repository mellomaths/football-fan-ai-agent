import os

from datetime import datetime

from src.agents.football_data_agent import FootballDataAgent
from src.config import COMPETITIONS_TO_LOAD
from src.infrastructure.custom_logger import create_logger
from src.infrastructure.file_system_database import FileSystemDatabase

LOGGER = create_logger(__name__)
DATABASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "db")


def job_load_database(database_dir: str = None, month: int = None, year: int = None):
    """
    Job to load matches from a specific month and year.
    After getting the matches from the FootballDataAgent, it saves them to the database.
    """
    if database_dir is None:
        database_dir = DATABASE_DIR
    now = datetime.now()
    if month is None:
        month = now.month
    if year is None:
        year = now.year
    log = LOGGER.getChild("job_load_database")
    log.info(f"Loading matches {database_dir} from {month}/{year}")
    log.debug(f"Current month: {month}, Year: {year}")
    football_agent = FootballDataAgent(
        api_key=os.getenv("FOOTBALL_DATA_API_KEY"),
        base_url=os.getenv("FOOTBALL_DATA_API_BASE_URL"),
    )
    db = FileSystemDatabase(database_dir=database_dir)
    competitions = football_agent.get_competitions()
    db.save_competitions(competitions)
    for competition_name in COMPETITIONS_TO_LOAD:
        log.info(f"Loading competition {competition_name}")
        comp = next(
            (comp for comp in competitions if competition_name in comp.get("name", "")),
            None,
        )
        if not comp:
            log.error(f"Competition {competition_name} not found in competitions")
            continue
        log.debug(f"Found competition: {comp}")
        matches = football_agent.get_matches_from_month(
            competition_name=comp["name"], month=month, year=year
        )
        log.debug(f"Found {len(matches)} matches for {comp['name']} in {month}/{year}")
        db.save_matches(matches, comp["id"])
        log.info(
            f"Saved {len(matches)} matches for {comp['name']} in {month}/{year} to the database"
        )
    log.info("All matches loaded and saved to the database")
    log.info("Job completed successfully")


def job_add_team_matches_to_calendar(team: str, database_dir: str = None):
    """
    Job to get matches from a specific team.
    This function is a placeholder for future implementation.
    """
    if database_dir is None:
        database_dir = DATABASE_DIR
    log = LOGGER.getChild("job_get_matches_from_team")
    log.info(f"Getting matches for team: {team}")
    db = FileSystemDatabase(
        database_dir=database_dir
    )
    matches = db.get_matches_from_team(team)
    if not matches:
        log.warning(f"No matches found for team {team}")
        return []
    log.info(f"Found {len(matches)} matches for team {team}")
    return None
