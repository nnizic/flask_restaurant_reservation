from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

# baza
db = SQLAlchemy()
migrate = Migrate()

# mail objekt
mail = Mail()

# logiranje admina
login_manager = LoginManager()


# inicijalizacija aplikacije
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = "login"  # ako nije prijavljen ide tu

    with app.app_context():
        from . import routes, models
        from .models import Admin

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    return app
