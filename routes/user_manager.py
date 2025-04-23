from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import logout_user, login_required, login_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import DataBase
from models.user import User
from models.forms import RegisterForm, LoginForm, UpdateProfileForm

users_bp = Blueprint('users', __name__)
login_manager = LoginManager()
login_manager.login_view = 'users.login'


@login_manager.user_loader
def load_user(user_id):
    with DataBase() as db:
        user = db.load_user(user_id)
    if user:
        return User(user[0], user[1], user[2])
    return None


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        with DataBase() as db:
            user = db.load_user_by_email(email)
        if user and check_password_hash(user[3], password):
            login_user(User(user[0], user[1], user[2]))
            return redirect(url_for('home'))
        else:
            return render_template('users/login.html', form=form, error='Invalid credentials')
    return render_template('users/login.html', form=form)


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        with DataBase() as db:
            existing_user = db.load_user_by_email(email)
            if existing_user:
                return render_template('users/register.html', form=form, error="Email already registered.")
            
            hashed_password = generate_password_hash(password)
            db.create_user(name, email, hashed_password)
        return redirect(url_for('users.login'))
    return render_template('users/register.html', form=form)


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@users_bp.route('/profile')
@login_required
def profile():
    with DataBase() as db:
        user = db.load_user(current_user.id)
        events_attended = db.get_user_attended_events(current_user.id)
        events_created = db.get_user_created_events(current_user.id)
    if user:
        user = User(user[0], user[1], user[2])
        return render_template('users/profile.html', user=current_user, events_attended=events_attended, events_created=events_created)
    return redirect(url_for('users.login'))


@users_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateProfileForm(obj=current_user)
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        with DataBase() as db:
            if password:
                hashed_password = generate_password_hash(password)
                db.update_user(current_user.id, name, email, hashed_password)
            else:
                db.update_user(current_user.id, name, email)
        return redirect(url_for('users.profile'))
    return render_template('users/update_profile.html', form=form)


@users_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    with DataBase() as db:
        db.delete_user(current_user.id)
    logout_user()
    return redirect(url_for('home'))