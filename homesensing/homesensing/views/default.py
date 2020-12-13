from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from ..models import Measurement, Photo, Details
from sqlalchemy.exc import DBAPIError
import pyramid.httpexceptions as exc
import datetime as dt
import os
import logging

log = logging.getLogger(__name__)

from .. import models

@view_defaults(route_name='home')
class DBViews:
    def __init__(self, request):
        self.request = request

    # ========= views  =============================================
    @view_config(renderer='../templates/home.mako')
    def home(self):
        return {'authorised': False}

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
        return {'status': 'success'}

    @view_config(route_name='store', renderer='json')
    def store(self):
        """
        Adds a photo

        :return:
        """
        self.authorise()
        # typology == 'photo':
        path = self.save_photo()
        entry = Photo(datetime=self.get_time('datetime'),
                      sensor=self.get_value('sensor', str),
                      path=path)
        self.request.dbsession.add(entry)  # transaction manager built in. No commit.
        msg = f'Added photo by {entry.sensor} at {entry.datetime} as {entry.path}'
        log.info(msg)
        return {'status': 'success'}

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
        return {'status': 'success'}

    def save_photo(self):
        pass

    @view_config(route_name='read', renderer='json')
    def read(self):
        if 'delta' in self.request.params:
            # delta will be used only if no 'stop'
            delta = self.get_value('delta', float)
        else:
            delta = 5
        start = self.get_time('start', delta=delta)
        stop = self.get_time('stop')
        query_search = self.request \
            .dbsession \
            .query(Measurement) \
            .filter(Measurement.datetime > start) \
            .filter(Measurement.datetime < stop)
        if 'sensor' in self.request.params:
            sensor = self.get_value('sensor', str)
            query_search.filter(Measurement.sensor == sensor)
        else:
            sensor = 'all'
        ## get data
        results = []
        sensors = set()
        for measurement in query_search.all():
            results.append({'datetime': measurement.datetime.isoformat(),
                            'sensor': measurement.sensor,
                            'value': measurement.value})
            sensors.add(measurement.sensor)
        ## sensor details
        query_search = self.request \
            .dbsession \
            .query(Details)
        if sensor != 'all':
            query_search = query_search.filter(Details.sensor.in_(list(sensors)))
        row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
        sensor_details = {row.sensor: row2dict(row) for row in query_search.all()}
        ## return
        log.info(f'serving sensor={sensor} data')
        return {'data': results,
                'start': start.isoformat(),
                'stop': stop.isoformat(),
                'sensor': sensor,
                'sensor_details': sensor_details
                }

    # ========= dependents  =============================================

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

    def authorise(self):
        if 'key' not in self.request.params:
            log.info(f'Error authenticating (no authorisation key)')
            raise exc.HTTPBadRequest('No authorisation key (parameter key)')
        if self.request.params['key'] != os.environ['SECRETCODE']:
            log.info(f'Error authenticating (wrong authorisation key)')
            raise exc.HTTPForbidden(f'Authorisation key {self.request.params["key"]} is wrong')
        else:
            return True

#
# @view_config(route_name='home', renderer='../templates/home.mako')
# def my_view(request):
#     try:
#         query = request.dbsession.query(models.Measurement)
#         one = query.first() #.filter(models.Measurement.name == 'one')
#     except DBAPIError:
#         return Response(db_err_msg, content_type='text/plain', status=500)
#     return {'one': one, 'project': 'homesensing'}

# ==== START =======================
#     if 'start' in request.params:
#         self.start = dt.datetime(*map(int, request.params.get('start').split('-')))
#     else:
#         self.start = dt.datetime.combine((dt.datetime.now() - dt.timedelta(days=5)).date(), dt.time.min)
#     # ==== STOP =======================
#     if 'stop' in request.params:
#         # %Y-%m-%d
#         self.stop = dt.datetime(*map(int, request.params.get('stop').split('-')))
#     else:
#         self.stop = dt.datetime.now()
#
#
#
#
# def serve_data():
#
#     dt, temp, hum, CO2, VOC = get_sensor_data(start=start, stop=stop)
#     CO2 = [c if c < 5e3 else None for c in CO2]
#     # stop and start my be out of bounds.
#     days = {d.date() for d in dt}
#     nights, twilights = get_nighttime(days)
#     ftime, ftemp, fhum = get_forecast(days)
#     shapes = [
#                 {'type': 'rect',
#                 'xref': 'x',
#                 'yref': 'paper',
#                 'x0': dusk,
#                 'y0': 0,
#                 'x1': dawn,
#                 'y1': 1,
#                 'fillcolor': '#191970', #midnightblue
#                 'opacity': 0.4,
#                 'line': {'width': 0},
#                 'layer': 'below'
#                 } for dusk, dawn in nights] +\
#             [
#                 {'type': 'rect',
#                  'xref': 'x',
#                  'yref': 'paper',
#                  'x0': a,
#                  'y0': 0,
#                  'x1': b,
#                  'y1': 1,
#                  'fillcolor': '#6495ed', #cornflowerblue
#                  'opacity': 0.4,
#                  'line': {'width': 0},
#                  'layer': 'below'
#                  } for a, b in twilights]
#     return render_template('temperature.html',
#                            dt=json.dumps([d.strftime('%Y-%m-%d %H:%M:%S') for d in dt]),
#                            temp=json.dumps(temp),
#                            hum=json.dumps(hum),
#                            CO2=json.dumps(CO2),
#                            VOC=json.dumps(VOC),
#                            ftime=json.dumps(ftime),
#                            ftemp=json.dumps(ftemp),
#                            fhum=json.dumps(fhum),
#                            shapes=json.dumps(shapes),
#                            today=str(datetime.now().date()),
#                            yesterday=str((datetime.now() - timedelta(days=1)).date()),
#                            threedaysago=str((datetime.now() - timedelta(days=3)).date()),
#                            aweekago=str((datetime.now() - timedelta(days=7)).date()))
#
#
# db_err_msg = """\
# Pyramid is having a problem using your SQL database.  The problem
# might be caused by one of the following things:
#
# 1.  You may need to initialize your database tables with `alembic`.
#     Check your README.md for descriptions and try to run it.
#
# 2.  Your database server may not be running.  Check that the
#     database server referred to by the "sqlalchemy.url" setting in
#     your "development.ini" file is running.
#
# After you fix the problem, please restart the Pyramid application to
# try it again.
# """
