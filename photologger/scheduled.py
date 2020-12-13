from warnings import warn

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from signal import signal, SIGINT
from .slack import slack
from threading import Lock
from .camera import Photo
import logging

log = logging.getLogger(__name__)

class Schedule:
    lock = Lock() #stop interferring with each other.

    def __init__(self, interval_minutes=10):
        signal(SIGINT, self.death_handler)
        ## Scheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=self.photo, trigger="interval", minutes=interval_minutes)
        scheduler.start()

    def photo(self):
        log.debug('Taking photo.')
        with self.lock:
            photo = Photo()
            log.debug(f'Took photo via merge of {photo.exposures} stills')

    def death_handler(self, signal_received, frame):
        try:
            if Photo._camera and not Photo._camera.closed:
                Photo._camera.close()
        except:
            pass
        if self.lock.locked(): self.lock.release()
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        slack('Shutting down gracefully')
        exit(0)

