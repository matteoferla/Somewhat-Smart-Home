import os
from homesensing_api import HomieAPI

for key in ('HOMESENSING_URL', 'HOMESENSING_KEY', 'SLACK_HOOK'):
    assert key in os.environ, f'Config error: missing {key}'

homie = HomieAPI(base_url=os.environ['HOMESENSING_URL'], key=os.environ['HOMESENSING_KEY'])

location = 'garden'

# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime as dt

from .wind import Anemometer
from .rain import RainGauge
from .temp import Temperature
from .core import detect_undervoltage, send_slack

if False:
    sampling_window = 60 * 60
    wind = Anemometer(15, window=sampling_window, radius=0.07)
    rain = RainGauge(18, window=sampling_window, volume=0.0085, area=0.0063615)
    temp = Temperature(4)

    # ------------------------------------------------------

    def alert_undervoltage():
        if detect_undervoltage:
            send_slack(f'{location} reports undervoltage')


    def safety(fun):
        def wrapped():
            try:
                fun()
            except Exception as error:
                voltage = 'undervoltage' if detect_undervoltage() else 'normal voltage'
                send_slack(f'{location}: {fun.__name__} {error.__class__.__name__}: {error} ({voltage})')

        return wrapped


    @safety
    def sense_temp():
        t, h = temp()
        homie.record(sensor=f'{location}:temperature',
                     value=t,
                     datetime=dt.datetime.now())

        homie.record(sensor=f'{location}:humidity',
                     value=h,
                     datetime=dt.datetime.now())


    @safety
    def sense_rain():
        homie.record(sensor=f'{location}:rain_rate',
                     value=rain.rate,
                     datetime=dt.datetime.now())


    @safety
    def sense_wind():
        homie.record(sensor=f'{location}:wind_speed',
                     value=wind.speed,
                     datetime=dt.datetime.now())


    # ------------------------------------------------------
    sense_temp()
    sense_rain()
    sense_wind()

    scheduler = BlockingScheduler()
    scheduler.add_job(func=alert_undervoltage, trigger="interval", seconds=sampling_window)
    scheduler.add_job(func=sense_temp, trigger="interval", seconds=sampling_window)
    scheduler.add_job(func=sense_rain, trigger="interval", seconds=sampling_window)
    scheduler.add_job(func=sense_wind, trigger="interval", seconds=sampling_window)
    scheduler.start()
