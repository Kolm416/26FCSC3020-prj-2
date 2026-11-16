'''
CSC3020 - Software Engineering Fundamentals
Instructor: Thyago Mota
Student(s): Juvia Archuleta, Leigha Lennon
Description: Project 2
'''

import os
from pathlib import Path
from flask import Flask
from flask_caching import Cache
from flask_login import LoginManager
from .models import db, User

cache = Cache()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None

def create_app(test_config=None):
    app = Flask(__name__)
    db_path = Path(app.instance_path) / 'ctf.sqlite3'
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'development-only-change-me'),
        SQLALCHEMY_DATABASE_URI='sqlite:///' + str(db_path),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CACHE_TYPE='SimpleCache',
        CACHE_DEFAULT_TIMEOUT=300,
    )
    if test_config:
        app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    cache.init_app(app)
    login_manager.init_app(app)
    from .routes import main
    app.register_blueprint(main)
    with app.app_context():
        db.create_all()
    return app