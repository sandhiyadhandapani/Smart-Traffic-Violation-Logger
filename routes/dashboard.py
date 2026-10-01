from flask import Blueprint, render_template
from sqlalchemy import func

from extensions import db
from models.violation import Violation
from routes.auth import login_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard_home():
    total_violations = db.session.query(Violation).count()
    unpaid_violations = db.session.query(Violation).filter_by(payment_status="Unpaid").count()
    paid_violations = db.session.query(Violation).filter_by(payment_status="Paid").count()
    total_fine_amount = db.session.query(func.sum(Violation.fine_amount)).scalar() or 0

    return render_template(
        "dashboard.html",
        total_violations=total_violations,
        unpaid_violations=unpaid_violations,
        paid_violations=paid_violations,
        total_fine_amount=total_fine_amount,
    )
