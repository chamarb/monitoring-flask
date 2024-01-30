from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EndDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    mac_address = db.Column(db.String(17), nullable=False)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

class IoTDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(255), nullable=False)
    temp = db.Column(db.Float)
    time = db.Column(db.TIMESTAMP)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)














'''from dataclasses import dataclass

@dataclass
class EndDevice:
    name: str
    ip_address: str
    mac_address: str
    longitude: float = None
    latitude: float = None

@dataclass
class IoTDevice:
    mac: str
    temp: float
    datetime: str
    latitude: float
    longitude: float'''









'''from dataclasses import dataclass

@dataclass
class EndDevice:
    name: str
    ip_address: str
    mac_address: str
    longitude: float = None
    latitude: float = None

@dataclass
class IoTDevice:
    mac: str
    temp: float
    datetime: str
    latitude: float
    longitude: float'''

