from wink import WinkClient
from sources import uber, muni, weather, mint
from datetime import datetime

#FILL THESE IN FOR YOUR NEEDS
HOME_LATLNG = (0, 0)
MUNI_STOP = 0
MUNI_ROUTE = (0, "Inbound")

MINT_LOGIN = {
        'email': '',
        'password': '',
        'account_id': 12345
}
MONTHLY_BUDGET = 100

client = WinkClient(
    client_id='TODO',
    client_secret='TODO',
    access_token='Log in to get this',
    refresh_token='Log in to get this')


def update():
    minute = datetime.now().minute
    print str(datetime.now())
    nimbus = client.devices()[0]

    #Dial 1: uber
    uber_dial = nimbus.dials[0]
    update_uber_dial(uber_dial)
    client.update_device(uber_dial)

    #Dial 2: muni
    muni_dial = nimbus.dials[1]
    update_muni_dial(muni_dial)
    client.update_device(muni_dial)

    #Dial 3: weather
    #only update this every 20 minutes
    if minute % 20 == 0:
        weather_dial = nimbus.dials[2]
        update_weather_dial(weather_dial)
        client.update_device(weather_dial)
    else:
        print "Keeping weather the same"

    #Dial 4: budget
    #only update this every 20 minutes
    if minute % 20 == 0:
        budget_dial = nimbus.dials[3]
        update_budget_dial(budget_dial)
        client.update_device(budget_dial)
    else:
        print "Keeping budget the same"


def update_uber_dial(dial):
    #label: wait time
    #dial: surge pricing (1 is up[0], 1.25 is 90, 1.5 is 120, 1.75 is 180, 2 is 240, higher is past)

    wait, surge = uber.get_info(HOME_LATLNG)
    print "Uber: %d, %f" % (wait, surge)

    dial.description = "%.1fX" % (surge)
    if surge <= 1.01:
        dial.value = 1
    elif surge <= 1.25:
        dial.value = (surge - 1) * 90 / .25
    elif surge <= 1.5:
        dial.value = (surge - 1) * 120 / .5
    elif surge <= 1.75:
        dial.value = (surge - 1) * 180 / .75
    elif surge <= 2:
        dial.value = (surge - 1) * 240
    else:
        dial.value = min(surge * 325 / 3, 325)

    dial.label = "%.1f min" % (wait / 60.0)


def update_muni_dial(dial):
    #label: time till 45 at union street
    #dial: delay between next bus and the one after that (out of 30 minutes)
    #token = "d8b9a58b-8aea-48a9-b33a-ee40d227a281"

    times = muni.get_times(MUNI_STOP, MUNI_ROUTE)
    print "Muni: %s" % (times)

    dial.label = "%d min" % (times[0])
    dial.value = max(min((times[1] - times[0]) / 30.0, 1) * 350, 1)
    dial.description = ", ".join(map(str, times))


def update_weather_dial(dial):
    #display: low/high
    #dial: chance of precipitation
    low, high, precip = weather.get_info(HOME_LATLNG)
    print "Weather: %f, %f, %f" % (low, high, precip)

    dial.label = "%d>-%d>" % (int(low), int(high))
    dial.value = max(precip * 350, 1)
    dial.description = "%d%% Rain" % (int(precip * 100))


def update_budget_dial(dial):
    #display: money spent this month
    #dial: % of budget
    budget = MONTHLY_BUDGET
    spent = -1 * mint.get_balance(**MINT_LOGIN)
    print "Mint: $%.2f" % (spent)

    dial.label = "$%.2f" % (spent)
    dial.value = max((budget - spent) / budget * 355, 1)
    dial.description = "%.1f%%" % (spent / budget * 100)


if __name__ == '__main__':
    update()
