import os
import typer

from dotenv import load_dotenv
from src.cron.jobs import job_load_database, job_add_team_matches_to_calendar
from src.infrastructure.custom_logger import create_logger
from src.infrastructure.google_calendar import create_calendar_manager_from_env

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


@app.command()
def calendar_list():
    """List available Google Calendars."""
    try:
        calendar_manager = create_calendar_manager_from_env()
        calendars = calendar_manager.list_calendars()
        
        if not calendars:
            typer.echo("No calendars found or failed to list calendars.")
            return
        
        typer.echo(f"Found {len(calendars)} calendar(s):")
        for calendar in calendars:
            primary_mark = " (Primary)" if calendar.get('primary') else ""
            typer.echo(f"  • {calendar['summary']} - ID: {calendar['id']}{primary_mark}")
            
    except Exception as e:
        typer.echo(f"Error listing calendars: {e}")
        typer.echo("Make sure you have set up Google Calendar authentication in your .env file.")


@app.command()
def add_team_to_calendar(
    team: str = typer.Argument(..., help="Name of the team to add matches for"),
    calendar_id: str = typer.Option("primary", help="Google Calendar ID to add events to"),
):
    """Add all matches for a specific team to Google Calendar."""
    try:
        result = job_add_team_matches_to_calendar(
            team=team,
            database_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "db"),
            calendar_id=calendar_id
        )
        
        if result["success"]:
            typer.echo(f"✅ Successfully processed matches for {team}")
            typer.echo(f"   Matches found: {result['matches_found']}")
            typer.echo(f"   Events created: {result['events_created']}")
            
            if result.get('errors'):
                typer.echo(f"   Errors: {len(result['errors'])}")
                for error in result['errors']:
                    typer.echo(f"     • {error}")
        else:
            typer.echo(f"❌ Failed to add matches for {team}")
            typer.echo(f"   Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        typer.echo("Make sure you have set up Google Calendar authentication in your .env file.")


@app.command()
def setup_calendar():
    """Setup Google Calendar integration."""
    typer.echo("🔧 Google Calendar Setup Guide")
    typer.echo("")
    typer.echo("Choose ONE authentication method:")
    typer.echo("")
    typer.echo("1. OAuth 2.0 (Interactive - requires browser)")
    typer.echo("   • Go to Google Cloud Console")
    typer.echo("   • Enable Google Calendar API")
    typer.echo("   • Create OAuth 2.0 credentials")
    typer.echo("   • Download as credentials.json")
    typer.echo("   • Set GOOGLE_CALENDAR_CREDENTIALS_PATH=credentials.json")
    typer.echo("")
    typer.echo("2. Service Account (Automated - no browser)")
    typer.echo("   • Go to Google Cloud Console")
    typer.echo("   • Create service account")
    typer.echo("   • Download JSON key")
    typer.echo("   • Set GOOGLE_CALENDAR_SERVICE_ACCOUNT_PATH=key.json")
    typer.echo("")
    typer.echo("3. Application Default Credentials (ADC)")
    typer.echo("   • Install gcloud CLI")
    typer.echo("   • Run: gcloud auth application-default login")
    typer.echo("   • Set GOOGLE_CALENDAR_USE_ADC=true")
    typer.echo("")
    typer.echo("4. API Key (Read-only access)")
    typer.echo("   • Get API key from Google Cloud Console")
    typer.echo("   • Set GOOGLE_CALENDAR_API_KEY=your_key")
    typer.echo("   • Note: Cannot create/modify events")
    typer.echo("")
    typer.echo("Environment variables to set in .env:")
    typer.echo("   GOOGLE_CALENDAR_CREDENTIALS_PATH=credentials.json")
    typer.echo("   GOOGLE_CALENDAR_SERVICE_ACCOUNT_PATH=service-account.json")
    typer.echo("   GOOGLE_CALENDAR_USE_ADC=true")
    typer.echo("   GOOGLE_CALENDAR_API_KEY=your_api_key")
    typer.echo("")
    typer.echo("Commands to test:")
    typer.echo("  • calendar-list - List available calendars")
    typer.echo("  • add-team-to-calendar 'Team Name' - Add team matches to calendar")


if __name__ == "__main__":
    app()
