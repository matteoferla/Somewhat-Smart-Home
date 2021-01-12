# Bins go out on alternating Thursday evenings

from functools import partial

def binmaster(pin, weekday=3):
        while datetime.now().weekday() == weekday:
            with digitalio.DigitalInOut(pin) as led:
                led.direction = digitalio.Direction.OUTPUT
                led.value = True
                time.sleep(0.5)
                led.value = False
                time.sleep(0.5)

bluebinmaster = partial(binmaster, pin=board.D24)
greenbinmaster = partial(binmaster, pin=board.D23)

# next green
greenday = datetime.fromisoformat('2020-12-03 16:30:00')
while greenday < datetime.now():
    greenday += timedelta(days=7)

# next green
blueday = datetime.fromisoformat('2020-12-10 16:30:00')
while blueday < datetime.now():
    blueday += timedelta(days=7)

scheduler.add_job(greenbinmaster, 'interval', weeks=2, start_date=greenday.isoformat())
scheduler.add_job(bluebinmaster, 'interval', weeks=2, start_date=blueday.isoformat())