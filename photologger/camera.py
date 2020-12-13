import time
from picamera import PiCamera
from PIL import Image
from io import BytesIO
import numpy as np
from datetime import datetime
import os

from .flash import Flash

###################################################

class Photo:
    _camera = None
    save_path='' # 'static','plant_photos/'
    # see also a SIGINT death safeguard.
    # it is this or the gc ...

    def __init__(self, warmup=5, mode='strip'):
        self.exposures = 0
        with PiCamera() as self.camera:
            self.data = np.zeros((self.camera.resolution[1], self.camera.resolution[0], 3)) #480, 720
            self.__class__._camera = self.camera # death prevention..
            self.camera.start_preview()
            time.sleep(warmup)
            with Flash():
                while np.max(self.data) < 255 and self.exposures < 10:
                    self.data = np.add(self.data, np.asarray(self.capture()))
                    self.exposures += 1
        self.__class__._camera = None
        self.data = self.per_channel(self.scale, self.data)
        self.data = self.per_channel(self.histogram_stretch, self.data)
        self.image = Image.fromarray(self.data)
        self.save()

    @staticmethod
    def per_channel(fx, t):
        a = [fx(t[:, :, c]) for c in range(3)]
        return np.stack(a, axis=-1)

    @staticmethod
    def scale(matrix: np.ndarray, interval=(0, 255)) -> np.ndarray:
        minima = np.min(matrix)
        maxima = np.max(matrix)
        scaled = (matrix - minima) / (maxima - minima) * interval[1] + interval[0]
        return scaled

    @staticmethod
    def histogram_stretch(t: np.ndarray) -> np.ndarray:
        hist, bins = np.histogram(t.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_normalized = cdf * hist.max() / cdf.max()
        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0)
        return cdf[t.astype('uint8')].astype('uint8')

    def capture(self) -> Image:
        stream = BytesIO()
        self.camera.capture(stream, format='jpeg')
        stream.seek(0)
        im = Image.open(stream)
        return im

    def rotate(self) -> Image:
        # Image
        return self.image.transpose(Image.ROTATE_180)

    def save(self):
        self.image.save(os.path.join(self.save_path, datetime.now().isoformat(timespec='seconds')+'.jpg'),
                        optimize=True,
                        quality=75)
