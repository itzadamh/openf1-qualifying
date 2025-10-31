import requests

# ------ Functions ------
def menu():
    print("""
          -------------------------------------
          |                                   |
          |   My F1 Qualifying mini project   |
          |         powered by OpenF1         |
          |                                   |
          -------------------------------------
Note: Fastest Lap is based on the furthest qualifying stage reached.
If their lap is shown as "None", they may have DNF'd, DNS'd, or been DSQ'd.
Additionally, the lap time should be accurate, but not guaranteed 100%. 
          """)
    
    country = input("Please enter the country of the race (e.g. Singapore): \n")
    year = int(input("Please enter the year of the race: \n"))
    print()
    
    return country, year
    
def get_meetingkey(country, year):
    url = f"https://api.openf1.org/v1/meetings?country_name={country}&year={year}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        meetings = response.json()
        
        if not meetings:
            return None

        # If there's only one meeting, use it.
        if len(meetings) == 1:
            # print separator/loading message for single meeting (race)
            load_message = f"Loading {country} {year} Qualifying results..."
            print("-" * (len(load_message) + 3))
            print(load_message)
            print("-" * (len(load_message) + 3))
            return meetings[0]['meeting_key']

        # Multiple meetings: show a list and ask the user to choose.
        print(f"Multiple meetings found for {country} {year}:")
        for i, m in enumerate(meetings, start=1):
            # Build a friendly label from available fields (fall back to meeting_key)
            label = m.get('meeting_name') or m.get('meeting_location') or m.get('circuit_name') or m.get('meeting_key')
            # If the API provides a date or round, show it too (optional)
            date = m.get('start_date') or m.get('date')
            if date:
                label = f"{label} ({date})"
            print(f"  {i}. {label}")

        while True:
            choice = input(f"Select meeting (1-{len(meetings)}) or 'q' to cancel: ").strip()
            if choice.lower() == 'q':
                return None
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(meetings):
                    # print separator/loading message after selection
                    load_message = f"Loading {country} {year} Qualifying results..."
                    print("-" * (len(load_message) + 3))
                    print(load_message)
                    print("-" * (len(load_message) + 3))
                    return meetings[idx - 1]['meeting_key']
            print("Invalid selection. Please try again.")

    except requests.RequestException as e:
        print(f"Error fetching meeting key: {e}")
        return None

def get_sessionkey(meeting_key):
    if meeting_key is None:
        return None
    
    session_name = "Qualifying"
    url = f"https://api.openf1.org/v1/sessions?meeting_key={meeting_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        sessions = response.json()
        
        for session in sessions:
            if session["session_name"].lower() == session_name.lower():
                return session['session_key']
        
        return None
    except requests.RequestException as e:
        print(f"Error fetching session key: {e}")
        return None

def format_laptime(seconds):
    # No lap duration, could be did not finish/start, disqualification
    if seconds is None:
        return None
    
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    ms = int(round((remaining_seconds - int(remaining_seconds)) * 1000, 3)) # Decimal part of the seconds is multiplied by 1000
    
    # Handle the edge case where milliseconds round up to 1000
    if ms == 1000:
        ms = 0
        remaining_seconds += 1
        
    return f"{minutes:02}:{int(remaining_seconds):02}.{ms:03}"

# ------ Main ------
def main():
    country, year = menu()
    meeting_key = get_meetingkey(country, year)
    
    if meeting_key is None:
        print(f"Error: Could not find a meeting for {country} {year}.")
        return
    
    session_key = get_sessionkey(meeting_key)
    
    if session_key is None:
        print(f"Error: Could not find qualifying session for {country} {year}.")
        return

    url = f"https://api.openf1.org/v1/starting_grid?session_key={session_key}&position>=1"
    driver_url = f"https://api.openf1.org/v1/drivers?session_key={session_key}"

    response = requests.get(url)
    driver_response = requests.get(driver_url)

    if response.status_code == 200 and driver_response.status_code == 200:
        data = response.json()
        driver_data = driver_response.json()
        print(f"Found {len(data)} starting positions.")
        print(f"Found {len(driver_data)} drivers.\n")

        # Get the set of driver numbers we actually need
        needed_driver_numbers = {item['driver_number'] for item in data}
        
        driver_number_to_names = {}
        driver_number_to_team = {}

        # Only process drivers that are in the qualifying results
        for driver in driver_data:
            driver_number = driver['driver_number']
            if driver_number in needed_driver_numbers:
                driver_number_to_names[driver_number] = driver['full_name']
                driver_number_to_team[driver_number] = driver['team_name']


        # Qualifying loop
        for item in data:
            driver_number = item['driver_number']
            full_name = driver_number_to_names[driver_number]
            team = driver_number_to_team[driver_number]
            laptime = format_laptime(item["lap_duration"])

            print(f"Driver: {full_name} | {driver_number}")
            print(f"Team: {team}")
            print(f"Position: {item['position']}")
            print(f"Fastest Lap: {laptime}\n")
            
            # Hide Meeting and Session key for now
            # print(f"Meeting Key: {item['meeting_key']}")
            # print(f"Session Key: {item['session_key']}")
            
    else:
        print("Error:", response.status_code, response.text)
        
if __name__ == "__main__":
    main()
    input("Press Enter to exit...")