## homesensing

Started from Pyramid SQLite cookiecutter.
Changed CDNs to use BS4, full JQuery and Plotly.

* `homesensing_api.py`: For pis across house to send their data
* `homesensing`: For gateway pi

## Install

Dev setup:

    pip3 install -e .
    alembic -c development.ini revision --autogenerate -m "init"
    alembic -c development.ini upgrade head
    python3 app.py --d
    
Prod setup:


    pip3 install .
    alembic -c production.ini revision --autogenerate -m "init"
    alembic -c production.ini upgrade head
    python3 app.py --d
    
## Database

There are three tables.

* Measurment —each entry is a sensor measurement at a given time
* Photo —each entry is a path to a photo (from a "sensor" (camera) at a given time)
* Details —each entry is the unique details for a sensor
    
## Routes

Webpage is for viewing API for adding.
Adding only works if one has the key.
fail2ban jail need to be configure to jail excessive 404 triggerers.

### Adding data

The file `homesensing/homesensing_api.py` contains a class that can add data to the server.

But the key part is that `/record` route requires the following:

    {'key': '👾👾👾',
    'datetime': dt.datetime.now().isoformat(), # optional.
    'sensor': '👾👾👾',
    'value': '👾👾👾'}

## Text from cookiecutter

The folder was started with a cookiecutter 
and here is the verbose text from that.

- Change directory into your newly created project if not already there. Your
  current directory should be the same as this README.txt file and setup.py.

    cd homesensing

- Create a Python virtual environment, if not already created.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Initialize and upgrade the database using Alembic.

    - Generate your first revision.

        env/bin/alembic -c development.ini revision --autogenerate -m "init"

    - Upgrade to that revision.

        env/bin/alembic -c development.ini upgrade head

- Load default data into the database using a script.

    env/bin/initialize_homesensing_db development.ini

- Run your project's tests.

    env/bin/pytest

- Run your project.

    env/bin/pserve development.ini
