"""Initialize app."""
from flask import Flask, url_for
from flask_uploads import configure_uploads, patch_request_class

from app.core import db, login_manager, migrate, photos, drop_zone
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

    drop_zone.init_app(app)
    app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
    app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
    app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
    app.config['DROPZONE_PARALLEL_UPLOADS'] = 3

    migrate.init_app(app, db)

    with app.app_context():
        from . import routes

        @login_manager.user_loader
        def load_user(user_id):

            return User.query.filter(User.id == int(user_id)).first()

        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        # app.register_blueprint(auth.auth_bp)

        return app
