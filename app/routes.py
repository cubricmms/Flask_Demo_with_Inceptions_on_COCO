from datetime import datetime as dt

from flask import request, render_template, Blueprint, flash, redirect, url_for, abort
from flask_login import login_user, current_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError

from .core import db, photos
from .forms import SignupForm, LoginForm, UploadImageForm
from .models import Photo, User

# Blueprint Configuration
main_bp = Blueprint('main_bp', __name__, template_folder='templates', static_folder='static')


@main_bp.route('/')
def index():
    return render_template('base.html')


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


@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadImageForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filename = photos.save(request.files['animal_image'])
            url = photos.url(filename)
            photo = Photo(current_user.id, image_filename=filename, image_url=url)
            db.session.add(photo)
            db.session.commit()
            flash('New image, {}, added!'.format(photo.image_filename), 'success')
            return redirect(url_for("main_bp.show", usr=current_user.username, id=photo.id))
        else:
            # flash_errors(form)
            flash('ERROR! Recipe was not added.', 'error')
    return render_template('upload.html', form=form)


@main_bp.route('/<usr>/<id>')
@login_required
def show(usr, id):
    photo = Photo.query.filter(Photo.id == int(id)).first()
    if photo is None:
        abort(404)
    url = photos.url(photo.image_filename)
    return render_template('image-display.html', url=url, photo=photo.image_filename)


@main_bp.route('/show/<usr>/<uid>')
@login_required
def show_all(usr, uid):
    _photos = Photo.query.filter(Photo.user_id == int(uid)).all()
    if photos is None:
        abort(404)
    # url = photos.url(photo.image_filename)
    return render_template('my-upload.html', photos=_photos)
