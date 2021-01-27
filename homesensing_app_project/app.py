from waitress import serve
from pyramid.paster import get_app, setup_logging
import os, argparse

# ======================================================================================================================

# check and fill missing environment variables.
# ones with None are optional.
environmental = dict(SECRETCODE='ERROR',
                     SLACK_WEBHOOK=None,
                     LOCAL_LATITUDE=51.746000, # Oxford
                     LOCAL_LONGITUTE=-1.258200 # Oxford
                     )

for ev in environmental:
    if ev in os.environ:
        print(f'Environment variable {ev}: present')
    elif environmental[ev] is None:
        print(f'Environment variable {ev}: skipping')
    else:
        print(f'Environment variable {ev}: defaulting to {environmental[ev]}')
        os.environ[ev] = str(environmental[ev])

# ======================================================================================================================

# custom `app.py` due to os.environs...
parser = argparse.ArgumentParser()
parser.add_argument('--d', action='store_true', help='run in dev mode')
if parser.parse_args().d:
    print('*'*10)
    print('RUNNING IN DEV MODE')
    print('*' * 10)
    configfile = 'development.ini'
else:
    configfile = 'production.ini'

# ======================================================================================================================

setup_logging(configfile)
app = get_app(configfile, 'main') #pyramid.router.Router

# ======================================================================================================================

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000, threads=50)