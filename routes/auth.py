from functools import wraps

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

auth_bp = Blueprint("auth", __name__)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        current_app.config.setdefault("SECRET_KEY", "smart-traffic-logger-demo")

        if "officer_logged_in" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped_view


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    current_app.config.setdefault("SECRET_KEY", "smart-traffic-logger-demo")

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == "officer" and password == "traffic123":
            session["officer_logged_in"] = True
            session["officer_username"] = username
            flash("Login successful.", "success")
            return redirect(url_for("dashboard.dashboard_home"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    current_app.config.setdefault("SECRET_KEY", "smart-traffic-logger-demo")

    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
