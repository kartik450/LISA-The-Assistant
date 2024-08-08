import requests

def get_current_location():
    response = requests.get("https://ipinfo.io")
    data = response.json()
    lat, lon = map(float, data['loc'].split(','))
    return data['city'], data['region'], data['country'], lat, lon

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=precipitation_probability"
    response = requests.get(url)
    data = response.json()
    if 'current_weather' not in data:
        print(f"Error: {data}")
        return None
    return data

if __name__ == "__main__":
    city, region, country, lat, lon = get_current_location()
    weather = get_weather(lat, lon)
    
    if weather:
        current_weather = weather['current_weather']
        precipitation_probability = weather['hourly']['precipitation_probability'][0] if 'precipitation_probability' in weather['hourly'] else 'No data'
        
        print(f"Location: {city}, {region}, {country} ({lat}, {lon})")
        print(f"Weather Code: {current_weather['weathercode']}")
        print(f"Temperature: {current_weather['temperature']}°C")
        print(f"Chance of Rain: {precipitation_probability}%")
    else:
        print("Failed to retrieve weather data")
