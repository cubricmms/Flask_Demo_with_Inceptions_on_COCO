"""Initialize app."""
from flask import Flask
from app.core import db, login_manager, migrate, rdb, cache_rdb, photos
from flask_uploads import configure_uploads, patch_request_class
from .models import User


def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('configuration.Config')

    # Initialize Plugins
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Initial upload with photos, set default upload size to 16 megabytes
    configure_uploads(app, photos)
    patch_request_class(app)  # set maximum file size, default is 16MB

    migrate.init_app(app, db)

    with app.app_context():
        from . import routes

        @login_manager.user_loader
        def load_user(user_id):
            return User.get(user_id)

        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        # app.register_blueprint(auth.auth_bp)

        return app
