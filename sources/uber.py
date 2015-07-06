import requests

SERVER_TOKEN = "REGISTER TO GET THIS"
API_ENDPOINT = "https://api.uber.com"

DEFAULT_END = (0,0) #can be anywhere nearby your start location
DEFAULT_TYPE = "uberX"


def request(method, path, **kwargs):
    headers = kwargs.setdefault('headers', {})
    headers['Authorization'] = 'Token %s' % (SERVER_TOKEN)

    url = API_ENDPOINT + ('/' if path[0] != '/' else '') + path
    return requests.request(method, url, **kwargs)


def get(path, **kwargs):
    return request("GET", path, **kwargs)


def get_product_id(latlng, name=DEFAULT_TYPE):
    data = get("/v1/products", params={"latitude": latlng[0], "longitude": latlng[1]}).json()
    for prod in data.get("products", []):
        if prod.get("display_name") == name:
            return prod.get("product_id", None)
    return None


def get_price_info(latlng, destination=DEFAULT_END, name=DEFAULT_TYPE):
    #returns (estimate, surge)
    params = {
        "start_latitude": latlng[0],
        "start_longitude": latlng[1],
        "end_latitude": destination[0],
        "end_longitude": destination[1]
    }
    data = get("/v1/estimates/price", params=params).json()

    for prod in data.get("prices", []):
        if prod.get("display_name") == name:
            return (prod.get("estimate"), prod.get("surge_multiplier"))
    return None


def get_time_info(latlng, name=DEFAULT_TYPE):
    #returns estimate in seconds
    params = {
        "start_latitude": latlng[0],
        "start_longitude": latlng[1],
    }
    data = get("/v1/estimates/time", params=params).json()

    for prod in data.get("times", []):
        if prod.get("display_name") == name:
            return prod.get("estimate")
    return None


def get_info(latlng, name="uberX"):
    #Returns (wait_time, surge)
    p_estimate, surge = get_price_info(latlng, name=name)
    t_estimate = get_time_info(latlng, name=name)
    return (t_estimate, surge)

if __name__ == '__main__':
    print get_info(DEFAULT_END)
