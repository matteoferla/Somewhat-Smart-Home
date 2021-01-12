import adafruit_dht, board

dht = adafruit_dht.DHT11(board.D${sensors['DHT11']}, use_pulseio=False)
time.sleep(0.5)

def dht_sense():
    if dht.temperature is None:
        return sense()
    homie.record(sensor='LEGO:temperature', value=dht.temperature, datetime=dt.datetime.now())
    homie.record(sensor='LEGO:humidity', value=dht.humidity, datetime=dt.datetime.now())
    return True

# ----------------------------------------------------------------------------------------------------------------------

print(dht_sense())
scheduler.add_job(func=dht_sense, trigger="interval", hours=1)

# ----------------------------------------------------------------------------------------------------------------------
