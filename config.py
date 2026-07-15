"""
SneakerHub — Application Configuration
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sneakerhub-secret-key-change-in-production')
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = db_url or f'sqlite:///{os.path.join(BASE_DIR, "database.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    PRODUCT_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'products')
    PROFILE_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'profile')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Pagination
    PRODUCTS_PER_PAGE = 12
    ORDERS_PER_PAGE = 10
    USERS_PER_PAGE = 15

    # Tax & Shipping
    TAX_RATE = 0.08  # 8%
    SHIPPING_COST = 12.99


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
