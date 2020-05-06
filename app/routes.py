from flask import current_app as app
from flask import request, render_template, Blueprint, flash, redirect, url_for, abort, g

from .core import photos
from .models import Photo

# Blueprint Configuration
main_bp = Blueprint('main_bp', __name__, template_folder='templates', static_folder='static')


@main_bp.route('/')
def index():
    return render_template('base.html')


@main_bp.route('/register')
def register():
    return render_template('/auth/register.html')


@main_bp.route('/login')
def login():
    return render_template('/auth/login.html')


@main_bp.route('/logout')
def logout():
    return render_template('base.html')


@app.route('/upload', methods=['GET', 'POST'])
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
