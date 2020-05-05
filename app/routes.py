from flask import request, render_template, make_response, Blueprint
from datetime import datetime as dt
from .models import db, User
from flask_login import current_user
from flask import current_app as app
from .assets import compile_auth_assets
from flask_login import login_required

# Blueprint Configuration
main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')
compile_auth_assets(app)


@main_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    """Serve logged-in Dashboard."""
    return render_template('dashboard.jinja2',
                           title='Flask-Login Tutorial.',
                           template='dashboard-template',
                           current_user=current_user,
                           body="You are now logged in!")


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))

# @app.route('/', methods=['GET'])
# def create_user():
#     """Create a user."""
#     username = request.args.get('user')
#     email = request.args.get('email')
#     if username and email:
#         existing_user = User.query.filter(User.username == username or User.email == email).first()
#         if existing_user:
#             return make_response(f'{username} ({email}) already created!')
#         new_user = User(username=username,
#                         email=email,
#                         created=dt.now(),
#                         bio="In West Philadelphia born and raised, on the playground is where I spent most of my days",
#                         admin=False)  # Create an instance of the User class
#         db.session.add(new_user)  # Adds new User record to database
#         db.session.commit()  # Commits all changes
#     return render_template('users.html',
#                            users=User.query.all(),
#                            title="Show Users")


@app.route('/list/')
def posts():
    return render_template('list.html')
