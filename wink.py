import requests


class WinkClient:
    API_ENDPOINT = "https://winkapi.quirky.com"

    def __init__(self, client_id, client_secret, access_token=None, refresh_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token

    def api_url(self, path):
        return self.API_ENDPOINT + ('/' if path[0] != '/' else '') + path

    def is_authenticated(self):
        return self.access_token is not None

    def authenticate(self, username, password):
        data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "username": username,
                "password": password,
                "grant_type": "password"
        }

        resp = requests.post(self.api_url('/oauth2/token'), json=data)
        if resp.status_code == requests.codes.OK:
            auth = resp.json()
            self.access_token = auth['access_token']
            self.refresh_token = auth['refresh_token']
        else:
            print "Bad response", resp
            raise "Bad response while authenticating"

    def refresh_auth(self):
        assert self.refresh_token is not None, "Must have a refresh token, call authenticate() first"

        data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token"
        }

        resp = requests.post(self.api_url('/oauth2/token'), json=data)
        if resp.status_code == requests.codes.OK:
            auth = resp.json()
            self.access_token = auth['access_token']
            self.refresh_token = auth['refresh_token']
        else:
            print "Bad response", resp
            raise "Bad response while refreshing"

    def request(self, method, path, **kwargs):
        headers = kwargs.setdefault('headers', {})
        headers['Authorization'] = 'Bearer %s' % (self.access_token)

        url = self.api_url(path)

        r = requests.request(method, url, **kwargs)
        if r.status_code == 200:
            return r.json()
        else:
            print ">>> Non-200 status code: ", r.status_code, r
            if r.status_code == 401:
                print "Refreshing auth token"
                self.refresh_auth()
                return self.request(method, path, **kwargs)
            else:
                raise "Bad response", r.text

    def get(self, path, **kwargs):
        return self.request('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self.request('POST', path, **kwargs)

    def put(self, path, **kwargs):
        return self.request('PUT', path, **kwargs)

    def devices(self):
        assert self.is_authenticated(), "You must authenticate before calling this method"

        data = self.get('/users/me/wink_devices')['data']

        devices = []
        for device_data in data:
            #dynamic loading and creation of devices. *whistle*
            device_name = device_data['model_name']
            module = __import__('devices.%s' % device_name, globals(), locals(), [device_name])
            if not module:
                raise "Don't know how to support device '%s'" % (device_data['model_name'])

            device = vars(module)[device_name].from_json(device_data)
            devices.append(device)

        return devices

    def update_device(self, device):
        return self.put(device.url(), json=device.configuration())

if __name__ == '__main__':
    print "Fetch the access token for a user:"
    client_id = raw_input("Wink Client ID:").strip()
    client_secret = raw_input("Wink Client Secret:").strip()

    username = raw_input("Wink Username:").strip()
    password = raw_input("Wink Password:").strip()

    client = WinkClient(client_id, client_secret, None, None)
    client.authenticate(username, password)
    print "Access Token:", client.access_token
    print "Refresh Token:", client.refresh_token
