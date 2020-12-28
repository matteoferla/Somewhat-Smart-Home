def core():
    with open('/sys/class/thermal/thermal_zone0/temp') as core:
        v = int(core.read().strip()) / 1e3
        homie.record(sensor='homeserver:CPU_temperature', value=v, datetime=dt.datetime.now())
        return v

# -----------------------------------------------------------------------------------------------------------------------------

print(core())
scheduler.add_job(func=core, trigger="interval", hours=1)