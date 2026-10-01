from datetime import datetime
from pathlib import Path

import qrcode
from flask import Blueprint, flash, redirect, render_template, request, url_for

from extensions import db
from models.violation import Violation
from routes.auth import login_required


violations_bp = Blueprint("violations", __name__)


def generate_qr_code_for_violation(violation):
    qr_dir = Path(__file__).resolve().parents[1] / "static" / "qr_codes"
    qr_dir.mkdir(parents=True, exist_ok=True)

    # Mobile-accessible URL using the laptop's Wi-Fi IP address
    qr_url = f"http://192.168.31.237:5000/status/{violation.id}"

    qr_file = qr_dir / f"violation_{violation.id}.png"

    qr_image = qrcode.make(qr_url)
    qr_image.save(qr_file)

    return f"qr_codes/violation_{violation.id}.png"


@violations_bp.route("/violations/add", methods=["GET", "POST"])
@login_required
def add_violation():
    if request.method == "POST":
        vehicle_number = request.form.get("vehicle_number", "").strip()
        violation_type = request.form.get("violation_type", "").strip()
        location = request.form.get("location", "").strip()
        date_value = request.form.get("date", "")
        fine_amount_value = request.form.get("fine_amount", "").strip()

        if not all([
            vehicle_number,
            violation_type,
            location,
            date_value,
            fine_amount_value
        ]):
            flash("Please fill in all required fields.", "danger")
            return render_template("add_violation.html")

        try:
            violation_date = datetime.strptime(
                date_value,
                "%Y-%m-%d"
            ).date()

            fine_amount = float(fine_amount_value)

        except ValueError:
            flash("Please enter a valid date and fine amount.", "danger")
            return render_template("add_violation.html")

        new_violation = Violation(
            vehicle_number=vehicle_number,
            violation_type=violation_type,
            location=location,
            date=violation_date,
            fine_amount=fine_amount,
            payment_status="Unpaid",
        )

        db.session.add(new_violation)
        db.session.commit()

        try:
            generate_qr_code_for_violation(new_violation)

        except Exception as exc:
            flash(
                f"Violation saved successfully, but QR generation failed: {exc}",
                "warning"
            )

        else:
            flash("Violation added successfully.", "success")

        return redirect(url_for("violations.history"))

    return render_template("add_violation.html")


@violations_bp.route("/violations/history")
@login_required
def history():
    query = Violation.query

    vehicle_number = request.args.get(
        "vehicle_number",
        ""
    ).strip()

    violation_type = request.args.get(
        "violation_type",
        ""
    ).strip()

    payment_status = request.args.get(
        "payment_status",
        ""
    ).strip()

    date_value = request.args.get(
        "date",
        ""
    ).strip()

    if vehicle_number:
        query = query.filter(
            Violation.vehicle_number.ilike(
                f"%{vehicle_number}%"
            )
        )

    if violation_type:
        query = query.filter(
            Violation.violation_type.ilike(
                f"%{violation_type}%"
            )
        )

    if payment_status:
        query = query.filter(
            Violation.payment_status == payment_status
        )

    if date_value:
        query = query.filter(
            Violation.date == date_value
        )

    violations = query.order_by(
        Violation.date.desc(),
        Violation.id.desc()
    ).all()

    return render_template(
        "history.html",
        violations=violations,
        vehicle_number=vehicle_number,
        violation_type=violation_type,
        payment_status=payment_status,
        date_value=date_value,
    )


@violations_bp.route(
    "/violations/<int:violation_id>/paid",
    methods=["POST"]
)
@login_required
def mark_paid(violation_id):
    violation = Violation.query.get_or_404(violation_id)

    violation.payment_status = "Paid"

    db.session.commit()

    flash("Violation marked as paid.", "success")

    return redirect(
        url_for(
            "violations.view_violation",
            violation_id=violation.id
        )
    )


@violations_bp.route("/violations/<int:violation_id>")
@login_required
def view_violation(violation_id):
    violation = Violation.query.get_or_404(violation_id)

    qr_image_path = None

    qr_file = (
        Path(__file__).resolve().parents[1]
        / "static"
        / "qr_codes"
        / f"violation_{violation.id}.png"
    )

    if qr_file.exists():
        qr_image_path = (
            f"qr_codes/violation_{violation.id}.png"
        )

    return render_template(
        "challan.html",
        violation=violation,
        qr_image_path=qr_image_path
    )