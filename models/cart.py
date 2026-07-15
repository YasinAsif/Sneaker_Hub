"""
SneakerHub — Cart Model
"""
from datetime import datetime, timezone
from extensions import db


class Cart(db.Model):
    """Shopping cart item."""
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    size = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', 'size', name='unique_cart_item'),
    )

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __repr__(self):
        return f'<Cart user={self.user_id} product={self.product_id} qty={self.quantity}>'
