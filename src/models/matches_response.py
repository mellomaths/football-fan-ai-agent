from pydantic import BaseModel


class Team(BaseModel):
    abbrev: str
    display_name: str
    link: str
    logo: str


class UpcomingMatchesResponse(BaseModel):
    date: str
    date_detail: str
    completed: bool
    competition: str
    home_team: Team
    away_team: Team
    stadium: str
    link: str
