from flask import Flask
from .config import Config
from .extensions import db, migrate , jwt, bcrypt




def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    from app.models.user import User
    from app.routes.auth import auth
    app.register_blueprint(auth)

    return app