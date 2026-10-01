from pathlib import Path

from flask import Blueprint, render_template

from models.violation import Violation

public_bp = Blueprint("public", __name__)


def get_qr_image_path(violation_id):
    qr_file = Path(__file__).resolve().parents[1] / "static" / "qr_codes" / f"violation_{violation_id}.png"
    if qr_file.exists():
        return f"qr_codes/violation_{violation_id}.png"
    return None


@public_bp.route("/status/<int:violation_id>")
def violation_status(violation_id):
    violation = Violation.query.get(violation_id)

    if violation is None:
        return render_template("status.html", violation=None, qr_image_path=None), 404

    return render_template(
        "status.html",
        violation=violation,
        qr_image_path=get_qr_image_path(violation_id),
    )
