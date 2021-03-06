import time
from picamera import PiCamera
PiCamera.CAPTURE_TIMEOUT = 1200  # twenty minutes

from PIL import Image
from io import BytesIO
import numpy as np
from datetime import datetime
import os


###################################################

class Photo:
    _camera = None
    save_path = ''  # 'static','plant_photos/'

    # see also a SIGINT death safeguard.
    # it is this or the gc ...

    def __init__(self,
                 warmup: int = 5,
                 stack=True,
                 max_exposures: int = 20,
                 debug=False,
                 resolution=None,
                 correct=True,
                 autosave=False):
        self.exposures = 0
        self.debug = debug
        self.stack = stack
        self.max_exposures = max_exposures
        with PiCamera(led_pin=None) as self.camera:
            if resolution is not None:
                self.camera.resolution = resolution
            self.data = np.zeros((self.camera.resolution[1], self.camera.resolution[0], 3))  # 480, 720
            self.__class__._camera = self.camera  # death prevention..
            self.camera.start_preview()
            time.sleep(warmup)
            # while np.max(self.data) < 255 and self.exposures < 10:
            while True:
                self.data = np.add(self.data, np.asarray(self.capture()))
                self.exposures += 1
                if self.debug:
                    channel_flat = self.data.reshape((self.data.shape[0] * self.data.shape[1], 3))
                    print(f'Per channel max intensities from exposure stack of {self.exposures}')
                    print(np.max(channel_flat, axis=0))
                    print(f'Per channel medians  intensities from exposure stack of {self.exposures}')
                    print(np.median(channel_flat, axis=0))
                median = np.median(self.data)
                if not self.stack:
                    break
                elif self.exposures == 1 and median > 100:
                    # don't stack for no reason.
                    break
                elif self.exposures == 1:
                    self.camera.sensor_mode = 3
                    # self.iso = 800
                    self.camera.shutter_speed = self.camera.exposure_speed * int(255 / np.max(self.data))
                    if self.debug:
                        print(f'Setting shutter speed to {self.camera.shutter_speed} '+ \
                              f'(previous exposure: {self.camera.exposure_speed}'+ \
                              f' times {int(255 / np.max(self.data))}')
                elif median > 120:
                    break
                elif self.exposures >= self.max_exposures:
                    break
                else:
                    pass  # new exposure
        self.__class__._camera = None
        if correct:
            self.data = self.per_channel(self.scale, self.data)
            self.data = self.per_channel(self.histogram_stretch, self.data)
        else:
            self.data = self.data.astype('uint8')
        self.image = Image.fromarray(self.data)
        if autosave:
            self.save()

    @staticmethod
    def per_channel(fx, t):
        a = [fx(t[:, :, c]) for c in range(3)]
        return np.stack(a, axis=-1)

    @staticmethod
    def scale(matrix: np.ndarray, interval=(0, 255)) -> np.ndarray:
        minima = np.min(matrix)
        maxima = np.max(matrix)
        lower_bound = interval[0]
        higher_bound = np.min([interval[1], np.max(matrix) * 1.3])
        scaled = (matrix - minima) / (maxima - minima) * higher_bound + lower_bound
        return scaled

    @staticmethod
    def histogram_stretch(t: np.ndarray) -> np.ndarray:
        hist, bins = np.histogram(t.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_normalized = cdf * hist.max() / cdf.max()
        cdf_m = np.ma.masked_equal(cdf, 0)
        # don't stretch the max more than 30% or it gets pixellated.
        # note that this may have been scaled anyway beforehand.
        maximum = np.min([255, np.max(t) * 1.3])
        cdf_m = (cdf_m - cdf_m.min()) * maximum / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0)
        return cdf[t.astype('uint8')].astype('uint8')

    def capture(self) -> Image:
        stream = BytesIO()
        # flash is not working?
        #with Flash() as flash:  # this should be using led_pin!
        self.camera.capture(stream, format='jpeg')
        stream.seek(0)
        im = Image.open(stream)
        return im

    def rotate(self) -> Image:
        """
        This just does self.image.transpose(Image.ROTATE_180)
        as is here to remind me of the transpose command.

        :return:
        """
        # Image
        return self.image.transpose(Image.ROTATE_180)

    def save(self, filename=None):
        if filename is None:
            filename = os.path.join(self.save_path, datetime.now().isoformat(timespec='seconds') + '.jpg')
        if self.debug:
            print(f'Saving as {filename}')
        self.image.save(filename,
                        optimize=True,
                        quality=75)
