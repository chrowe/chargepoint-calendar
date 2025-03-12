import time
import os
from python_chargepoint import ChargePoint


def fetch_charging_sessions(pages):
    session_list = []

    # Set up ChargePoint
    chargepoint_username = os.getenv('CHARGEPOINT_USERNAME')
    chargepoint_password = os.getenv('CHARGEPOINT_PASSWORD')
    client = ChargePoint(chargepoint_username, chargepoint_password)


    # Get the first 10 charging sessions
    response = client.session.get(f'{client.global_config.endpoints.mapcache}v2?{{"user_id":{client.user_id},"charging_activity_monthly":{{}}}}')
    # Get additional charging sessions in batches of 10
    for i in range(pages):
        page_offset = response.json()["charging_activity_monthly"]["page_offset"]
        if page_offset == "last_page":
            break
        print(i, page_offset)
            
        req = f'{client.global_config.endpoints.mapcache}v2?{{"user_id":{client.user_id},"charging_activity_monthly":{{"page_offset":"{page_offset}"}}}}'
        response = client.session.get(req)

        # Fetch charging sessions
        month_info = response.json().get("charging_activity_monthly", {}).get("month_info", [])
    
        for sessions in month_info:
            for session in sessions.get("sessions", {}):
                session_list.append(session)

        
        # Maybe not necessary to wait this long between requests?
        time.sleep(1)


    return session_list