import requests
from lxml import etree

TOKEN = "REGISTER TO GET THIS"
API_ENDPOINT = "http://services.my511.org/Transit2.0/"

#docs @ http://511.org/docs/RTT%20API%20V2.0%20Reference.pdf

def get(path, **kwargs):
    kwargs.setdefault('params', {})
    kwargs['params']['token'] = TOKEN

    url = API_ENDPOINT + ('/' if path[0] != '/' else '') + path
    r = requests.get(url, **kwargs)
    return etree.fromstring(r.text)


#Route: (stop, direction)
def get_stops(route):
    #Stop codes: http://services.my511.org/Transit2.0/GetStopsForRoute.aspx?token=<token>&routeIDF=SF-MUNI~45~Inbound
    xml = get("GetStopsForRoute.aspx", params={'routeIDF': 'SF-MUNI~%s~%s' % (route[0], route[1])})
    stoplist = xml.xpath('/RTT/AgencyList/Agency/RouteList/Route/RouteDirectionList/RouteDirection/StopList')
    return [(stop.get("name"), stop.get("StopCode")) for stop in stoplist[0].iter("Stop")]


#Route: (stop, direction)
def get_times(stop, route):
    #Info: http://services.my511.org/Transit2.0/GetNextDeparturesByStopCode.aspx?token=<token>&stopcode=16748
    xml = get("GetNextDeparturesByStopCode.aspx", params={'stopcode': stop})
    routeCode = route[0]
    routeDirection = route[1]
    xpath = ("/RTT/AgencyList/Agency/RouteList/Route[@Code='%s']"
                       "/RouteDirectionList/RouteDirection[@Code='%s']"
                       "/StopList/Stop[@StopCode='%s']/DepartureTimeList/DepartureTime") % (routeCode, routeDirection, stop)
    times = xml.xpath(xpath)
    return [int(time.text) for time in times]


if __name__ == '__main__':
    DEFAULT_STOP = 0
    DEFAULT_ROUTE = (0, "Inbound")

    print get_times(DEFAULT_STOP, DEFAULT_ROUTE)
