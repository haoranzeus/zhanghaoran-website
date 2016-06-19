from . import db

class Entries(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    #comment = db.Column(db.Text)
