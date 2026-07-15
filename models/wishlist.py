"""
SneakerHub — Wishlist Model
"""
from datetime import datetime, timezone
from extensions import db


class Wishlist(db.Model):
    """User's saved/favorited products."""
    __tablename__ = 'wishlists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='unique_user_product_wishlist'),
    )

    def __repr__(self):
        return f'<Wishlist user={self.user_id} product={self.product_id}>'
