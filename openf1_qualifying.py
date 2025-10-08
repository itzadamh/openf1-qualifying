import requests
url = "https://api.openf1.org/v1/starting_grid?session_key=9892&position>=1"
driver_url = "https://api.openf1.org/v1/drivers"


response = requests.get(url)
driver_response = requests.get(driver_url)

if response.status_code & driver_response.status_code == 200:
    data = response.json()
    driver_data = driver_response.json()
    print(f"Found {len(data)} starting positions.")
    print(f"Found {len(data)} drivers.")

    driver_number_to_names = {}

    # Creates the dictionary with key, value pairs for drivers and their number
    for driver in driver_data:
        driver_number = driver['driver_number']
        full_name = driver['full_name']
        driver_number_to_names[driver_number] = full_name

    # Qualifying loop
    for item in data:
        driver_number = item['driver_number']
        full_name = driver_number_to_names[driver_number]

        print("\n")
        print(f"Driver: {full_name} | {driver_number}")
        print(f"Position: {item['position']}")
        print(f"Lap Duration: {item['lap_duration']}")
        print(f"Meeting Key: {item['meeting_key']}")
        print(f"Session Key: {item['session_key']}")
        
else:
    print("Error:", response.status_code, response.text)