"""
SneakerHub — Authentication Routes
Handles registration, login, logout, and forgot password.
"""
import re
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with full validation."""
    if current_user.is_authenticated:
        return redirect(url_for('buyer.home'))

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        phone = request.form.get('phone', '').strip()
        country = request.form.get('country', '').strip()
        role = request.form.get('role', 'buyer')

        # --- Server-side validation ---
        errors = []

        if not first_name:
            errors.append('First name is required.')
        if not last_name:
            errors.append('Last name is required.')
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters.')
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('A valid email address is required.')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters.')
        if not re.search(r'[A-Z]', password):
            errors.append('Password must contain at least one uppercase letter.')
        if not re.search(r'[0-9]', password):
            errors.append('Password must contain at least one number.')
        if password != confirm_password:
            errors.append('Passwords do not match.')
        if phone and not re.match(r'^\+?[\d\s\-]{7,20}$', phone):
            errors.append('Please enter a valid phone number.')
        if role not in ('buyer', 'seller'):
            errors.append('Invalid role selected.')

        # Uniqueness checks
        if User.query.filter_by(username=username).first():
            errors.append('Username is already taken.')
        if User.query.filter_by(email=email).first():
            errors.append('Email is already registered.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html',
                                   first_name=first_name, last_name=last_name,
                                   username=username, email=email, phone=phone,
                                   country=country, role=role)

        # Create user
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone=phone,
            country=country,
            role=role
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login with username or email."""
    if current_user.is_authenticated:
        return redirect(url_for('buyer.home'))

    if request.method == 'POST':
        login_id = request.form.get('login_id', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'

        if not login_id or not password:
            flash('Please enter your credentials.', 'danger')
            return render_template('login.html', login_id=login_id)

        # Look up by username or email
        user = User.query.filter(
            (User.username == login_id) | (User.email == login_id.lower())
        ).first()

        if user and user.check_password(password):
            if not user.is_active_user:
                flash('Your account has been deactivated. Contact support.', 'danger')
                return render_template('login.html', login_id=login_id)

            login_user(user, remember=remember)
            flash(f'Welcome back, {user.first_name}!', 'success')

            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            if user.is_seller:
                return redirect(url_for('seller.dashboard'))
            return redirect(url_for('buyer.home'))
        else:
            flash('Invalid username/email or password.', 'danger')
            return render_template('login.html', login_id=login_id)

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('buyer.home'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Simplified forgot password — resets password directly for demo/testing."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not email:
            flash('Please enter your email address.', 'danger')
            return render_template('forgot_password.html')

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('No account found with that email.', 'danger')
            return render_template('forgot_password.html', email=email)

        if not new_password or len(new_password) < 8:
            flash('New password must be at least 8 characters.', 'danger')
            return render_template('forgot_password.html', email=email)

        if new_password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('forgot_password.html', email=email)

        user.set_password(new_password)
        db.session.commit()
        flash('Password reset successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('forgot_password.html')
