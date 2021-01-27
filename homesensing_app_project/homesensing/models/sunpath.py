import os
import sqlalchemy as db
from .meta import Base


class Sunpath(Base):
    """
    The table containing the sun details.
    """
    __tablename__ = 'sunpath'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    dawn = db.Column(db.DateTime(timezone=True), unique=True, nullable=False)
    sunrise = db.Column(db.DateTime(timezone=True), unique=True, nullable=False)
    sunset = db.Column(db.DateTime(timezone=True), unique=True, nullable=False)
    dusk = db.Column(db.DateTime(timezone=True), unique=True, nullable=False)
