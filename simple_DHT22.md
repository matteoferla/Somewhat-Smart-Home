## DHT22 server

This is just a simple Flask server that logs and servers a DHT22.

## DB

This is a close variant from https://github.com/matteoferla/Raspberry-Pi-irrigator/blob/master/models.py

    from datetime import datetime
    import sqlalchemy as db
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    import Adafruit_DHT
    from collections import namedtuple
    
    DHT = namedtuple('DHT', ['humidity', 'temperature'])
    
    Base = declarative_base()
    
    class Measurement(Base):
        """
        The table containing the measurements.
        """
        __tablename__ = 'measurements'
        id = db.Column(db.Integer, primary_key=True)
        datetime = db.Column(db.DateTime(timezone=True), unique=True, nullable=False)
        temperature = db.Column(db.Float, unique=False, nullable=False)
        humidity = db.Column(db.Float, unique=False, nullable=False)
    
    #### Lastly ####
    engine = db.create_engine('sqlite:///temperature.sqlite')
    Session = sessionmaker()
    session = Session(bind=engine)
    Base.metadata.create_all(engine)
    
## Scheduler

Measurement method

    def old_sense():
        dht = DHT(*Adafruit_DHT.read(22, 4))
        if dht.temperature is None:
            return sense()
        datum = Measurement(datetime=datetime.now(),
                            temperature=dht.temperature,
                            humidity=dht.humidity)
        
        session.add(datum)
        session.commit()

Scheduler:

    from apscheduler.schedulers.background import BackgroundScheduler
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=sense, trigger="interval", hours=1)

## Flask

    from flask import Flask, render_template, request
    
    app = Flask(__name__)
    
    
    def format_results(query):
        clean = lambda v: v.isoformat() if isinstance(v, datetime)
        to_dict = lambda row: {k: clean(v) else v
        for k, v in row.__dict__.items() if k != '_sa_instance_state'}
        return [to_dict for row in results]
    
    
    def read_data(start, stop):
        return format_results(session.query(Measurement) \
                              .filter(Measurement.datetime > start) \
                              .filter(Measurement.datetime < stop) \
                              .all()
                              )
    
    
    @app.route('/')
    def serve_data():
        if 'stop' in request.args:
            # %Y-%m-%d
            stop = datetime(*map(int, request.args.get('stop').split('-')))
        else:
            stop = datetime.now()
        if 'start' in request.args:
            start = datetime(*map(int, request.args.get('start').split('-')))
        else:
            start = datetime.combine((datetime.now() - timedelta(days=7)).date(), dtime.min)
        dt, temp, hum = read_data(start=start, stop=stop)
    
    
    app.run('0.0.0.0', 5000)


    