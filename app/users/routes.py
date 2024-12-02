from flask import Flask, render_template, request, redirect, flash, url_for,Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from app.users.forms import LoginForm, SignupForm  # Import the form classes

user = Blueprint('user',__name__)

# Login route
@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('exam.home'))  # Redirect to a dashboard or homepage
        except Exception as e:

            flash('User not found','danger')
            return(redirect(url_for('user.login')))
            # flash('Login successful!', 'success')
        else:
            flash('Invalid email or password!', 'danger')
            return(redirect(url_for('user.login')))
    return render_template('login.html', form=form)  # Render the login page

# Signup route
@user.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered!', 'danger')
            return redirect(url_for('user.signup'))

        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('user.login'))

    return render_template('signup.html', form=form)  # Render the signup page

# Dashboard route (protected)
@user.route('/dashboard')
@login_required
def dashboard():
    return f"Welcome, {current_user.username}! This is your dashboard."

# Logout route
@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('user.login'))
