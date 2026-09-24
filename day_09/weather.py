import requests

# Coordinate for Kolkata: Lat 22.5726, Long 88.3639
url = "https://api.open-meteo.com/v1/forecast?latitude=22.5726&longitude=88.3639&current_weather=true"
data = requests.get(url).json()

temp = data["current_weather"]["temperature"]
print(f"Current Kolkata Temperature: {temp}°C")