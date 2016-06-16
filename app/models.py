from . import db

class Role(db.Model):
    __tablename__ = "enteries"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, nullable=False)
    text = db.Column(db.Test, nullable=False)
