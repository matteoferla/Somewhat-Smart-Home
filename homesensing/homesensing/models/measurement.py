import sqlalchemy as db

from .meta import Base

class Measurement(Base): # db.Model
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime(timezone=True), nullable=False)
    #datetime = db.Column(db.Text)
    sensor = db.Column(db.Text)
    value = db.Column(db.Float, nullable=False)

class FauxDateMeasurement: #(Measurement):
    """
    The parsing of datetime is too slow. text for the win. This is the original test.
    """
    __tablename__ = 'measurements'
    __table_args__ = {'extend_existing': True}
    datetime = db.Column(db.Text)

#db.Index('my_index', Measurement.name, unique=True, mysql_length=255)
