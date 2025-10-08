import requests
url = "https://api.openf1.org/v1/starting_grid?session_key=9892&position>=1"
driver_url = "https://api.openf1.org/v1/drivers"

response = requests.get(url)
driver_response = requests.get(driver_url)

# ------ Functions ------

def format_laptime(seconds):
    # No lap duration, could be did not finish/start, disqualification
    if seconds is None:
        return "None"
    
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    ms = int(round((remaining_seconds - int(remaining_seconds)) * 1000, 3)) # decimal part of the seconds is multiplied by 1000
    
    return f"{minutes:02}:{int(remaining_seconds):02}.{ms:03}"

# ------ Main ------

if response.status_code & driver_response.status_code == 200:
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