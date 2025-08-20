"""
Google Calendar integration for Football Fan AI Agent.

This module provides functionality to create football match events in Google Calendar.
It handles multiple authentication methods: OAuth 2.0, Service Account, and Application Default Credentials.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google.auth import default
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .custom_logger import create_logger

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

LOGGER = create_logger(__name__)


class GoogleCalendarManager:
    """Manages Google Calendar operations for football matches."""
    
    def __init__(self, 
                 credentials_path: Optional[str] = None, 
                 token_path: str = "token.json",
                 service_account_path: Optional[str] = None,
                 use_adc: bool = False,
                 api_key: Optional[str] = None):
        """
        Initialize the Google Calendar manager with flexible authentication.
        
        Args:
            credentials_path: Path to OAuth credentials file (credentials.json)
            token_path: Path to store/retrieve OAuth token
            service_account_path: Path to service account JSON key file
            use_adc: Use Application Default Credentials (gcloud, GCP metadata)
            api_key: Google API key for read-only operations
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service_account_path = service_account_path
        self.use_adc = use_adc
        self.api_key = api_key
        self.service = None
        self.log = LOGGER.getChild("GoogleCalendarManager")
        
        # Validate authentication method
        auth_methods = sum([
            bool(credentials_path),
            bool(service_account_path),
            use_adc,
            bool(api_key)
        ])
        
        if auth_methods == 0:
            self.log.warning("No authentication method specified. Will try ADC first.")
            self.use_adc = True
        elif auth_methods > 1:
            self.log.warning("Multiple authentication methods specified. Priority: ADC > Service Account > OAuth > API Key")
    
    def authenticate(self) -> bool:
        """
        Authenticate with Google Calendar API using the best available method.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        # Try authentication methods in order of preference
        auth_methods = [
            ("Application Default Credentials", self._authenticate_adc),
            ("Service Account", self._authenticate_service_account),
            ("OAuth 2.0", self._authenticate_oauth),
            ("API Key", self._authenticate_api_key)
        ]
        
        for method_name, auth_func in auth_methods:
            if self._should_try_method(method_name):
                self.log.info(f"Trying {method_name} authentication...")
                try:
                    if auth_func():
                        self.log.info(f"Successfully authenticated using {method_name}")
                        return True
                except Exception as e:
                    self.log.warning(f"{method_name} authentication failed: {e}")
                    continue
        
        self.log.error("All authentication methods failed")
        return False
    
    def _should_try_method(self, method_name: str) -> bool:
        """Determine if a specific authentication method should be attempted."""
        if method_name == "Application Default Credentials":
            return self.use_adc
        elif method_name == "Service Account":
            return bool(self.service_account_path)
        elif method_name == "OAuth 2.0":
            return bool(self.credentials_path)
        elif method_name == "API Key":
            return bool(self.api_key)
        return False
    
    def _authenticate_adc(self) -> bool:
        """Authenticate using Application Default Credentials."""
        try:
            creds, project = default(scopes=SCOPES)
            if creds and creds.valid:
                self.service = build('calendar', 'v3', credentials=creds)
                self.log.info(f"Using ADC from project: {project}")
                return True
            else:
                self.log.warning("ADC credentials not valid")
                return False
        except Exception as e:
            self.log.warning(f"ADC authentication failed: {e}")
            return False
    
    def _authenticate_service_account(self) -> bool:
        """Authenticate using service account credentials."""
        if not self.service_account_path or not os.path.exists(self.service_account_path):
            return False
        
        try:
            creds = service_account.Credentials.from_service_account_file(
                self.service_account_path, scopes=SCOPES
            )
            self.service = build('calendar', 'v3', credentials=creds)
            self.log.info("Service account authentication successful")
            return True
        except Exception as e:
            self.log.error(f"Service account authentication failed: {e}")
            return False
    
    def _authenticate_oauth(self) -> bool:
        """Authenticate using OAuth 2.0 flow."""
        if not self.credentials_path or not os.path.exists(self.credentials_path):
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
    
    def _authenticate_api_key(self) -> bool:
        """Authenticate using API key (read-only access)."""
        if not self.api_key:
            return False
        
        try:
            # API key authentication only supports read operations
            self.service = build('calendar', 'v3', developerKey=self.api_key)
            self.log.info("API key authentication successful (read-only access)")
            return True
        except Exception as e:
            self.log.error(f"API key authentication failed: {e}")
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
        
        # Check if we have write access (API key is read-only)
        if hasattr(self.service, 'developerKey'):
            self.log.error("Cannot create events with API key authentication (read-only)")
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
        
        # Check if we have write access
        if hasattr(self.service, 'developerKey'):
            self.log.error("Cannot create events with API key authentication (read-only)")
            return {"success": False, "error": "API key authentication is read-only"}
        
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
        
        # Check if we have write access
        if hasattr(self.service, 'developerKey'):
            self.log.error("Cannot delete events with API key authentication (read-only)")
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


def create_calendar_manager(credentials_path: Optional[str] = None,
                           token_path: str = "token.json",
                           service_account_path: Optional[str] = None,
                           use_adc: bool = False,
                           api_key: Optional[str] = None) -> GoogleCalendarManager:
    """
    Factory function to create and authenticate a Google Calendar manager.
    
    Args:
        credentials_path: Path to OAuth credentials file
        token_path: Path to store/retrieve OAuth token
        service_account_path: Path to service account JSON key file
        use_adc: Use Application Default Credentials
        api_key: Google API key for read-only operations
        
    Returns:
        GoogleCalendarManager: Authenticated calendar manager instance
    """
    manager = GoogleCalendarManager(
        credentials_path=credentials_path,
        token_path=token_path,
        service_account_path=service_account_path,
        use_adc=use_adc,
        api_key=api_key
    )
    
    if manager.authenticate():
        return manager
    else:
        raise RuntimeError("Failed to authenticate with Google Calendar API")


def create_calendar_manager_from_env() -> GoogleCalendarManager:
    """
    Create calendar manager using environment variables for authentication.
    
    Environment variables:
    - GOOGLE_CALENDAR_CREDENTIALS_PATH: Path to OAuth credentials file
    - GOOGLE_CALENDAR_TOKEN_PATH: Path to OAuth token file
    - GOOGLE_CALENDAR_SERVICE_ACCOUNT_PATH: Path to service account key file
    - GOOGLE_CALENDAR_USE_ADC: Use Application Default Credentials (true/false)
    - GOOGLE_CALENDAR_API_KEY: Google API key for read-only access
    
    Returns:
        GoogleCalendarManager: Authenticated calendar manager instance
    """
    return create_calendar_manager(
        credentials_path=os.getenv('GOOGLE_CALENDAR_CREDENTIALS_PATH'),
        token_path=os.getenv('GOOGLE_CALENDAR_TOKEN_PATH', 'token.json'),
        service_account_path=os.getenv('GOOGLE_CALENDAR_SERVICE_ACCOUNT_PATH'),
        use_adc=os.getenv('GOOGLE_CALENDAR_USE_ADC', 'false').lower() == 'true',
        api_key=os.getenv('GOOGLE_CALENDAR_API_KEY')
    )
