"""
SneakerHub — Seller Routes
Dashboard, product CRUD, order management for sellers.
"""
import json
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import desc
from extensions import db
from models import Product, Brand, Category, Order, OrderItem
from routes.utils import roles_required, save_image, delete_image

seller_bp = Blueprint('seller', __name__, url_prefix='/seller')


@seller_bp.route('/dashboard')
@login_required
@roles_required('seller', 'admin')
def dashboard():
    products = Product.query.filter_by(seller_id=current_user.id).all()
    total_products = len(products)
    total_stock = sum(p.stock for p in products)
    # Sales via order items
    from models import OrderItem
    product_ids = [p.id for p in products]
    order_items = OrderItem.query.filter(OrderItem.product_id.in_(product_ids)).all() if product_ids else []
    total_sales = len(order_items)
    total_revenue = sum(oi.price * oi.quantity for oi in order_items)
    return render_template('seller_dashboard.html', products=products,
                           total_products=total_products, total_stock=total_stock,
                           total_sales=total_sales, total_revenue=total_revenue)


@seller_bp.route('/add-product', methods=['GET', 'POST'])
@login_required
@roles_required('seller', 'admin')
def add_product():
    brands = Brand.query.order_by(Brand.name).all()
    categories = Category.query.order_by(Category.name).all()
    if request.method == 'POST':
        model = request.form.get('model', '').strip()
        brand_id = request.form.get('brand_id', type=int)
        category_id = request.form.get('category_id', type=int)
        price = request.form.get('price', type=float)
        color = request.form.get('color', '').strip()
        gender = request.form.get('gender', 'Unisex')
        sizes = request.form.getlist('sizes')
        condition = request.form.get('condition', 'New')
        stock = request.form.get('stock', 0, type=int)
        description = request.form.get('description', '').strip()
        release_year = request.form.get('release_year', type=int)
        sku = request.form.get('sku', '').strip()

        errors = []
        if not model:
            errors.append('Model name is required.')
        if not brand_id:
            errors.append('Brand is required.')
        if not category_id:
            errors.append('Category is required.')
        if not price or price <= 0:
            errors.append('Valid price is required.')
        if not sku:
            errors.append('SKU is required.')
        elif Product.query.filter_by(sku=sku).first():
            errors.append('SKU already exists.')
        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('seller_add_product.html', brands=brands, categories=categories)

        # Handle images
        images = []
        if 'images' in request.files:
            files = request.files.getlist('images')
            for f in files[:5]:  # Max 5 images
                filename = save_image(f, subfolder='products')
                if filename:
                    images.append(filename)

        product = Product(
            seller_id=current_user.id, brand_id=brand_id, category_id=category_id,
            model=model, sku=sku, price=price, color=color, gender=gender,
            sizes=json.dumps(sizes), condition=condition, stock=stock,
            description=description, release_year=release_year,
            images=json.dumps(images)
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('seller.dashboard'))
    return render_template('seller_add_product.html', brands=brands, categories=categories)


@seller_bp.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
@login_required
@roles_required('seller', 'admin')
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id != current_user.id and not current_user.is_admin:
        abort(403)
    brands = Brand.query.order_by(Brand.name).all()
    categories = Category.query.order_by(Category.name).all()
    if request.method == 'POST':
        product.model = request.form.get('model', '').strip()
        product.brand_id = request.form.get('brand_id', type=int)
        product.category_id = request.form.get('category_id', type=int)
        product.price = request.form.get('price', type=float)
        product.color = request.form.get('color', '').strip()
        product.gender = request.form.get('gender', 'Unisex')
        product.sizes = json.dumps(request.form.getlist('sizes'))
        product.condition = request.form.get('condition', 'New')
        product.stock = request.form.get('stock', 0, type=int)
        product.description = request.form.get('description', '').strip()
        product.release_year = request.form.get('release_year', type=int)
        new_sku = request.form.get('sku', '').strip()
        if new_sku != product.sku:
            if Product.query.filter_by(sku=new_sku).first():
                flash('SKU already exists.', 'danger')
                return render_template('seller_edit_product.html', product=product,
                                       brands=brands, categories=categories)
            product.sku = new_sku
        if 'images' in request.files:
            files = request.files.getlist('images')
            new_images = []
            for f in files[:5]:
                filename = save_image(f, subfolder='products')
                if filename:
                    new_images.append(filename)
            if new_images:
                product.images = json.dumps(new_images)
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('seller.dashboard'))
    return render_template('seller_edit_product.html', product=product,
                           brands=brands, categories=categories)


@seller_bp.route('/delete-product/<int:product_id>', methods=['POST'])
@login_required
@roles_required('seller', 'admin')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id != current_user.id and not current_user.is_admin:
        abort(403)
    for img in product.images_list:
        delete_image(img, subfolder='products')
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'info')
    return redirect(url_for('seller.dashboard'))


@seller_bp.route('/orders')
@login_required
@roles_required('seller', 'admin')
def seller_orders():
    product_ids = [p.id for p in Product.query.filter_by(seller_id=current_user.id).all()]
    order_items = OrderItem.query.filter(OrderItem.product_id.in_(product_ids)).all() if product_ids else []
    order_ids = list(set(oi.order_id for oi in order_items))
    orders = Order.query.filter(Order.id.in_(order_ids)).order_by(desc(Order.created_at)).all() if order_ids else []
    return render_template('seller_orders.html', orders=orders)


@seller_bp.route('/order/<int:order_id>/update', methods=['POST'])
@login_required
@roles_required('seller', 'admin')
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status', '')
    if new_status in ('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled'):
        order.status = new_status
        db.session.commit()
        flash(f'Order #{order.id} status updated to {new_status}.', 'success')
    return redirect(url_for('seller.seller_orders'))
