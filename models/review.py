"""
SneakerHub — Review Model
"""
from datetime import datetime, timezone
from extensions import db


class Review(db.Model):
    """Product review left by a buyer."""
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1–5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Unique constraint: one review per user per product
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='unique_user_product_review'),
    )

    def __repr__(self):
        return f'<Review user={self.user_id} product={self.product_id} rating={self.rating}>'
