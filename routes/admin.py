"""
SneakerHub — Admin Routes
Dashboard, user/product/order/review management.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import desc, func
from extensions import db
from models import User, Product, Brand, Category, Order, OrderItem, Review
from routes.utils import roles_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
@roles_required('admin')
def dashboard():
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.total)).scalar() or 0
    recent_orders = Order.query.order_by(desc(Order.created_at)).limit(10).all()
    # Stats for charts
    buyers = User.query.filter_by(role='buyer').count()
    sellers = User.query.filter_by(role='seller').count()
    admins = User.query.filter_by(role='admin').count()
    pending_orders = Order.query.filter_by(status='Pending').count()
    shipped_orders = Order.query.filter_by(status='Shipped').count()
    delivered_orders = Order.query.filter_by(status='Delivered').count()
    return render_template('admin_dashboard.html',
                           total_users=total_users, total_products=total_products,
                           total_orders=total_orders, total_revenue=round(total_revenue, 2),
                           recent_orders=recent_orders, buyers=buyers, sellers=sellers,
                           admins=admins, pending_orders=pending_orders,
                           shipped_orders=shipped_orders, delivered_orders=delivered_orders)


@admin_bp.route('/users')
@login_required
@roles_required('admin')
def manage_users():
    page = request.args.get('page', 1, type=int)
    role_filter = request.args.get('role', '')
    query = User.query
    if role_filter:
        query = query.filter_by(role=role_filter)
    users = query.order_by(desc(User.created_at)).paginate(page=page, per_page=15, error_out=False)
    return render_template('admin_users.html', users=users, role_filter=role_filter)


@admin_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
@login_required
@roles_required('admin')
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot deactivate yourself.', 'danger')
        return redirect(url_for('admin.manage_users'))
    user.is_active_user = not user.is_active_user
    db.session.commit()
    status = 'activated' if user.is_active_user else 'deactivated'
    flash(f'User {user.username} has been {status}.', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@roles_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete yourself.', 'danger')
        return redirect(url_for('admin.manage_users'))
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} has been deleted.', 'info')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/products')
@login_required
@roles_required('admin')
def manage_products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(desc(Product.created_at)).paginate(page=page, per_page=15, error_out=False)
    return render_template('admin_products.html', products=products)


@admin_bp.route('/products/<int:product_id>/approve', methods=['POST'])
@login_required
@roles_required('admin')
def approve_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.is_approved = not product.is_approved
    db.session.commit()
    status = 'approved' if product.is_approved else 'unapproved'
    flash(f'Product "{product.model}" {status}.', 'success')
    return redirect(url_for('admin.manage_products'))


@admin_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
@roles_required('admin')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'info')
    return redirect(url_for('admin.manage_products'))


@admin_bp.route('/orders')
@login_required
@roles_required('admin')
def manage_orders():
    page = request.args.get('page', 1, type=int)
    orders = Order.query.order_by(desc(Order.created_at)).paginate(page=page, per_page=15, error_out=False)
    return render_template('admin_orders.html', orders=orders)


@admin_bp.route('/orders/<int:order_id>/update', methods=['POST'])
@login_required
@roles_required('admin')
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status', '')
    if new_status in ('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled'):
        order.status = new_status
        db.session.commit()
        flash(f'Order #{order.id} updated to {new_status}.', 'success')
    return redirect(url_for('admin.manage_orders'))


@admin_bp.route('/reviews')
@login_required
@roles_required('admin')
def manage_reviews():
    page = request.args.get('page', 1, type=int)
    reviews = Review.query.order_by(desc(Review.created_at)).paginate(page=page, per_page=15, error_out=False)
    return render_template('admin_reviews.html', reviews=reviews)


@admin_bp.route('/reviews/<int:review_id>/delete', methods=['POST'])
@login_required
@roles_required('admin')
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted.', 'info')
    return redirect(url_for('admin.manage_reviews'))
