# ----------------------------------------------------------------------------------------------------------------------

import adafruit_dht, board

dht = adafruit_dht.DHT22(board.D${sensors['DHT22']}, use_pulseio=True)
#Adafruit_DHT.read(22, 17) #An AM2306 is the same as a DHT22.
time.sleep(0.5)

def dht_sense():
    # dht = DHT(*Adafruit_DHT.read(22, 17))
    dht.measure()
    homie.record(sensor='${pi_name}:temperature',
                value=dht.temperature,
                datetime=dt.datetime.now())
    homie.record(sensor='${pi_name}:humidity',
                value=dht.humidity,
                datetime=dt.datetime.now())
    return True

# ----------------------------------------------------------------------------------------------------------------------

print(dht_sense())
scheduler.add_job(func=dht_sense, trigger="interval", hours=1)

# ----------------------------------------------------------------------------------------------------------------------
