import sqlalchemy as db

from .meta import Base


class Measurement(Base): # db.Model
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime(timezone=True), nullable=False)
    sensor = db.Column(db.Text)
    value = db.Column(db.Float, nullable=False)


#db.Index('my_index', Measurement.name, unique=True, mysql_length=255)
