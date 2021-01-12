# ======================================================================================================================
# Code from ${pi_description}
# IP: ${ip}
# shortname: "${pi_name}"
# ----------------------------------------------------------------------------------------------------------------------

from homesensing_api import HomieAPI

homie = HomieAPI(base_url='http://${gateway}:8000', key='${key}')

% if is_background:
    from apscheduler.schedulers.background import BackgroundScheduler as Scheduler
% else:
    from apscheduler.schedulers.blocking import BlockingScheduler as Scheduler
% endif
scheduler = Scheduler()

import datetime as dt



# ======================================================================================================================
% if 'bindicator' in sensors:
    <%inherit file="bindicator.mako"/>
% endif

% if 'DS18S20' in sensors:
    <%inherit file="DS18S20.mako"/>
% endif

% if 'DHT22' in sensors:
    # sensors['DHT22'] is the GPIO int
    <%inherit file="DHT22.mako"/>
% endif

% if 'DHT11' in sensors:
    # sensors['DHT22'] is the GPIO int
    <%inherit file="DHT22.mako"/>
% endif

% if 'SGP30' in sensors:
    # fix it manually!
    <%inherit file="SGP30.mako"/>
% endif

% if 'core' in sensors:
    # assumes Raspian
    <%inherit file="core.mako"/>
% endif

# ======================================================================================================================

scheduler.start()
# scheduler.print_jobs()
