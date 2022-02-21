from webapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    booking = db.relationship('Booking', backref='guest')

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"

class Bungalow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True ,nullable=False)
    content = db.Column(db.Text, nullable=False)
    bungalow_type = db.Column(db.Integer, nullable=False)
    weekprice = db.Column(db.Integer, nullable=False)
    booking = db.relationship('Booking', backref='bungalow')

    def __repr__(self):
        return f"Bungalow('{self.name}', '{self.bungalow_type}', '{self.weekprice}')"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bungalow_id = db.Column(db.Integer, db.ForeignKey('bungalow.id'), nullable=False)
    week = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Booking('{self.guest_id}', '{self.bungalow_id}', '{self.week}')"