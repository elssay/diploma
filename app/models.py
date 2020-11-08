from app import db
from datetime import datetime





class Auto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    price = db.Column(db.Integer)
    aprice = db.Column(db.Float)
    description = db.Column(db.String(128))
    transmission = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    astatus = db.Column(db.Boolean)
    img_url = db.Column(db.String(128))
    rented = db.Column(db.DateTime, default=datetime.now)
    end_of_rent = db.Column(db.DateTime, default=datetime.now)
    rented = db.Column(db.DateTime)
    end_of_rent = db.Column(db.DateTime)
    arented = db.Column(db.DateTime)
    aend_of_rent = db.Column(db.DateTime)
    aurented = db.Column(db.DateTime, default=datetime.now)
    auend_of_rent = db.Column(db.DateTime, default=datetime.now)
    auprice = db.Column(db.Float(asdecimal=True))
    autprice = db.Column(db.Float)
    total_price = db.Column(db.Float)
    total_time = db.Column(db.DateTime)
    atotal_time = db.Column(db.Integer)
    rent_count = db.Column(db.Integer)



class Rentlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auto_id = db.Column(db.Integer)
    rented = db.Column(db.DateTime, default=datetime.now)
    end_of_rent = db.Column(db.DateTime, default=datetime.now)
    rentprice = db.Column(db.Float)
