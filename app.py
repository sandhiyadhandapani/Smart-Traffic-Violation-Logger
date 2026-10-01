from pathlib import Path

from flask import Flask

from extensions import db

BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATABASE_DIR / "traffic.db"


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    app.config["SECRET_KEY"] = "traffic-pulse-demo-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from models.violation import Violation

    try:
        from routes.auth import auth_bp
        app.register_blueprint(auth_bp)
    except ImportError:
        pass

    try:
        from routes.dashboard import dashboard_bp
        app.register_blueprint(dashboard_bp)
    except ImportError:
        pass

    try:
        from routes.violations import violations_bp
        app.register_blueprint(violations_bp)
    except ImportError:
        pass

    try:
        from routes.public import public_bp
        app.register_blueprint(public_bp)
    except ImportError:
        pass

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)