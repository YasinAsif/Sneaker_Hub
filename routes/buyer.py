"""
SneakerHub — Buyer Routes
Home, catalog, product detail, search, cart, checkout, wishlist, profile, orders, reviews.
"""
import json
from flask import (Blueprint, render_template, redirect, url_for, flash,
                   request, jsonify, current_app, abort)
from flask_login import login_required, current_user
from sqlalchemy import or_, desc, asc
from extensions import db
from models import Product, Brand, Category, Cart, Wishlist, Order, OrderItem, Review
from routes.utils import save_image

buyer_bp = Blueprint('buyer', __name__)


@buyer_bp.route('/')
def home():
    featured = Product.query.filter_by(is_featured=True, is_approved=True).limit(8).all()
    latest = Product.query.filter_by(is_approved=True).order_by(desc(Product.created_at)).limit(8).all()
    brands = Brand.query.all()
    trending = Product.query.filter_by(is_approved=True).all()
    trending = sorted(trending, key=lambda p: p.average_rating, reverse=True)[:8]
    return render_template('index.html', featured=featured, latest=latest,
                           brands=brands, trending=trending)


@buyer_bp.route('/catalog')
def catalog():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PRODUCTS_PER_PAGE']
    query = Product.query.filter_by(is_approved=True)

    brand_filter = request.args.get('brand', '')
    category_filter = request.args.get('category', '')
    color_filter = request.args.get('color', '')
    gender_filter = request.args.get('gender', '')
    condition_filter = request.args.get('condition', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    size_filter = request.args.get('size', '')

    if brand_filter:
        brand_obj = Brand.query.filter_by(slug=brand_filter).first()
        if brand_obj:
            query = query.filter_by(brand_id=brand_obj.id)
    if category_filter:
        cat_obj = Category.query.filter_by(slug=category_filter).first()
        if cat_obj:
            query = query.filter_by(category_id=cat_obj.id)
    if color_filter:
        query = query.filter(Product.color.ilike(f'%{color_filter}%'))
    if gender_filter:
        query = query.filter_by(gender=gender_filter)
    if condition_filter:
        query = query.filter_by(condition=condition_filter)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if size_filter:
        query = query.filter(Product.sizes.contains(f'"{size_filter}"'))

    sort = request.args.get('sort', 'newest')
    sort_map = {
        'oldest': asc(Product.created_at),
        'price_low': asc(Product.price),
        'price_high': desc(Product.price),
        'name_az': asc(Product.model),
        'name_za': desc(Product.model),
    }
    query = query.order_by(sort_map.get(sort, desc(Product.created_at)))

    products = query.paginate(page=page, per_page=per_page, error_out=False)
    brands = Brand.query.order_by(Brand.name).all()
    categories = Category.query.order_by(Category.name).all()
    colors = [c[0] for c in db.session.query(Product.color).distinct().order_by(Product.color).all()]

    return render_template('catalog.html', products=products, brands=brands,
                           categories=categories, colors=colors,
                           current_filters={'brand': brand_filter, 'category': category_filter,
                                            'color': color_filter, 'gender': gender_filter,
                                            'condition': condition_filter, 'min_price': min_price,
                                            'max_price': max_price, 'size': size_filter, 'sort': sort})


@buyer_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = product.reviews.order_by(desc(Review.created_at)).all()
    related = Product.query.filter(Product.brand_id == product.brand_id,
                                   Product.id != product.id,
                                   Product.is_approved == True).limit(4).all()
    in_wishlist = False
    user_review = None
    if current_user.is_authenticated:
        in_wishlist = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first() is not None
        user_review = Review.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    return render_template('product.html', product=product, reviews=reviews,
                           related=related, in_wishlist=in_wishlist, user_review=user_review)


@buyer_bp.route('/search')
def search():
    q = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    if not q:
        return render_template('search_results.html', products=None, query='')
    query = Product.query.filter(Product.is_approved == True)
    brand_matches = Brand.query.filter(Brand.name.ilike(f'%{q}%')).all()
    brand_ids = [b.id for b in brand_matches]
    query = query.filter(or_(Product.model.ilike(f'%{q}%'), Product.description.ilike(f'%{q}%'),
                             Product.color.ilike(f'%{q}%'), Product.brand_id.in_(brand_ids) if brand_ids else False))
    products = query.order_by(desc(Product.created_at)).paginate(
        page=page, per_page=current_app.config['PRODUCTS_PER_PAGE'], error_out=False)
    return render_template('search_results.html', products=products, query=q)


@buyer_bp.route('/api/search')
def api_search():
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify([])
    products = Product.query.filter(Product.is_approved == True,
                                    or_(Product.model.ilike(f'%{q}%'), Product.color.ilike(f'%{q}%'))).limit(8).all()
    results = [{'id': p.id, 'model': p.model, 'brand': p.brand.name, 'price': p.price,
                'image': p.primary_image, 'url': url_for('buyer.product_detail', product_id=p.id)} for p in products]
    return jsonify(results)


@buyer_bp.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    subtotal = sum(item.subtotal for item in cart_items)
    tax = round(subtotal * current_app.config['TAX_RATE'], 2)
    shipping = current_app.config['SHIPPING_COST'] if cart_items else 0
    total = round(subtotal + tax + shipping, 2)
    return render_template('cart.html', cart_items=cart_items, subtotal=subtotal,
                           tax=tax, shipping=shipping, total=total)


@buyer_bp.route('/cart/add', methods=['POST'])
@login_required
def cart_add():
    product_id = request.form.get('product_id', type=int)
    size = request.form.get('size', '')
    quantity = request.form.get('quantity', 1, type=int)
    product = Product.query.get_or_404(product_id)
    if product.stock < 1:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Out of stock.'}), 400
        flash('Product is out of stock.', 'danger')
        return redirect(url_for('buyer.product_detail', product_id=product_id))
    existing = Cart.query.filter_by(user_id=current_user.id, product_id=product_id, size=size).first()
    if existing:
        existing.quantity += quantity
    else:
        db.session.add(Cart(user_id=current_user.id, product_id=product_id, quantity=quantity, size=size))
    db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': 'Added to cart!',
                        'cart_count': Cart.query.filter_by(user_id=current_user.id).count()})
    flash('Product added to cart!', 'success')
    return redirect(url_for('buyer.product_detail', product_id=product_id))


@buyer_bp.route('/cart/update', methods=['POST'])
@login_required
def cart_update():
    cart_id = request.form.get('cart_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id != current_user.id:
        abort(403)
    if quantity < 1:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = min(quantity, cart_item.product.stock)
    db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        items = Cart.query.filter_by(user_id=current_user.id).all()
        subtotal = sum(i.subtotal for i in items)
        tax = round(subtotal * current_app.config['TAX_RATE'], 2)
        shipping = current_app.config['SHIPPING_COST'] if items else 0
        return jsonify({'success': True, 'subtotal': round(subtotal, 2), 'tax': tax,
                        'shipping': shipping, 'total': round(subtotal + tax + shipping, 2),
                        'cart_count': len(items)})
    flash('Cart updated.', 'success')
    return redirect(url_for('buyer.cart'))


@buyer_bp.route('/cart/remove', methods=['POST'])
@login_required
def cart_remove():
    cart_id = request.form.get('cart_id', type=int)
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id != current_user.id:
        abort(403)
    db.session.delete(cart_item)
    db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        items = Cart.query.filter_by(user_id=current_user.id).all()
        subtotal = sum(i.subtotal for i in items)
        tax = round(subtotal * current_app.config['TAX_RATE'], 2)
        shipping = current_app.config['SHIPPING_COST'] if items else 0
        return jsonify({'success': True, 'subtotal': round(subtotal, 2), 'tax': tax,
                        'shipping': shipping, 'total': round(subtotal + tax + shipping, 2),
                        'cart_count': len(items)})
    flash('Item removed from cart.', 'info')
    return redirect(url_for('buyer.cart'))


@buyer_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('buyer.cart'))
    subtotal = sum(item.subtotal for item in cart_items)
    tax = round(subtotal * current_app.config['TAX_RATE'], 2)
    shipping = current_app.config['SHIPPING_COST']
    total = round(subtotal + tax + shipping, 2)
    if request.method == 'POST':
        address = request.form.get('address', '').strip()
        phone = request.form.get('phone', '').strip()
        payment_method = request.form.get('payment_method', 'Cash on Delivery')
        if not address or not phone:
            flash('Address and phone are required.', 'danger')
            return render_template('checkout.html', cart_items=cart_items,
                                   subtotal=subtotal, tax=tax, shipping=shipping, total=total)
        order = Order(buyer_id=current_user.id, subtotal=round(subtotal, 2), tax=tax,
                      shipping=shipping, total=total, address=address, phone=phone,
                      payment_method=payment_method)
        db.session.add(order)
        db.session.flush()
        for ci in cart_items:
            db.session.add(OrderItem(order_id=order.id, product_id=ci.product_id,
                                     quantity=ci.quantity, price=ci.product.price, size=ci.size))
            ci.product.stock = max(0, ci.product.stock - ci.quantity)
        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('buyer.orders'))
    return render_template('checkout.html', cart_items=cart_items,
                           subtotal=subtotal, tax=tax, shipping=shipping, total=total)


@buyer_bp.route('/orders')
@login_required
def orders():
    page = request.args.get('page', 1, type=int)
    user_orders = Order.query.filter_by(buyer_id=current_user.id).order_by(
        desc(Order.created_at)).paginate(page=page, per_page=current_app.config['ORDERS_PER_PAGE'], error_out=False)
    return render_template('orders.html', orders=user_orders)


@buyer_bp.route('/wishlist')
@login_required
def wishlist():
    items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', wishlist_items=items)


@buyer_bp.route('/wishlist/add', methods=['POST'])
@login_required
def wishlist_add():
    product_id = request.form.get('product_id', type=int)
    Product.query.get_or_404(product_id)
    if not Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first():
        db.session.add(Wishlist(user_id=current_user.id, product_id=product_id))
        db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': 'Added to wishlist!'})
    flash('Added to wishlist!', 'success')
    return redirect(url_for('buyer.product_detail', product_id=product_id))


@buyer_bp.route('/wishlist/remove', methods=['POST'])
@login_required
def wishlist_remove():
    product_id = request.form.get('product_id', type=int)
    item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': 'Removed from wishlist.'})
    flash('Removed from wishlist.', 'info')
    return redirect(request.referrer or url_for('buyer.wishlist'))


@buyer_bp.route('/wishlist/move-to-cart', methods=['POST'])
@login_required
def wishlist_move_to_cart():
    product_id = request.form.get('product_id', type=int)
    product = Product.query.get_or_404(product_id)
    existing_cart = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing_cart:
        existing_cart.quantity += 1
    else:
        sizes = product.sizes_list
        db.session.add(Cart(user_id=current_user.id, product_id=product_id,
                            quantity=1, size=sizes[0] if sizes else ''))
    Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).delete()
    db.session.commit()
    flash('Moved to cart!', 'success')
    return redirect(url_for('buyer.wishlist'))


@buyer_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name', '').strip()
        current_user.last_name = request.form.get('last_name', '').strip()
        current_user.phone = request.form.get('phone', '').strip()
        current_user.country = request.form.get('country', '').strip()
        current_user.address = request.form.get('address', '').strip()
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename:
                filename = save_image(file, subfolder='profile')
                if filename:
                    current_user.profile_image = filename
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('buyer.profile'))
    recent_orders = Order.query.filter_by(buyer_id=current_user.id).order_by(
        desc(Order.created_at)).limit(5).all()
    return render_template('profile.html', recent_orders=recent_orders)


@buyer_bp.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    if not current_user.check_password(current_password):
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('buyer.profile'))
    if len(new_password) < 8:
        flash('New password must be at least 8 characters.', 'danger')
        return redirect(url_for('buyer.profile'))
    if new_password != confirm_password:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('buyer.profile'))
    current_user.set_password(new_password)
    db.session.commit()
    flash('Password changed successfully!', 'success')
    return redirect(url_for('buyer.profile'))


@buyer_bp.route('/review/add', methods=['POST'])
@login_required
def review_add():
    product_id = request.form.get('product_id', type=int)
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '').strip()
    Product.query.get_or_404(product_id)
    if not rating or rating < 1 or rating > 5:
        flash('Please select a rating (1-5).', 'danger')
        return redirect(url_for('buyer.product_detail', product_id=product_id))
    existing = Review.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        existing.rating = rating
        existing.comment = comment
        flash('Review updated!', 'success')
    else:
        db.session.add(Review(user_id=current_user.id, product_id=product_id, rating=rating, comment=comment))
        flash('Review submitted!', 'success')
    db.session.commit()
    return redirect(url_for('buyer.product_detail', product_id=product_id))


@buyer_bp.route('/reviews')
@login_required
def reviews():
    user_reviews = Review.query.filter_by(user_id=current_user.id).order_by(desc(Review.created_at)).all()
    return render_template('reviews.html', reviews=user_reviews)


@buyer_bp.app_context_processor
def cart_count_processor():
    if current_user.is_authenticated:
        return {'cart_count': Cart.query.filter_by(user_id=current_user.id).count()}
    return {'cart_count': 0}
