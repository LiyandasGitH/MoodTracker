import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        moods = {
            "1": {"name": "Very Happy", "colour", "5"},
            "2": {"name": "Sort of Happy", "colour", "2"},
            "3": {"name": "Neutral", "colour", "8"},
            "4": {"name": "Uninterested", "colour", "6"},
            "5": {"name": "Very Uniterested", "colour", "1"}
        }

        print("\n--- Aya's Mood Tracker ---")
        for key, value in moods.items():
            print(f"{key}: {value['name']}")

        choice = input("\nHow are you feeling today (1-5)\t")
        notes = input("Any notes for today?\t")

        if choice in moods:
            selected = moods[choice]
            today = datetime.date.today().isoformat()

            event_body = {
                'summary': f"Mood: {selected['name']}",
                'description': notes,
                'start': {'date': today},
                'end': {'date': today},
                'colourId': selected['colour'],
            }

            event = service.events().insert(calendarId='primary', body=event_body).execute()
            print(f"\nSuccessfully logged! View here: {event.get('htmlLink')}")

        else:
            print("Invalid choice. No mood logged.")
    

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()