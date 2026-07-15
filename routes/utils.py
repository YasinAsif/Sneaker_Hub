"""
SneakerHub — Utility Helpers
Role decorators, image upload, pagination helpers.
"""
import os
import uuid
from functools import wraps
from flask import abort, current_app, flash, redirect, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename


def roles_required(*roles):
    """Decorator to restrict route access to specific user roles."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            if current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_image(file, subfolder='products'):
    """
    Save uploaded image with a unique filename.
    Returns the saved filename or None on failure.
    """
    if not file or file.filename == '':
        return None

    if not allowed_file(file.filename):
        return None

    # Generate unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"

    if subfolder == 'products':
        upload_path = current_app.config['PRODUCT_UPLOAD_FOLDER']
    else:
        upload_path = current_app.config['PROFILE_UPLOAD_FOLDER']

    os.makedirs(upload_path, exist_ok=True)
    file.save(os.path.join(upload_path, filename))
    return filename


def delete_image(filename, subfolder='products'):
    """Delete an uploaded image file."""
    if not filename or filename in ('default.png', 'default_sneaker.png'):
        return
    if subfolder == 'products':
        path = os.path.join(current_app.config['PRODUCT_UPLOAD_FOLDER'], filename)
    else:
        path = os.path.join(current_app.config['PROFILE_UPLOAD_FOLDER'], filename)
    if os.path.exists(path):
        os.remove(path)
