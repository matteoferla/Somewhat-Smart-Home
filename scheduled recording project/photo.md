# ----------------------------------------------------------------------------------------------------------------------
# 'picamera': {'name': 'xx', 'rotate': True}

from photologger import Photo
import requests
from PIL import Image


def photograph():
    extension = 'PNG'
    photo = Photo(max_exposures=100,
                  stack=True, 
                  resolution = (1920, 1080), 
                  debug=False)
    if ${sensors['picamera']['rotate']}:
        img = photo.image.transpose(Image.ROTATE_90)
    else:
        img = photo.image
    img.save(open('temp.png', 'wb'), format=extension)
    sensor = "${sensors['picamera']['name']}"
    isodate = dt.datetime.now().isoformat()
    reply = requests.post(f'{homie.base_url}/store', {'key': homie.key,
                                                     'extension': extension,
                                                     'datetime': isodate,
                                                     'sensor': sensor},
                          files={'photo': open('temp.png', 'rb')}
                          )

print(photograph())
scheduler.add_job(func=photograph, trigger="interval", minutes=30)

# ----------------------------------------------------------------------------------------------------------------------
