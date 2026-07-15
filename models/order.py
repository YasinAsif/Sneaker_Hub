"""
SneakerHub — Order & OrderItem Models
"""
from datetime import datetime, timezone
from extensions import db


class Order(db.Model):
    """Customer order."""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    # Statuses: Pending, Processing, Shipped, Delivered, Cancelled
    subtotal = db.Column(db.Float, nullable=False, default=0.0)
    tax = db.Column(db.Float, nullable=False, default=0.0)
    shipping = db.Column(db.Float, nullable=False, default=0.0)
    total = db.Column(db.Float, nullable=False, default=0.0)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    payment_method = db.Column(db.String(30), nullable=False, default='Cash on Delivery')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic',
                            cascade='all, delete-orphan')

    @property
    def item_count(self):
        return self.items.count()

    def __repr__(self):
        return f'<Order #{self.id} — ${self.total}>'


class OrderItem(db.Model):
    """Individual item within an order."""
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f'<OrderItem order={self.order_id} product={self.product_id} qty={self.quantity}>'
