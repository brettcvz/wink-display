import requests

API_ENDPOINT = "https://api.forecast.io/forecast/"
TOKEN = "REGISTER TO GET THIS"


def get_info(latlng):
    url = API_ENDPOINT + "%s/%f,%f" % (TOKEN, latlng[0], latlng[1])
    data = requests.get(url).json()
    today = data['daily']['data'][0]

    return (today['apparentTemperatureMin'], today['apparentTemperatureMax'], today['precipProbability'])


if __name__ == '__main__':
    DEFAULT_LATLNG = (0, 0)
    print get_info(DEFAULT_LATLNG)
