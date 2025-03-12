import os
from datetime import datetime, timedelta, UTC
from google.oauth2 import service_account
from googleapiclient.discovery import build
from fetch_charging_sessions import fetch_charging_sessions

# Set up Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'
calendar_id = os.getenv('GOOGLE_CALENDAR_ID')
user_email = os.getenv('USER_EMAIL')

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)


def get_last_download_time():
    # Implement a way to store and retrieve the last download time
    # For example, use a file, database, or environment variable
    try:
        with open('last_download_time.txt', 'r') as file:
            return datetime.fromisoformat(file.read().strip())
    except FileNotFoundError:
        return datetime.now(UTC) - timedelta(days=1)
    

def update_last_download_time(time):
    with open('last_download_time.txt', 'w') as file:
        file.write(time.isoformat())
    

def get_or_create_calendar(service, calendar_name, user_email):
    # Check if the calendar exists
    calendar_list = service.calendarList().list().execute()
    for calendar in calendar_list['items']:
        if calendar['summary'] == calendar_name:
            return calendar['id']
    
    # Create the calendar if it doesn't exist
    calendar = {
        'summary': calendar_name,
        'timeZone': 'UTC'
    }
    created_calendar = service.calendars().insert(body=calendar).execute()
    
    # Give yourself access to the calendar
    rule = {
        'scope': {
            'type': 'user',
            'value': user_email,
        },
        'role': 'owner'
    }
    service.acl().insert(calendarId=created_calendar['id'], body=rule).execute()
    
    return created_calendar['id']

def add_event_to_calendar(session):
    current_charging = session['current_charging']
    if current_charging != "done":
        print("Session is still ongoing, skipping event creation.")
    else:
        from datetime import datetime
        # Convert timestamp in milliseconds to datetime
        start_time = datetime.fromtimestamp(session['start_time'] / 1000)
        end_time = datetime.fromtimestamp(session['end_time'] / 1000)

        session_time = session['session_time'] / 60000 / 60
        energy_kwh = session['energy_kwh']
        miles_added = session['miles_added']

        session_description = f'{session_time:.2f} hour long session from {start_time} to {end_time}, Energy: {energy_kwh} kWh and {miles_added} miles added'

        event = {
            'summary': f'EV Charging Session: {energy_kwh:.2f} kWh',
            'description': session_description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
        }

        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")

def main():
    global calendar_id
    calendar_id = get_or_create_calendar(service, "Chargepoint charging", user_email)
    print(f"Using calendar ID: {calendar_id}")

    last_download_time = get_last_download_time()
    print(f"Last download time: {last_download_time}")

    sessions = fetch_charging_sessions(100)

    # Save sessions to a file
    with open('sessions.json', 'w') as f:
        import json
        json.dump(sessions, f)
 
    for session in sessions:
        # Uncomment the following line to add events to Google Calendar
        add_event_to_calendar(session)

    #update_last_download_time(datetime.now(UTC))

if __name__ == '__main__':
    main()
