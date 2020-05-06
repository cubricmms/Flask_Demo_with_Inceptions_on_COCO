"""Initialize app."""
from flask import Flask
from app.core import db, login_manager, migrate, rdb, cache_rdb
# from flask_caching import RedisCache


def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('configuration.Config')

    # 处理 X-FORWARD- 系列 HTTP 头
    # app.wsgi_app = ProxyFix(app.wsgi_app)

    # Initialize Plugins
    db.init_app(app)

    login_manager.init_app(app)

    migrate.init_app(app, db)

    # rdb.init_app(app, config_prefix='REDIS')
    # cache_rdb.init_app(app, config_prefix='CACHE')
    # backend = RedisCache(cache_rdb, key_prefix='pg:cache:')

    with app.app_context():
        from . import routes
        from . import auth

        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        return app
