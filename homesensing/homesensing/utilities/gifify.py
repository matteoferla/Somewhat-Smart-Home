import os
from PIL import Image, ImageFont, ImageDraw
import imageio
import pygifsicle # requires gifsicle
import logging

log = logging.getLogger(__name__)

folder = os.path.split(__file__)[0]
parent = os.path.split(folder)[0]
target_folder = os.path.join(parent, 'static')

def gifify(sensor_forename, photo_entries):
    size = 1080 / 2, 1920 / 2  # x/5 each
    images = []
    font = ImageFont.truetype("Vera.ttf", 32)
    for entry in photo_entries:
        path = os.path.join(target_folder, entry['path'])
        print(path)
        if not os.path.exists(path):  # image removed (dick pic photobomb)
            log.warning(f'Cannot find file {entry["path"]}')
            continue
        im = Image.open(path)
        draw = ImageDraw.Draw(im)
        draw.text((0, 0), entry['datetime'], font=font, fill='cyan')
        im.thumbnail(size, Image.ANTIALIAS)
        images.append(im)
    first_filename = os.path.join(target_folder, 'test.gif')
    imageio.mimsave(first_filename, images, fps=5)
    final_filename = os.path.join(target_folder, f'{sensor_forename}.gif')
    pygifsicle.optimize(first_filename, final_filename)
    return final_filename