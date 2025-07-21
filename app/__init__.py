from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

# baza
db = SQLAlchemy()
migrate = Migrate()

# mail objekt
mail = Mail()


# inicijalizacija aplikacije
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    with app.app_context():
        from . import routes, models

        db.create_all()

    return app
