import os
from PIL import Image, ImageFont, ImageDraw
import imageio
import pygifsicle # requires gifsicle
import logging

log = logging.getLogger(__name__)

folder = os.path.split(__file__)[0]
root_folder = os.path.split(folder)[0]

def gifify(sensor_forename, photo_entries):
    size = 1080 / 2, 1920 / 2  # x/5 each
    images = []
    font = ImageFont.truetype("Vera.ttf", 32)
    for entry in photo_entries:
        path = os.path.join(root_folder, entry['path'])
        print(path)
        if not os.path.exists(path):  # image removed (dick pic photobomb)
            log.warning(f'Cannot find file {entry["path"]}')
            continue
        try:
            im = Image.open(path)
        except Exception as error:
            log.warning(f'Cannot read file {entry["path"]}')
            continue
        draw = ImageDraw.Draw(im)
        draw.text((0, 0), entry['datetime'], font=font, fill='cyan')
        im.thumbnail(size, Image.ANTIALIAS)
        images.append(im)
    first_filename = os.path.join(root_folder, 'static', 'test.gif')
    imageio.mimsave(first_filename, images, fps=5)
    final_filename = os.path.join(root_folder, 'static', f'{sensor_forename}.gif')
    pygifsicle.optimize(first_filename, final_filename)
    return final_filename