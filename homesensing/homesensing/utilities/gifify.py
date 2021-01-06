import os
from PIL import Image, ImageFont, ImageDraw
import imageio
import pygifsicle # requires gifsicle

folder = os.path.split(__file__)[0]
parent = os.path.split(folder)[0]
static = os.path.join(parent, 'static')

def gifify(sensor_forename, photo_entries):
    size = 1080 / 2, 1920 / 2  # x/5 each
    images = []
    font = ImageFont.truetype("Vera.ttf", 32)
    for entry in photo_entries:
        path = os.path.join(static, entry['path'])
        if not os.path.exists(path):  # image removed (dick pic photobomb)
            continue
        im = Image.open(path)
        draw = ImageDraw.Draw(im)
        draw.text((0, 0), entry['datetime'], font=font, fill='cyan')
        im.thumbnail(size, Image.ANTIALIAS)
        images.append(im)
    imageio.mimsave('test.gif', images, fps=5)
    final_filename = os.path.join(static, f'{sensor_forename}.gif')
    pygifsicle.optimize('test.gif', final_filename)
    return final_filename