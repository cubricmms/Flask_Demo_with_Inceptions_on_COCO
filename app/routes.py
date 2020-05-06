from datetime import datetime as dt

from flask import current_app as app
from flask import request, render_template, Blueprint, flash, redirect, url_for, abort, g
from flask_login import login_user, current_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError

from .core import db, photos
from .forms import SignupForm, LoginForm
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
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        rec = Photo(filename=filename, user=g.user.id)
        rec.store()
        flash("Photo saved.")
        return redirect(url_for('show', id=rec.id))
    return render_template('upload.html')


@app.route('/photo/<id>')
def show(id):
    photo = Photo.load(id)
    if photo is None:
        abort(404)
    url = photos.url(photo.filename)
    return render_template('show.html', url=url, photo=photo)
