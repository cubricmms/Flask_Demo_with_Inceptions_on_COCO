from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_uploads import UploadSet, IMAGES

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# 普通的 Redis 连接池
rdb = FlaskRedis()

# 缓存用 Redis 连接池
cache_rdb = FlaskRedis()

photos = UploadSet('photos', IMAGES)
