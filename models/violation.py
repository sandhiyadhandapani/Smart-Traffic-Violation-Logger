from extensions import db


class Violation(db.Model):
    __tablename__ = "violations"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(50), nullable=False)
    violation_type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    fine_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(
        db.String(20),
        nullable=False,
        default="Unpaid"
    )
