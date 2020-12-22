# Code from sensors next to plants
# 192.168.1.3
# "plant"

"""



$ sudo nano /etc/systemd/system/scheduled.service

[Unit]
Description=Run python scheduler
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/
ExecStart=python3 /home/pi/scheduled_tasks.py
Restart=always

[Install]
WantedBy=multi-user.target
"""

# ----------------------------------------------------------------------------------------------------------------------

from homesensing_api import HomieAPI

homie = HomieAPI(base_url='http://192.168.0.75:8000', key='properbaltic')

# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
scheduler = BlockingScheduler()

import datetime as dt

# ======================================================================================================================

# https://github.com/matteoferla/Raspberry-Pi-irrigator/blob/master/models.py
import time
from w1thermsensor import W1ThermSensor
time.sleep(1)

# ----------------------------------------------------------------------------------------------------------------------
# Local mirror

# https://github.com/matteoferla/Raspberry-Pi-irrigator/blob/master/models.py
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Measurement(Base):
    """
    The table containing the measurements.
    """
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)
    value = db.Column(db.Float, unique=False, nullable=False)
    sensor = db.Column(db.String, unique=False, nullable=False)

#### Lastly ####
engine = db.create_engine('sqlite:///local_backup.sqlite')
Session = sessionmaker()
session = Session(bind=engine)
Base.metadata.create_all(engine)

# ----------------------------------------------------------------------------------------------------------------------

def sense_probes():
    for sensor in W1ThermSensor.get_available_sensors():
        datum = Measurement(datetime=dt.datetime.now(),
                            value=sensor.get_temperature(),
                            sensor=sensor.id)
        session.add(datum)
        homie.record(sensor='plant:temperature_probe_' + datum.sensor,
                     value=datum.value,
                     datetime=datum.datetime)
    session.commit()

# ----------------------------------------------------------------------------------------------------------------------

print(sense_probes())
scheduler.add_job(func=sense_probes, trigger="interval", hours=1)

# ----------------------------------------------------------------------------------------------------------------------
import adafruit_dht, board

dht = adafruit_dht.DHT22(board.D17, use_pulseio=True)
#Adafruit_DHT.read(22, 17) #An AM2306 is the same as a DHT22.
time.sleep(0.5)

def dht_sense():
    # dht = DHT(*Adafruit_DHT.read(22, 17))
    dht.measure()
    datum = Measurement(datetime=dt.datetime.now(),
                        value=dht.temperature,
                        sensor='temperature')
    session.add(datum)
    session.commit()
    homie.record(sensor='plant:temperature', value=datum.value, datetime=datum.datetime)
    #
    datum = Measurement(datetime=dt.datetime.now(),
                        value=dht.humidity,
                        sensor='humidity')
    session.add(datum)
    session.commit()
    homie.record(sensor='plant:humidity', value=datum.value, datetime=datum.datetime)
    return datum

# ----------------------------------------------------------------------------------------------------------------------

print(dht_sense())
scheduler.add_job(func=dht_sense, trigger="interval", hours=1)

# ----------------------------------------------------------------------------------------------------------------------
import adafruit_sgp30, busio

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8aae)
# correct humidity
# (humidity, temperature) = Adafruit_DHT.read(22, 17) #An AM2306 is the same as a DHT22.
# if humidity is None or temperature is None:
#     continue
# # convert RH to AH (g/m^3)
# T = temperature + 273.15
# p = 1e5
# rho = 1.225
# es = 611.2 * math.exp(17.67 * (T - 273.15) / (T - 29.65))
# rvs = 0.622 * es / (p - es)
# rv = humidity / 100. * rvs
# qv = rv / (1 + rv)
# AH = qv * rho * 1e3
# sgp30.set_iaq_humidity(AH)

def sgp30_sense():
    # dht = DHT(*Adafruit_DHT.read(22, 4))
    # no humidity correction as it does not seem to work.
    measured_CO2, measured_VOC = sgp30.iaq_measure()
    datum = Measurement(datetime=dt.datetime.now(),
                        value=measured_CO2,
                        sensor='CO2')
    session.add(datum)
    session.commit()
    homie.record(sensor='plant:CO2', value=datum.value, datetime=datum.datetime)
    #
    datum = Measurement(datetime=dt.datetime.now(),
                        value=measured_VOC,
                        sensor='measured_VOC')
    session.add(datum)
    session.commit()
    homie.record(sensor='plant:VOC', value=datum.value, datetime=datum.datetime)
    return datum

# ----------------------------------------------------------------------------------------------------------------------

print(sgp30_sense())
scheduler.add_job(func=sgp30_sense, trigger="interval", hours=1)

# # ---------------------------------------------------------------------------------------------------------------------
# import logging, sys
#
# log = logging.getLogger('apscheduler')
# log.setLevel(logging.ERROR)
# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.DEBUG)
# handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))
# log.addHandler(handler)
# # ----------------------------------------------------------------------------------------------------------------------

# =============================================================================================================================

scheduler.start()
# scheduler.print_jobs()
