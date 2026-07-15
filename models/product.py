"""
SneakerHub — Product, Brand & Category Models
"""
from datetime import datetime, timezone
from extensions import db


class Brand(db.Model):
    """Sneaker brand (e.g., Nike, Adidas)."""
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    logo = db.Column(db.String(256), nullable=True)

    products = db.relationship('Product', backref='brand', lazy='dynamic')

    def __repr__(self):
        return f'<Brand {self.name}>'


class Category(db.Model):
    """Product category (e.g., Basketball, Running)."""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)

    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    """Sneaker product listing."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    model = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    price = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # Men, Women, Unisex
    sizes = db.Column(db.Text, nullable=False, default='[]')  # JSON array of available sizes
    condition = db.Column(db.String(20), nullable=False, default='New')  # New, Used, Refurbished
    stock = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text, nullable=True)
    release_year = db.Column(db.Integer, nullable=True)
    images = db.Column(db.Text, nullable=True, default='[]')  # JSON array of image filenames
    is_approved = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    reviews = db.relationship('Review', backref='product', lazy='dynamic',
                              cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    wishlist_entries = db.relationship('Wishlist', backref='product', lazy='dynamic',
                                      cascade='all, delete-orphan')
    cart_entries = db.relationship('Cart', backref='product', lazy='dynamic',
                                  cascade='all, delete-orphan')

    @property
    def average_rating(self):
        """Calculate average review rating."""
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def sizes_list(self):
        """Return sizes as a Python list."""
        import json
        try:
            return json.loads(self.sizes)
        except (json.JSONDecodeError, TypeError):
            return []

    @property
    def images_list(self):
        """Return images as a Python list."""
        import json
        try:
            return json.loads(self.images)
        except (json.JSONDecodeError, TypeError):
            return []

    @property
    def primary_image(self):
        """Return the first image or a default placeholder."""
        imgs = self.images_list
        return imgs[0] if imgs else 'default_sneaker.png'

    def __repr__(self):
        return f'<Product {self.model} (${self.price})>'
