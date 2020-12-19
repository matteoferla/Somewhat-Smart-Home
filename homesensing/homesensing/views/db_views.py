from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from ..models import Measurement, Photo, Details, Sunpath
from sqlalchemy.exc import DBAPIError
import pyramid.httpexceptions as exc
import datetime as dt
import os, re, shutil, time
import logging, time
import uuid
from .authenticate import Authenticator

log = logging.getLogger(__name__)


class DBViews:
    time_debug = False

    def __init__(self, request):
        self.request = request
        self.tick = time.time()

    @property
    def tock(self) -> float:
        return time.time()

    @property
    def time_taken(self) -> float:
        return self.tock - self.tick

    # === views

    @view_config(route_name='status', renderer='json')
    def status(self):
        """
        Is the key correct?

        :return:
        """
        authenticator = Authenticator(self.request)
        if not authenticator.has_key():
            return {'status': 'No key given'}
        elif not authenticator.is_valid():
            time.sleep(30)
            return {'status': 'Wrong key given', 'time_taken': self.time_taken}
        else:
            return {'status': 'Correct key given', 'time_taken': self.time_taken}

    @view_config(route_name='record', renderer='json')
    def record(self):
        """
        Adds a Measurement

        :return:
        """
        self.authorise()
        entry = Measurement(datetime=self.get_time('datetime'),
                            sensor=self.get_value('sensor', str),
                            value=self.get_value('value', float))
        self.request.dbsession.add(entry)  # transaction manager built in. No commit.
        msg = f'Added recording by {entry.sensor} of {entry.value} at {entry.datetime}'
        log.info(msg)
        return {'status': 'success', 'time_taken': self.time_taken}

    @view_config(route_name='store', renderer='json')
    def store(self):
        """
        Adds a photo

        :return:
        """
        self.authorise()
        # typology == 'photo':
        path = self.save_photo()
        if path is None:
            raise exc.HTTPBadRequest('The file did not save.')
        entry = Photo(datetime=self.get_time('datetime'),
                      sensor=self.get_value('sensor', str),
                      path=path)
        self.request.dbsession.add(entry)  # transaction manager built in. No commit.
        msg = f'Added photo by {entry.sensor} at {entry.datetime} as {entry.path}'
        log.info(msg)
        return {'status': 'success', 'time_taken': self.time_taken}

    @view_config(route_name='define', renderer='json')
    def define(self):
        """
        Add Details of sensor name
        Here defaults happen.

        :return:
        """
        entry = Details(sensor=self.get_value('sensor', str),
                        model=self.get_value('model', str),
                        location=self.get_value('location', str),
                        unit=self.get_value('unit', str),
                        graph_color=self.get_value('graph_color', str, '#dcdcdc'),
                        dashed=self.get_value('dashed', bool, False),
                        axis=self.get_value('axis', str, default='hundred')
                        )
        self.request.dbsession.add(entry)  # transaction manager built in. No commit.
        msg = f'Added details for {entry.sensor}'
        log.info(msg)
        return {'status': 'success', 'time_taken': self.time_taken}

    @view_config(route_name='read', renderer='json')
    def read(self):
        start, stop = self.get_boundaries()
        if self.time_debug:
            log.info(f'Prequery. Time taken: {self.time_taken}')
        query_search = self.request \
            .dbsession \
            .query(Measurement) \
            .filter(Measurement.datetime > start)
        if self.time_debug:
            log.info(f'Ori-query Time taken: {self.time_taken}')
        if 'stop' in self.request.params:
            query_search = query_search.filter(Measurement.datetime < stop)
        if 'sensor' in self.request.params:
            sensor = self.get_value('sensor', str)
            query_search.filter(Measurement.sensor == sensor)
        else:
            sensor = 'all'
        # === get data
        if self.time_debug:
            log.info(f'query done: {self.time_taken}')
        results = []
        sensors = set()
        for measurement in query_search.all():
            results.append({'datetime': measurement.datetime.isoformat(),
                            'sensor': measurement.sensor,
                            'value': measurement.value})
            sensors.add(measurement.sensor)

        if self.time_debug:
            log.info(f'Data flipped: {self.time_taken}')
        # === sensor details
        query_search = self.request \
            .dbsession \
            .query(Details)
        if sensor != 'all':
            query_search = query_search.filter(Details.sensor.in_(list(sensors)))
        sensor_details = {row.sensor: self.row2dict(row) for row in query_search.all()}
        if self.time_debug:
            log.info(f'Sensor data: {self.time_taken}')
        # === return
        log.info(f'serving sensor={sensor} data')
        return {'data': results,
                'start': start.isoformat(),
                'stop': stop.isoformat(),
                'sensor': sensor,
                'sensor_details': sensor_details,
                'time_taken': self.time_taken
                }

    @view_config(route_name='show', renderer='json')
    def show(self):
        # === Photos
        start, stop = self.get_boundaries()
        query_search = self.request \
            .dbsession \
            .query(Photo) \
            .filter(Photo.datetime > start)
        if 'stop' in self.request.params:
            query_search = query_search.filter(Measurement.datetime < stop)
        photos = [self.row2dict(row) for row in query_search.all()]
        log.info(f'Photos: {self.time_taken}')
        # === return
        return {'start': start.isoformat(),
                'stop': stop.isoformat(),
                'photos': photos,
                'time_taken': self.time_taken
                }

    @view_config(route_name='night', renderer='json')
    def night(self):
        start, stop = self.get_boundaries()
        # get all dates (not datetimes) between.
        dates = []
        start = start.date()
        stop = stop.date()
        new = start
        while new <= stop:
            dates.append(new)
            new += dt.timedelta(days=1)
        # get data
        nights, twilights = self.get_nighttime(dates)
        return {'nights': nights, 'twilights': twilights}

    # ========= dependents  =============================================

    def get_boundaries(self):
        if 'delta' in self.request.params:
            # delta will be used only if no 'stop'
            delta = self.get_value('delta', float)
        else:
            delta = 5
        start = self.get_time('start', delta=delta)
        stop = self.get_time('stop')
        return start, stop

    def get_value(self, key: str, value_type: type = str, default=None):
        if key in self.request.params:
            try:
                if value_type == bool:
                    if self.request.params[key] in ('true', 'True', 1):
                        return True
                    else:
                        return False
                else:
                    return value_type(self.request.params[key])
            except Exception:
                msg = f'The parameter {key} is not of type {value_type.__name__}.'
                log.info(f'Request error: {msg}')
                raise exc.HTTPBadRequest(msg)
        elif default is not None:
            return default
        else:
            msg = f'The parameter {key} is missing.'
            log.info(f'Request error: {msg}')
            raise exc.HTTPBadRequest(msg)

    def get_time(self, key: str, delta: float = 0) -> dt.datetime:
        if key in self.request.params:
            return dt.datetime.fromisoformat(self.request.params[key])
        elif delta == 0:
            return dt.datetime.now()
        else:
            return dt.datetime.now() - dt.timedelta(days=delta)

    def round_date(self, datetime: dt.datetime) -> dt.datetime:
        """
        Rounds the datetime to midnight
        """
        return dt.datetime.combine(datetime.date(), dt.time.min)

    def save_photo(self):
        sensor = re.sub('[^\w\.\_\-]', '_', self.get_value('sensor', str))
        extension = self.get_value('extension', str).replace('.', '')
        parent = os.path.split(__file__)[0]  # views
        root = os.path.split(parent)[0]
        folder = os.path.join(root, 'static/photos', sensor)
        if not os.path.exists(folder):
            log.info(f'making folder {folder}')
            os.mkdir(folder)
        filename = str(uuid.uuid4()) + '.' + extension
        with open(os.path.join(folder, filename), 'wb') as w:
            i = self.request.POST['photo'].file
            shutil.copyfileobj(i, w)
        return os.path.join('static', 'photos', sensor, filename)

    def authorise(self):
        Authenticator(self.request).assert_valid()

    def row2dict(self, r):
        return {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}


    def fetch_sunpath(self, date: dt.date):
        standard = '%Y-%m-%dT%H:%M:%S+00:00'
        lat = float(os.environ['LOCAL_LATITUDE']) #51.746000
        lon = float(os.environ['LOCAL_LONGITUTE']) #-1.258200
        url = f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}'
        data = self.requests.get(f'{url}&date={date.year}-{date.month}-{date.day}&formatted=0').json()['results']
        sun = Sunpath(date=date,
                    dawn=dt.datetime.strptime(data['civil_twilight_begin'], standard),
                    sunrise=dt.datetime.strptime(data['sunrise'], standard),
                    sunset=dt.datetime.strptime(data['sunset'], standard),
                    dusk=dt.datetime.strptime(data['civil_twilight_end'], standard)
                    )
        self.request.dbsession.add(sun)

    def get_nighttime(self, dates):
        # dates is a list of dates, not datetimes
        if len(dates):
            exc.HTTPBadRequest('No days')
        for date in dates:
            if self.request.dbsession.query(Sunpath).filter(Sunpath.date == date).first() is None:
                self.fetch_sunpath(date)
        previous = None
        nights = []
        twilights = []
        day = None
        for day in self.request.dbsession.query(Sunpath).filter(Sunpath.date >= min(dates)) \
                .filter(Sunpath.date <= max(dates)) \
                .order_by(Sunpath.date).all():
            if previous is None:
                date = day.date
                previous = datetime.combine(date, dtime.min)
            nights.append([previous.strftime(standard), day.dawn.strftime(standard)])
            previous = day.dusk
            twilights.append([day.dawn.strftime(standard), day.sunrise.strftime(standard)])
            twilights.append([day.sunset.strftime(standard), day.dusk.strftime(standard)])
        if not day is None:
            d = day.date
            ender = datetime.combine(d, dtime.max)
            nights.append([previous.strftime(standard), ender.strftime(standard)])
        else:
            log.critical('NO DATA! Is this the first run?')
        return nights, twilights


