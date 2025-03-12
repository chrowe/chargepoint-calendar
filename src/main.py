import os
from datetime import datetime, timedelta
from python_chargepoint import ChargePoint
from google.oauth2 import service_account
from googleapiclient.discovery import build
from fetch_charging_sessions import fetch_charging_sessions

# Set up ChargePoint
chargepoint_username = os.getenv('CHARGEPOINT_USERNAME')
chargepoint_password = os.getenv('CHARGEPOINT_PASSWORD')
cp = ChargePoint(chargepoint_username, chargepoint_password)

# Set up Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'
calendar_id = os.getenv('GOOGLE_CALENDAR_ID')

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
        return datetime.utcnow() - timedelta(days=1)

def update_last_download_time(time):
    with open('last_download_time.txt', 'w') as file:
        file.write(time.isoformat())

def add_event_to_calendar(session):
    start_time = session['start_time']
    end_time = session['end_time']
    description = f"Charging session at home: {session['energy_kWh']} kWh"

    event = {
        'summary': 'EV Charging Session',
        'description': description,
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
    last_download_time = get_last_download_time()
    print(f"Last download time: {last_download_time}")
    
    # Fetch charging sessions
    response = fetch_charging_sessions(cp)
    month_info = response.json().get("charging_activity_monthly", {}).get("month_info", [])
    
    for sessions in month_info:
        for session in sessions.get("sessions", {}):
            from datetime import datetime

            # Convert timestamp in milliseconds to datetime
            start_time = datetime.fromtimestamp(session['start_time'] / 1000)
            end_time = datetime.fromtimestamp(session['end_time'] / 1000)

            session_time = session['session_time'] / 60000 / 60
            miles_added = session['miles_added']

            #add_event_to_calendar(session)
            print(f'{session_time:.2f} hour long session from {start_time} to {end_time}, Energy:  kWh and {miles_added} miles added')

    #update_last_download_time(datetime.datetime.now(datetime.UTC))

if __name__ == '__main__':
    main()


