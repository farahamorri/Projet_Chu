# pdg_app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)  # Ajoutez cette ligne pour initialiser Flask-Login

    from pdg_app.views import auth
    app.register_blueprint(auth)

    # Ajoutez la fonction user_loader ici
    from pdg_app.models import Doctor
    @login_manager.user_loader
    def load_user(user_id):
        return Doctor.query.get(int(user_id))


    return app