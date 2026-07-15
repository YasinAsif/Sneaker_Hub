"""
SneakerHub — User Model
Handles user accounts, authentication, and role-based access.
"""
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(UserMixin, db.Model):
    """User account model supporting buyer, seller, and admin roles."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(60), nullable=True)
    role = db.Column(db.String(10), nullable=False, default='buyer')  # buyer, seller, admin
    profile_image = db.Column(db.String(256), nullable=True, default='default.png')
    address = db.Column(db.Text, nullable=True)
    is_active_user = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    products = db.relationship('Product', backref='seller', lazy='dynamic',
                               foreign_keys='Product.seller_id')
    orders = db.relationship('Order', backref='buyer', lazy='dynamic',
                             foreign_keys='Order.buyer_id')
    reviews = db.relationship('Review', backref='author', lazy='dynamic')
    wishlist_items = db.relationship('Wishlist', backref='user', lazy='dynamic',
                                    cascade='all, delete-orphan')
    cart_items = db.relationship('Cart', backref='user', lazy='dynamic',
                                cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against stored hash."""
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_seller(self):
        return self.role == 'seller'

    @property
    def is_buyer(self):
        return self.role == 'buyer'

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
