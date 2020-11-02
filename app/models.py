from app import db





class Auto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    price = db.Column(db.Integer)
    description = db.Column(db.String(128))
    transmission = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    img_url = db.Column(db.String(128))
    