"""
Take photos and serve them.
"""

from .get_app import create_app
from .camera import Photo
from .flash import Flash
from .scheduled import Schedule

def run(folder='/home/pi/photos', interval_minutes=10):
    Photo.save_path = folder
    schedule = Schedule(interval_minutes)
    app = create_app(folder)
    app.run(host='0.0.0.0', port=5000)


