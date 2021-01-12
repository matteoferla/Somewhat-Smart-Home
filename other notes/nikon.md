## Nikon

> Have you plugged in the micro-USB on both sides?!
> Remember to set mode to M and lens to M on the camera.

Controlling the Nikon DSLR with a Raspberry Pi

    sudo apt-get install python3-gphoto2
    
In Python

    import logging
    logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)

    
    import gphoto2 as gp
    callback_obj = gp.check_result(gp.use_python_logging())
    camera = gp.Camera()
    camera.init()
    
Pointless details

    print(camera.get_summary())
    
Take photo

    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
    # save locally
    target = os.path.join('/tmp', file_path.name)
    
Check

    from IPython.display import display, Image
    
    Image(target)
    
Lastly

    camera.exit()