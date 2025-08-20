"""
Google Calendar integration for Football Fan AI Agent.

This module provides functionality to create football match events in Google Calendar.
It uses OAuth 2.0 authentication for full calendar access.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .custom_logger import create_logger

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

LOGGER = create_logger(__name__)


class GoogleCalendarManager:
    """Manages Google Calendar operations for football matches using OAuth 2.0."""
    
    def __init__(self, credentials_path: str, token_path: str = "token.json"):
        """
        Initialize the Google Calendar manager with OAuth authentication.
        
        Args:
            credentials_path: Path to OAuth credentials file (credentials.json)
            token_path: Path to store/retrieve OAuth token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self.log = LOGGER.getChild("GoogleCalendarManager")
        
        if not credentials_path:
            raise ValueError("credentials_path is required for OAuth authentication")
    
    def authenticate(self) -> bool:
        """
        Authenticate with Google Calendar API using OAuth 2.0.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        if not os.path.exists(self.credentials_path):
            self.log.error(f"Credentials file not found: {self.credentials_path}")
            return False
        
        creds = None
        
        # Check if token file exists
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
                self.log.info("Loaded existing OAuth credentials from token file")
            except Exception as e:
                self.log.warning(f"Failed to load existing OAuth credentials: {e}")
                creds = None
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    self.log.info("Refreshed expired OAuth credentials")
                except Exception as e:
                    self.log.error(f"Failed to refresh OAuth credentials: {e}")
                    creds = None
            
            if not creds:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                    self.log.info("Generated new OAuth credentials through OAuth flow")
                except Exception as e:
                    self.log.error(f"Failed to generate OAuth credentials: {e}")
                    return False
                
                # Save credentials for next run
                try:
                    with open(self.token_path, 'w') as token:
                        token.write(creds.to_json())
                    self.log.info(f"Saved OAuth credentials to {self.token_path}")
                except Exception as e:
                    self.log.error(f"Failed to save OAuth credentials: {e}")
        
        # Build the service
        try:
            self.service = build('calendar', 'v3', credentials=creds)
            self.log.info("OAuth authentication successful")
            return True
        except Exception as e:
            self.log.error(f"Failed to build calendar service with OAuth: {e}")
            return False
    
    def create_match_event(self, match_data: Dict[str, Any], calendar_id: str = "primary") -> Optional[str]:
        """
        Create a calendar event for a football match.
        
        Args:
            match_data: Dictionary containing match information
            calendar_id: Google Calendar ID (default: primary)
            
        Returns:
            Optional[str]: Event ID if successful, None otherwise
        """
        if not self.service:
            self.log.error("Calendar service not initialized. Call authenticate() first.")
            return None
        
        try:
            # Parse match data
            home_team = match_data.get('homeTeam', {}).get('name', 'Unknown Team')
            away_team = match_data.get('awayTeam', {}).get('name', 'Unknown Team')
            competition = match_data.get('competition', {}).get('name', 'Football Match')
            
            # Parse date and time
            match_date = match_data.get('utcDate')
            if not match_date:
                self.log.error("Match date not found in match data")
                return None
            
            # Convert UTC date to datetime
            try:
                match_datetime = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
            except ValueError:
                self.log.error(f"Invalid date format: {match_date}")
                return None
            
            # Create event details with new title format
            event = {
                'summary': f'⚽️ {competition}: {home_team} x {away_team}',
                'description': f'Powered by Football Fan AI Agent',
                'start': {
                    'dateTime': match_datetime.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': (match_datetime + timedelta(hours=2)).isoformat(),
                    'timeZone': 'UTC',
                },
                'location': match_data.get('venue', 'TBD'),
                'colorId': '1',  # Blue color for sports events
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 30},
                        {'method': 'popup', 'minutes': 60},
                    ],
                },
                'extendedProperties': {
                    'private': {
                        'matchId': str(match_data.get('id', '')),
                        'competition': competition,
                        'homeTeam': home_team,
                        'awayTeam': away_team,
                    }
                }
            }
            
            # Create the event
            event_result = self.service.events().insert(
                calendarId=calendar_id,
                body=event
            ).execute()
            
            event_id = event_result.get('id')
            self.log.info(f"Successfully created calendar event: {event_id}")
            self.log.info(f"Event: {competition}: {home_team} x {away_team} on {match_datetime.strftime('%Y-%m-%d %H:%M')}")
            
            return event_id
            
        except HttpError as e:
            self.log.error(f"HTTP error creating calendar event: {e}")
            return None
        except Exception as e:
            self.log.error(f"Unexpected error creating calendar event: {e}")
            return None
    
    def create_team_matches_events(self, matches: List[Dict[str, Any]], team_name: str, 
                                  calendar_id: str = "primary") -> Dict[str, Any]:
        """
        Create calendar events for all matches of a specific team.
        
        Args:
            matches: List of match dictionaries
            team_name: Name of the team
            calendar_id: Google Calendar ID (default: primary)
            
        Returns:
            Dict[str, Any]: Summary of events created
        """
        if not self.service:
            self.log.error("Calendar service not initialized. Call authenticate() first.")
            return {"success": False, "error": "Service not initialized"}
        
        if not matches:
            self.log.warning(f"No matches found for team: {team_name}")
            return {"success": True, "matches_found": 0, "events_created": 0}
        
        self.log.info(f"Creating calendar events for {len(matches)} matches of {team_name}")
        
        events_created = 0
        errors = []
        
        for match in matches:
            try:
                event_id = self.create_match_event(match, calendar_id)
                if event_id:
                    events_created += 1
                else:
                    errors.append(f"Failed to create event for match {match.get('id', 'unknown')}")
            except Exception as e:
                error_msg = f"Error creating event for match {match.get('id', 'unknown')}: {e}"
                self.log.error(error_msg)
                errors.append(error_msg)
        
        result = {
            "success": True,
            "team": team_name,
            "matches_found": len(matches),
            "events_created": events_created,
            "errors": errors
        }
        
        self.log.info(f"Calendar events creation completed: {events_created}/{len(matches)} events created")
        return result
    
    def list_calendars(self) -> List[Dict[str, str]]:
        """
        List available calendars.
        
        Returns:
            List[Dict[str, str]]: List of calendar information
        """
        if not self.service:
            self.log.error("Calendar service not initialized. Call authenticate() first.")
            return []
        
        try:
            calendar_list = self.service.calendarList().list().execute()
            calendars = []
            
            for calendar in calendar_list.get('items', []):
                calendars.append({
                    'id': calendar['id'],
                    'summary': calendar.get('summary', 'No Name'),
                    'primary': calendar.get('primary', False),
                    'accessRole': calendar.get('accessRole', 'unknown')
                })
            
            self.log.info(f"Found {len(calendars)} calendars")
            return calendars
            
        except HttpError as e:
            self.log.error(f"HTTP error listing calendars: {e}")
            return []
        except Exception as e:
            self.log.error(f"Unexpected error listing calendars: {e}")
            return []
    
    def delete_event(self, event_id: str, calendar_id: str = "primary") -> bool:
        """
        Delete a calendar event.
        
        Args:
            event_id: ID of the event to delete
            calendar_id: Google Calendar ID (default: primary)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.service:
            self.log.error("Calendar service not initialized. Call authenticate() first.")
            return False
        
        try:
            self.service.events().delete(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            
            self.log.info(f"Successfully deleted event: {event_id}")
            return True
            
        except HttpError as e:
            self.log.error(f"HTTP error deleting event: {e}")
            return False
        except Exception as e:
            self.log.error(f"Unexpected error deleting event: {e}")
            return False


def create_calendar_manager(credentials_path: str, token_path: str = "token.json") -> GoogleCalendarManager:
    """
    Factory function to create and authenticate a Google Calendar manager.
    
    Args:
        credentials_path: Path to OAuth credentials file (required)
        token_path: Path to store/retrieve OAuth token
        
    Returns:
        GoogleCalendarManager: Authenticated calendar manager instance
    """
    manager = GoogleCalendarManager(
        credentials_path=credentials_path,
        token_path=token_path
    )
    
    if manager.authenticate():
        return manager
    else:
        raise RuntimeError("Failed to authenticate with Google Calendar API")


def create_calendar_manager_from_env() -> GoogleCalendarManager:
    """
    Create calendar manager using environment variables for OAuth authentication.
    
    Environment variables:
    - GOOGLE_CALENDAR_CREDENTIALS_PATH: Path to OAuth credentials file (required)
    - GOOGLE_CALENDAR_TOKEN_PATH: Path to OAuth token file (optional, defaults to token.json)
    
    Returns:
        GoogleCalendarManager: Authenticated calendar manager instance
    """
    credentials_path = os.getenv('GOOGLE_CALENDAR_CREDENTIALS_PATH')
    if not credentials_path:
        raise ValueError("GOOGLE_CALENDAR_CREDENTIALS_PATH environment variable is required")
    
    token_path = os.getenv('GOOGLE_CALENDAR_TOKEN_PATH', 'token.json')
    
    return create_calendar_manager(
        credentials_path=credentials_path,
        token_path=token_path
    )
