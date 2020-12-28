## DS18S20 Probe
# ----------------------------------------------------------------------------------------------------------------------

# pip install w1thermsensor
# https://github.com/matteoferla/Raspberry-Pi-irrigator/blob/master/models.py

# ----------------------------------------------------------------------------------------------------------------------

import time
from w1thermsensor import W1ThermSensor
time.sleep(1)

# ----------------------------------------------------------------------------------------------------------------------

def sense_probes():
    for sensor in W1ThermSensor.get_available_sensors():
        homie.record(sensor='${pi_name}:temperature_probe_' + sensor.id,
                     value=sensor.get_temperature(),
                     datetime=dt.datetime.now())
    return True

# ----------------------------------------------------------------------------------------------------------------------

print(sense_probes())
scheduler.add_job(func=sense_probes, trigger="interval", hours=1)

# ----------------------------------------------------------------------------------------------------------------------
