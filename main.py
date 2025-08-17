import os
import typer

from dotenv import load_dotenv
from src.cron.jobs import job_load_database, job_add_team_matches_to_calendar
from src.infrastructure.custom_logger import create_logger

load_dotenv()

LOGGER = create_logger(__name__)
app = typer.Typer()


@app.command()
def load_database():
    """Load data for a specific entity."""
    job_load_database(
        database_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "db")
    )


@app.command()
def add_to_calendar(
    team: str = typer.Argument(..., help="Name of the team to add matches for"),
):
    """Add matches for a specific team to the calendar."""
    job_add_team_matches_to_calendar(
        team=team,
        database_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "db")
    )


@app.command()
def hello(name: str = "World"):
    """Say hello to NAME."""
    typer.echo(f"Hello {name}!")


if __name__ == "__main__":
    app()
