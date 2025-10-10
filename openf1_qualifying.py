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
    
    load_message = f"Loading {country} {year} Qualifying results..."
    
    print("-" * (len(load_message) + 3))
    print(load_message)
    print("-" * (len(load_message) + 3))
    
    return country, year
    
def get_meetingkey(country, year):
    url = f"https://api.openf1.org/v1/meetings?country_name={country}&year={year}"
    response = requests.get(url)
    meetings = response.json()
    
    if meetings:
        return meetings[0]['meeting_key']
    else:
        return None

def get_sessionkey(meeting_key):
    session_name = "Qualifying"
    url = f"https://api.openf1.org/v1/sessions?meeting_key={meeting_key}"
    response = requests.get(url)
    sessions = response.json()
    
    for session in sessions:
        if session["session_name"].lower() == session_name.lower():
            return session['session_key']
    
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
    session_key = get_sessionkey(meeting_key)

    url = f"https://api.openf1.org/v1/starting_grid?session_key={session_key}&position>=1"
    driver_url = "https://api.openf1.org/v1/drivers"

    response = requests.get(url)
    driver_response = requests.get(driver_url)

    if response.status_code and driver_response.status_code == 200:
        data = response.json()
        driver_data = driver_response.json()
        print(f"Found {len(data)} starting positions.")
        print(f"Found {len(data)} drivers.\n")

        driver_number_to_names = {}
        driver_number_to_team = {}

        # Creates the dictionary with key, value pairs for drivers and their number
        for driver in driver_data:
            driver_number = driver['driver_number']
            full_name = driver['full_name']
            team = driver['team_name']

            driver_number_to_names[driver_number] = full_name
            driver_number_to_team[driver_number] = team


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