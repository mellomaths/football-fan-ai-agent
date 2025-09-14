from fastapi import APIRouter, status
from starlette.responses import JSONResponse

from infrastructure.logger import create_logger
from models.matches_response import UpcomingMatchesResponse
from scrappers.espn.espn_scrapper import EspnScrapper

LOGGER = create_logger(__name__)

router = APIRouter(prefix="/matches", tags=["matches"], redirect_slashes=False)


@router.get(
    "/{team_name}/upcoming",
    status_code=status.HTTP_200_OK,
    response_model=list[UpcomingMatchesResponse],
)
def get_upcoming_matches(team_name: str):
    log = LOGGER.getChild("get_upcoming_matches")
    log.info(f"Getting upcoming matches for team {team_name}")
    espn_scrapper = EspnScrapper()
    matches = espn_scrapper.get_upcoming_matches(team_name)
    log.info(f"Found {len(matches)} matches")
    return JSONResponse(status_code=status.HTTP_200_OK, content=matches)
