# -*- encoding: utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'dev_users'
    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(64),
                         index=False,
                         unique=True,
                         nullable=False)
    email = db.Column(db.String(40),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)
    website = db.Column(db.String(60),
                        index=False,
                        unique=False,
                        nullable=True)
    created_on = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)
    last_login = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)
    admin = db.Column(db.Boolean,
                      index=False,
                      unique=False,
                      nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, create, admin):
        self.username = username
        self.email = email
        self.created_on = create
        self.admin = admin
        self.authenticated = False

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Photo(db.Model):
    __tablename__ = "photo"

    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('dev_users.id'))
    boxes = db.Column(db.ARRAY(db.Float()), default=None, nullable=True)
    score = db.Column(db.ARRAY(db.Float()), default=None, nullable=True)
    classes = db.Column(db.ARRAY(db.Integer()), default=None, nullable=True)
    num_detection = db.Column(db.Integer, default=None, nullable=True)

    def __init__(self, user_id, image_filename=None, image_url=None, boxes=None, score=None, classes=None,
                 num_detection=None):
        self.image_filename = image_filename
        self.image_url = image_url
        self.user_id = user_id
        self.boxes = boxes
        self.score = score
        self.classes = classes
        self.num_detection = num_detection

    def __repr__(self):
        return '<id: {}, user_id: {}, filename: {}, url: {}, boxes: {}, score: {}, classes:{}, num_detection: {}>'.format(
            self.id, self.user_id, self.image_filename,
            self.image_url, self.boxes, self.score, self.classes, self.num_detection)
