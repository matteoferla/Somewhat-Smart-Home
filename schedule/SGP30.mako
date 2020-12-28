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
    homie.record(sensor='plant:CO2', value=measured_CO2, datetime=dt.datetime.now())
    homie.record(sensor='plant:VOC', value=measured_VOC, datetime=dt.datetime.now())
    return True

# ----------------------------------------------------------------------------------------------------------------------

print(sgp30_sense())
scheduler.add_job(func=sgp30_sense, trigger="interval", hours=1)

# ----------------------------------------------------------------------------------------------------------------------
