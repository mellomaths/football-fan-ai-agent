import os

from datetime import datetime

from src.agents.football_data_agent import FootballDataAgent
from src.config import COMPETITIONS_TO_LOAD
from src.infrastructure.custom_logger import create_logger
from src.infrastructure.file_system_database import FileSystemDatabase
from src.infrastructure.google_calendar import create_calendar_manager_from_env

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


def job_add_team_matches_to_calendar(team: str, database_dir: str = None, 
                                    calendar_id: str = "primary"):
    """
    Job to add matches from a specific team to Google Calendar.
    
    Args:
        team: Name of the team to add matches for
        database_dir: Directory containing the database files
        calendar_id: Google Calendar ID to add events to (default: primary)
        
    Returns:
        Dict: Summary of calendar events created
    """
    if database_dir is None:
        database_dir = DATABASE_DIR
    
    log = LOGGER.getChild("job_add_team_matches_to_calendar")
    log.info(f"Adding matches for team: {team} to Google Calendar")
    
    try:
        # Get matches from database
        db = FileSystemDatabase(database_dir=database_dir)
        matches = db.get_matches_from_team(team)
        
        if not matches:
            log.warning(f"No matches found for team {team}")
            return {
                "success": True,
                "team": team,
                "matches_found": 0,
                "events_created": 0,
                "message": "No matches found for this team"
            }
        
        log.info(f"Found {len(matches)} matches for team {team}")
        
        # Initialize Google Calendar manager using environment variables
        try:
            calendar_manager = create_calendar_manager_from_env()
            log.info("Successfully authenticated with Google Calendar")
        except Exception as e:
            log.error(f"Failed to authenticate with Google Calendar: {e}")
            return {
                "success": False,
                "team": team,
                "matches_found": len(matches),
                "events_created": 0,
                "error": f"Authentication failed: {str(e)}"
            }
        
        # Create calendar events for all matches
        result = calendar_manager.create_team_matches_events(matches, team, calendar_id)
        
        if result["success"]:
            log.info(f"Successfully created {result['events_created']} calendar events for {team}")
        else:
            log.error(f"Failed to create calendar events: {result.get('error', 'Unknown error')}")
        
        return result
        
    except Exception as e:
        log.error(f"Unexpected error in job_add_team_matches_to_calendar: {e}")
        return {
            "success": False,
            "team": team,
            "matches_found": 0,
            "events_created": 0,
            "error": f"Unexpected error: {str(e)}"
        }
