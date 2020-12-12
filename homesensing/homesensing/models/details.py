import sqlalchemy as db

from .meta import Base

class Details(Base): # db.Model
    __tablename__ = 'details'
    id = db.Column(db.Integer, primary_key=True)
    sensor = db.Column(db.Text, unique = True)
    location = db.Column(db.Text)
    model = db.Column(db.Text)
    unit = db.Column(db.Text)
    graph_color = db.Column(db.Text) # gainsboro say
    dashed = db.Column(db.Boolean(name='type_ck')) # external sources
    axis = db.Column(db.Text) #'hundred' axis = xaxis1