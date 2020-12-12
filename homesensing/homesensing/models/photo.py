import sqlalchemy as db

from .meta import Base

class Photo(Base): # db.Model
    __tablename__ = 'photography'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime(timezone=True), nullable=False)
    sensor = db.Column(db.Text)
    path = db.Column(db.Text)