from wink import WinkClient
from sources import uber, muni, weather, credit_card
from datetime import datetime

#FILL THESE IN FOR YOUR NEEDS
HOME_LATLNG = (0, 0)

MONTHLY_BUDGET = 100

client = WinkClient(
    client_id='TODO',
    client_secret='TODO',
    access_token='Log in to get this',
    refresh_token='Log in to get this')

plaid_client = credit_card.make_client(
        "PLAID_CLIENT_ID",
        "PLAID_SECRET",
        "PLAID_PUBLIC_KEY")

credit_card_access_token = "Get via plaid link"

def update(throttle=True):
    minute = datetime.now().minute
    print str(datetime.now())
    nimbus = client.devices()[0]

    #Dial 1: Date & Time
    datetime_dial = nimbus.dials[0]
    update_datetime_dial(datetime_dial)
    client.update_device(datetime_dial)

    #Dial 2: Weather
    #only update this every 20 minutes
    if not throttle or minute % 20 == 0:
        weather_dial = nimbus.dials[1]
        update_weather_dial(weather_dial)
        client.update_device(weather_dial)
    else:
        print "Keeping weather the same"

    #Dial 3: Sun position & moon phase
    #only update this every 20 minutes
    if not throttle or minute % 20 == 0:
        sun_and_moon_dial = nimbus.dials[2]
        update_sun_and_moon_dial(sun_and_moon_dial)
        client.update_device(sun_and_moon_dial)
    else:
        print "Keeping sun and moon the same"

    #Dial 4: budget
    #only update this every 20 minutes
    if not throttle or minute % 20 == 0:
        budget_dial = nimbus.dials[3]
        update_budget_dial(budget_dial)
        client.update_device(budget_dial)
    else:
        print "Keeping budget the same"

def update_datetime_dial(dial):
    #label: Date
    #dial: Clock time
    #secondary label: Clock time

    now = datetime.now()
    dial.description = now.stftime("%H:%M")
    dial.value = (now.hour % 12) * 30 + now.minute / 2
    dial.label = now.stftime("%a%-m-%-d")

def update_weather_dial(dial):
    #display: low/high
    #dial: chance of precipitation
    low, high, precip = weather.get_weather(HOME_LATLNG)
    print "Weather: %f, %f, %f" % (low, high, precip)

    dial.label = "%d>-%d>" % (int(low), int(high))
    dial.value = max(precip * 350, 1)
    dial.description = "%d%% Rain" % (int(precip * 100))

def update_sun_and_moon_dial(dial):
    #label: Next sunrise/sunset (e.g. "Up: 7:07", "Down: 5:15")
    #dial: Moon phase
    #secondary label: Moon phase
    next_sunchange_time, next_sunchange_is_sunrise, moon_phase = weather.get_sun_and_moon(HOME_LATLNG)

    if next_sunchange_is_sunrise:
        dial.label = "Up: %s" % (next_sunchange_time.strftime("%-I:%M"))
    else:
        dial.label = "Down: %s" % (next_sunchange_time.strftime("%-I:%M"))

    dial.value = max(min(moon_phase * 360, 355), 1)
    if moon_phase <= 0.05:
        dial.description = "New Moon"
    elif moon_phase <= 0.2:
        dial.description = "Wax cres"
    elif moon_phase <= 0.3:
        dial.description = "1st Quar"
    elif moon_phase <= 0.45:
        dial.description = "Wax Gibb"
    elif moon_phase <= 0.55:
        dial.description = "Full"
    elif moon_phase <= 0.7:
        dial.description = "Wan Gibb"
    elif moon_phase <= 0.8:
        dial.description = "3rd Quar"
    elif moon_phase <= 0.95:
        dial.description = "Wan Cres"
    else:
        dial.description = "New Moon"

def update_budget_dial(dial):
    #display: money spent this month
    #dial: % of budget
    budget = MONTHLY_BUDGET
    spent = credit_card.get_this_month_spend(plaid_client, credit_card_access_token)
    print "Spent: $%.2f" % (spent)
    fraction_spent = spent * 1.0 / budget

    dial.label = "$%.2f" % (spent)
    dial.value = max(min(fraction_spent * 355, 355), 1)
    dial.description = "%.1f%%" % (fraction_spent * 100)

if __name__ == '__main__':
    #update()
    update(throttle=False)
