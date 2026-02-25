from dotenv import load_dotenv
import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

# Load environment variables
load_dotenv()

# Initialize extensions
csrf = CSRFProtect()
# mail = Mail()  # Uncomment if using email

def create_app():
    from app import config
    from app.models import db

    app = Flask(__name__, instance_relative_config=True)

    # Load configuration
    app.config.from_pyfile('config.py', silent=True)
    app.config.from_object(config.DevelopmentConfig)

    # Ensure SECRET_KEY is set for CSRF
    if not app.config.get("SECRET_KEY"):
        app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") or "dev_secret_key_for_testing"

    # Initialize extensions
    csrf.init_app(app)
    db.init_app(app)
    # mail.init_app(app)
    Migrate(app, db)

    return app

# Create app instance
app = create_app()


from app import user
from app import models, form
