from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from ..models import Measurement, Photo, Details, Sunpath
from sqlalchemy.exc import DBAPIError
import pyramid.httpexceptions as exc
import datetime as dt
import os, re, shutil
import logging, time
import uuid

log = logging.getLogger(__name__)


# ========= views  =============================================
@view_config(route_name='home', renderer='../templates/home.mako')
def home(request):
    return {'authorised': False}