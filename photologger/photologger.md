# Photologger

There are three parts.

* camera (with various corrections)
* Flask server
* scheduler

## Camera

    from photologger import Photo, Flash
    
`Flash` has a class attribute `light`. By default it is set to GPIO21.

    import digitalio
    
    Flash.light = digitalio.DigitalInOut(board.D4)
    Flash.light.direction = digitalio.Direction.OUTPUT

`Camera` has several options.

    photo = Photo(stack=True, max_exposures=100, debug=True)
    
There are a few attributes of note:

* `photo.exposures`: number of exposures stacked
* `photo.image`: PIL object
* `photo.data`: numpy array

There are two processing steps that go on:

1. Image is scaled so each channel is within 0 and 255 or 30% max, whichever is lowest.
2. Image is histogram stretched

Other methods are `save` and `rotate`.

## Schedule

    from photologger import Schedule
    
    Schedule(interval_minutes=10, background=False)

## App

    from photologger import create_app, Photo, Schedule
    
    def run(folder='/home/pi/photos', interval_minutes=10):
        Photo.save_path = folder
        schedule = Schedule(interval_minutes)
        app = create_app(folder)
        app.run(host='0.0.0.0', port=5000)