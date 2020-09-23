from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from flask import Flask
from datetime import datetime
#from cyclones_api import app


DBUSERNAME = 'postgres'
DBHOST = 'postgres'
DBNAME = 'cyclone'
DBPASSWORD = 'cyclone'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%s:%s@%s:5432/%s' % (
    DBUSERNAME, DBPASSWORD, DBHOST, DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@dataclass
class CycloneHistory(db.Model):
    time: datetime
    lat: float
    long: float
    intensity: int

    time = db.Column(db.DateTime, primary_key=True)
    lat = db.Column(db.Float, primary_key=True)
    long = db.Column(db.Float, primary_key=True)
    intensity = db.Column(db.Integer)

    def __repr__(self):
        return '<History %s %s %s %s>' % (self.time, self.lat, self.long, self.intensity)


@dataclass
class CycloneForecast(db.Model):
    hour: int
    lat: float
    long: float
    intensity: int

    hour = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, primary_key=True)
    long = db.Column(db.Float, primary_key=True)
    intensity = db.Column(db.Integer)

    def __repr__(self):
        return '<Forecast %s %s %s %s>' % (self.hour, self.lat, self.long, self.intensity)
