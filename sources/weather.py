import requests
from datetime import datetime

API_ENDPOINT = "https://api.forecast.io/forecast/"
TOKEN = "REGISTER TO GET THIS"


def get_weather(latlng):
    url = API_ENDPOINT + "%s/%f,%f" % (TOKEN, latlng[0], latlng[1])
    data = requests.get(url).json()
    today = data['daily']['data'][0]

    return (today['apparentTemperatureMin'], today['apparentTemperatureMax'], today['precipProbability'])

def get_sun_and_moon(latlng):
    url = API_ENDPOINT + "%s/%f,%f" % (TOKEN, latlng[0], latlng[1])
    data = requests.get(url).json()
    today = data['daily']['data'][0]
    tomorrow = data['daily']['data'][1]

    moon_phase = today["moonPhase"]

    now = datetime.now()
    sunset = datetime.fromtimestamp(today["sunsetTime"])
    sunrise = datetime.fromtimestamp(today["sunriseTime"])
    if now < sunrise:
        #return today's sunrise
        return sunrise, True, moon_phase
    elif now < sunset:
        #return today's sunset
        return sunset, False, moon_phase
    else:
        #It's after sunset today, return tomorrow's sunrise
        return datetime.fromtimestamp(tomorrow["sunriseTime"]), True, moon_phase

if __name__ == '__main__':
    DEFAULT_LATLNG = (0, 0)
    print get_weather(DEFAULT_LATLNG)
    print get_sun_and_moon(DEFAULT_LATLNG)
