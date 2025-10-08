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

    for driver in driver_data:
        driver_number = driver['driver_number']
        full_name = driver['full_name']
        driver_number_to_names[driver_number] = full_name


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
# further improvements could mean changing meeting key to separately fetch the name of the race?
# same with session key, it gives the key but surely we could fetch the title/type aka if its practice 1 etc
# same with driver number, display the driver name (or name + number?)
# changing the format of lap duration to be minutes/seconds?

# more functionality could include allowing user inputs for specific races and sessions
# gap between the leader? or gap between each other