import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class CalendarManager:
    """will handle auth and communicate w/ google calendar"""

    SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

    credentials_path = "credentials.json"

    def __init__(self, credentials_path):
        self.credentials_path = credentials_path
        self.service = self._authenticate()

    def _authenticate(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return build("calendar", "v3", credentials=creds)


    def add_event(self, event_body):
        body = event_body
        calendarId = "869bb6fc60cb3801eb2b1ffce5bcef7bbfd0681cdc08f37766489bab62448442@group.calendar.google.com"
        return self.service.events().insert(calendarId, body).execute()
