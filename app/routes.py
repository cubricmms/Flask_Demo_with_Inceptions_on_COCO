from datetime import datetime as dt

import requests
from flask import request, render_template, Blueprint, flash, redirect, url_for, abort
from flask_login import login_user, current_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError

from .core import db, photos
from .forms import SignupForm, LoginForm, UploadImageForm
from .models import Photo, User
from .utils import get_image_np, coco_labels

from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from werkzeug.datastructures import FileStorage
from io import BytesIO

# Blueprint Configuration
main_bp = Blueprint('main_bp', __name__, template_folder='templates', static_folder='static')


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.username.data, form.email.data, dt.now(), False)
                new_user.set_password(form.password.data)
                new_user.authenticated = True
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering!', 'success')
                return redirect(url_for('main_bp.login'))
            except IntegrityError:
                db.session.rollback()
                flash('ERROR! Email ({}) already exists.'.format(form.email.data), 'error')
    return render_template('/auth/register.html', form=form)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.check_password(form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('Thanks for logging in, {}'.format(current_user.email))
                return redirect(url_for('main_bp.index'))
            else:
                flash('ERROR! Incorrect login credentials.', 'error')
    return render_template('/auth/login.html', form=form)


@main_bp.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('Goodbye!', 'info')
    return redirect(url_for('main_bp.login'))


def save_and_predict(file):
    filename = photos.save(file)
    url = photos.url(filename)
    path = photos.path(filename)
    payload = {"instances": [get_image_np(path).tolist()]}
    res = requests.post("http://localhost:8080/v1/models/default:predict", json=payload)
    predictions = res.json().get('predictions')[0]
    num_detections = predictions.get('num_detections')
    num_detections = int(num_detections)
    detection_classes, detection_boxes, detection_scores = predictions.get('detection_classes')[:num_detections], \
                                                           predictions.get('detection_boxes')[:num_detections], \
                                                           predictions.get('detection_scores')[:num_detections]

    source_img = Image.open(photos.path(filename)).convert("RGB")
    width, height = source_img.size
    for idx, box in enumerate(detection_boxes):
        ymin, xmin, ymax, xmax = height * box[0], width * box[1], height * box[2], width * box[3]
        draw = ImageDraw.Draw(source_img)
        draw.rectangle(((xmin, ymin), (xmax, ymax)))
        draw.text((xmin, ymin),
                  "class: %s confidence %s" % (
                      coco_labels[int(detection_classes[idx])], str(round(detection_scores[idx], 2))))
    image_io = BytesIO()
    source_img.save(image_io, format="JPEG")

    image_io.seek(0)

    processed_filename = 'proccessed_' + filename
    image_storage = FileStorage(stream=image_io, filename=processed_filename)
    photos.save(image_storage)
    processed_url = photos.url(processed_filename)
    photo = Photo(current_user.id, image_filename=filename, image_url=url, num_detection=num_detections,
                  boxes=detection_boxes, classes=detection_classes, score=detection_scores,
                  processed_filename=processed_filename, processed_url=processed_url)
    db.session.add(photo)
    db.session.commit()
    flash('New image, {}, added!'.format(photo.image_filename), 'success')


@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadImageForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            file = request.files['animal_image']
            save_and_predict(file)
            return redirect(url_for('main_bp.show_all'))
        elif request.files:
            file_obj = request.files
            for f in file_obj:
                file = request.files.get(f)
                save_and_predict(file)
            return redirect(url_for('main_bp.show_all'))
        else:
            flash('ERROR! Image was not added.', 'error')
    return render_template('upload.html', form=form)


@main_bp.route('/show-all')
@login_required
def show_all():
    uid = current_user.id
    _photos = Photo.query.filter(Photo.user_id == int(uid)).all()

    if photos is None:
        abort(404)
    return render_template('my-upload.html', photos=_photos)
