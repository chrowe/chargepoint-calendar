import time
import os

def fetch_charging_sessions(client):
    # Get the first 10 charging sessions
    response = client.session.get(f'{client.global_config.endpoints.mapcache}v2?{{"user_id":{client.user_id},"charging_activity_monthly":{{}}}}')
    # Get additional charging sessions in batches of 10
    for i in range(1):
        page_offset = response.json()["charging_activity_monthly"]["page_offset"]
        if page_offset == "last_page":
            break
        print(i, page_offset)
            
        req = f'{client.global_config.endpoints.mapcache}v2?{{"user_id":{client.user_id},"charging_activity_monthly":{{"page_offset":"{page_offset}"}}}}'
        response = client.session.get(req)

        # Maybe not necessary to wait this long between requests?
        time.sleep(5)
    
    return response



    {"charging_activity_monthly":{"page_size":20,"show_address_for_home_sessions":true}}
    {"charging_activity_monthly":{"page_offset":"p_2025_1","page_size":20,"show_address_for_home_sessions":true}}
    {"charging_activity_monthly":{"page_offset":"p_2024_12","page_size":20,"show_address_for_home_sessions":true}}