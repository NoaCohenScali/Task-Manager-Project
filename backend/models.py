from app import db

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donator_id = db.Column(db.Integer, db.ForeignKey('donator.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    sum = db.Column(db.Double, nullable=False)
    form_of_payment = db.Column(db.String(50), nullable=False)
    num_of_payment = db.Column(db.Integer, nullable=False)


class Donator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(300), nullable=False)
    address = db.Column(db.String(10), nullable=False)
    donations = db.relationship('Donation', backref='donator', lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "donations": self.donations
        } 