from flask import render_template, url_for, flash, redirect, request, Blueprint 
from webapp import app, db ,bcrypt
from webapp.main.forms import RegisterForm, LoginForm
from webapp.models import User, Booking, Bungalow
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    return render_template('home.html', css="home.css")

@main.route('/register', methods=["POST", "GET"])
def registreren():
    if current_user.is_authenticated:
        return redirect(url_for('main.account'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account has been created. You can now login.", 'success')
        return redirect(url_for('main.inloggen'))

    return render_template('registreren.html', form=form, title="Register")

@main.route('/login', methods=["POST", "GET"])
def inloggen():
    if current_user.is_authenticated:
        return redirect(url_for('main.account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.account'))
        else:
            flash(f"The combination of email address and password is incorrect.", 'danger')
    return render_template('login.html', form=form, title="login")

@main.route('/account')
@login_required
def account():
    bookings = Booking.query.join(Bungalow).filter(Booking.guest_id == current_user.id).all()
    return render_template('account.html', title="Account", bookings=bookings)

@main.route('/log-out')
def uitloggen():
    logout_user()
    return redirect(url_for('main.index'))

@main.errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404

@main.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

app.register_error_handler(404, not_found)
app.register_error_handler(403, forbidden)