"""
SneakerHub — Application Entry Point
Flask app factory with blueprint registration, error handlers, and seed CLI.
"""
import os
import json
import click
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from extensions import db, login_manager


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload directories exist
    os.makedirs(app.config['PRODUCT_UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROFILE_UPLOAD_FOLDER'], exist_ok=True)

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    CSRFProtect(app)

    # User loader
    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth import auth_bp
    from routes.buyer import buyer_bp
    from routes.seller import seller_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(buyer_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(admin_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    # Create tables
    with app.app_context():
        db.create_all()

    # Seed CLI command
    @app.cli.command('seed')
    @click.option('--drop', is_flag=True, help='Drop all tables first.')
    def seed_db(drop):
        """Populate database with sample data."""
        with app.app_context():
            if drop:
                click.echo('Dropping all tables...')
                db.drop_all()
                db.create_all()
                click.echo('Tables recreated.')

            from models import User, Product, Brand, Category, Order, OrderItem, Review, Wishlist, Cart

            if User.query.first():
                click.echo('Database already seeded. Use --drop to reset.')
                return

            # ── Brands ──
            brands_data = [
                ('Nike', 'nike'), ('Adidas', 'adidas'), ('New Balance', 'new-balance'),
                ('Puma', 'puma'), ('ASICS', 'asics'), ('Converse', 'converse'),
                ('Reebok', 'reebok'), ('Vans', 'vans'), ('Jordan', 'jordan'),
                ('Under Armour', 'under-armour')
            ]
            brands = {}
            for name, slug in brands_data:
                b = Brand(name=name, slug=slug)
                db.session.add(b)
                brands[slug] = b
            db.session.flush()

            # ── Categories ──
            cats_data = [
                ('Basketball', 'basketball'), ('Running', 'running'),
                ('Lifestyle', 'lifestyle'), ('Skateboarding', 'skateboarding'),
                ('Training', 'training')
            ]
            categories = {}
            for name, slug in cats_data:
                c = Category(name=name, slug=slug)
                db.session.add(c)
                categories[slug] = c
            db.session.flush()

            # ── Users ──
            admin = User(first_name='Admin', last_name='User', username='admin',
                         email='admin@sneakerhub.com', phone='+1234567890',
                         country='US', role='admin')
            admin.set_password('Admin123!')
            db.session.add(admin)

            sellers = []
            for i in range(1, 6):
                s = User(first_name=f'Seller{i}', last_name='Store',
                         username=f'seller{i}', email=f'seller{i}@sneakerhub.com',
                         phone=f'+1555000{i:04d}', country='US', role='seller')
                s.set_password('Seller123!')
                db.session.add(s)
                sellers.append(s)

            buyers = []
            for i in range(1, 15):
                b = User(first_name=f'Buyer{i}', last_name='Customer',
                         username=f'buyer{i}', email=f'buyer{i}@sneakerhub.com',
                         phone=f'+1555100{i:04d}', country='US', role='buyer')
                b.set_password('Buyer123!')
                db.session.add(b)
                buyers.append(b)
            db.session.flush()

            # ── Products ──
            sneakers = [
                ('Air Max 90', 'nike', 'lifestyle', 130, 'White', 'Unisex', True),
                ('Air Force 1 Low', 'nike', 'lifestyle', 110, 'White', 'Men', True),
                ('Dunk Low Retro', 'nike', 'skateboarding', 115, 'Black/White', 'Unisex', True),
                ('Air Jordan 1 High OG', 'jordan', 'basketball', 180, 'Chicago Red', 'Men', True),
                ('Air Jordan 4 Retro', 'jordan', 'basketball', 210, 'Military Black', 'Men', True),
                ('Ultraboost 22', 'adidas', 'running', 190, 'Core Black', 'Unisex', False),
                ('Superstar Classic', 'adidas', 'lifestyle', 100, 'White/Black', 'Unisex', False),
                ('Yeezy Boost 350 V2', 'adidas', 'lifestyle', 230, 'Beluga', 'Unisex', True),
                ('Stan Smith', 'adidas', 'lifestyle', 85, 'White/Green', 'Men', False),
                ('Forum Low', 'adidas', 'basketball', 95, 'Cloud White', 'Unisex', False),
                ('550', 'new-balance', 'lifestyle', 130, 'White/Green', 'Unisex', True),
                ('990v6', 'new-balance', 'running', 200, 'Grey', 'Men', False),
                ('574 Classic', 'new-balance', 'lifestyle', 90, 'Navy', 'Men', False),
                ('327', 'new-balance', 'running', 100, 'Sea Salt', 'Women', False),
                ('2002R', 'new-balance', 'running', 150, 'Rain Cloud', 'Unisex', True),
                ('RS-X3', 'puma', 'running', 110, 'White/Blue', 'Men', False),
                ('Suede Classic', 'puma', 'lifestyle', 75, 'Black', 'Unisex', False),
                ('Slipstream Lo', 'puma', 'lifestyle', 90, 'White/Gum', 'Unisex', False),
                ('Gel-Kayano 14', 'asics', 'running', 150, 'Silver', 'Unisex', True),
                ('Gel-1130', 'asics', 'running', 120, 'White/Clay Grey', 'Unisex', False),
                ('Chuck Taylor All Star', 'converse', 'lifestyle', 60, 'Black', 'Unisex', False),
                ('Chuck 70 Hi', 'converse', 'lifestyle', 90, 'Parchment', 'Unisex', True),
                ('One Star Pro', 'converse', 'skateboarding', 85, 'Black/White', 'Men', False),
                ('Club C 85', 'reebok', 'lifestyle', 80, 'White/Green', 'Unisex', False),
                ('Classic Leather', 'reebok', 'lifestyle', 75, 'White', 'Men', False),
                ('Old Skool', 'vans', 'skateboarding', 70, 'Black/White', 'Unisex', True),
                ('Sk8-Hi', 'vans', 'skateboarding', 80, 'Black', 'Unisex', False),
                ('Authentic', 'vans', 'skateboarding', 55, 'Red', 'Unisex', False),
                ('Era', 'vans', 'lifestyle', 60, 'Navy', 'Men', False),
                ('Curry Flow 10', 'under-armour', 'basketball', 160, 'Blue', 'Men', False),
                ('HOVR Phantom 3', 'under-armour', 'running', 140, 'Black', 'Men', False),
                ('SlipSpeed', 'under-armour', 'training', 150, 'White', 'Unisex', False),
                ('Air Max 97', 'nike', 'running', 175, 'Silver Bullet', 'Men', True),
                ('Blazer Mid 77', 'nike', 'lifestyle', 105, 'White/Black', 'Unisex', False),
                ('React Infinity Run', 'nike', 'running', 160, 'Blue', 'Men', False),
                ('Air Zoom Pegasus 40', 'nike', 'running', 130, 'Black/White', 'Men', False),
                ('Air Jordan 11 Retro', 'jordan', 'basketball', 225, 'Bred', 'Men', True),
                ('NMD R1', 'adidas', 'lifestyle', 140, 'Core Black/White', 'Unisex', False),
                ('Gazelle', 'adidas', 'lifestyle', 90, 'Collegiate Navy', 'Unisex', False),
                ('Made in USA 993', 'new-balance', 'running', 175, 'Grey', 'Men', False),
                ('RS-Dreamer', 'puma', 'basketball', 125, 'Red Blast', 'Men', False),
                ('Gel-Lyte III', 'asics', 'lifestyle', 120, 'White/Black', 'Unisex', False),
                ('Run Star Hike', 'converse', 'lifestyle', 110, 'Black/White', 'Unisex', False),
                ('Question Mid', 'reebok', 'basketball', 140, 'White/Red', 'Men', False),
                ('Half Cab', 'vans', 'skateboarding', 75, 'Navy', 'Men', False),
                ('Project Rock 5', 'under-armour', 'training', 150, 'Black/Gold', 'Men', False),
                ('Air Max Plus', 'nike', 'lifestyle', 175, 'Hyper Blue', 'Men', False),
                ('Samba OG', 'adidas', 'lifestyle', 100, 'White/Black/Gum', 'Unisex', True),
                ('FuelCell Rebel v3', 'new-balance', 'running', 130, 'Neon Dragonfly', 'Women', False),
                ('Clyde All-Pro', 'puma', 'basketball', 130, 'White/Red', 'Men', False),
            ]

            all_sizes = ['6', '6.5', '7', '7.5', '8', '8.5', '9', '9.5', '10', '10.5', '11', '11.5', '12', '13']
            descs = [
                'A timeless classic that delivers comfort and style for everyday wear.',
                'Premium materials meet cutting-edge design in this iconic silhouette.',
                'Engineered for performance with responsive cushioning technology.',
                'The perfect blend of heritage design and modern comfort.',
                'Street-ready style with all-day comfort and durability.',
            ]

            products = []
            for i, (model, brand_slug, cat_slug, price, color, gender, featured) in enumerate(sneakers):
                import random
                p = Product(
                    seller_id=sellers[i % len(sellers)].id,
                    brand_id=brands[brand_slug].id,
                    category_id=categories[cat_slug].id,
                    model=model, sku=f'SH-{i+1001:04d}',
                    price=price, color=color, gender=gender,
                    sizes=json.dumps(random.sample(all_sizes, random.randint(6, 12))),
                    condition='New', stock=random.randint(3, 50),
                    description=descs[i % len(descs)],
                    release_year=random.choice([2022, 2023, 2024, 2025, 2026]),
                    images=json.dumps(['img/products/' + cat_slug + '.png'] if cat_slug in ['basketball', 'running', 'lifestyle'] else ['img/products/lifestyle.png']),
                    is_approved=True, is_featured=featured
                )
                db.session.add(p)
                products.append(p)
            db.session.flush()

            # ── Reviews ──
            import random
            comments = [
                'Absolutely love these! Super comfortable and stylish.',
                'Great quality for the price. Would definitely recommend.',
                'Fit perfectly true to size. Very happy with my purchase.',
                'The colorway is even better in person. Must cop!',
                'Decent shoes but expected better cushioning for the price.',
                'These are fire! Getting compliments everywhere I go.',
                'Good everyday sneakers. Nothing too flashy but reliable.',
                'Amazing build quality. You can tell these are premium.',
            ]
            for _ in range(40):
                r = Review(
                    user_id=random.choice(buyers).id,
                    product_id=random.choice(products).id,
                    rating=random.randint(3, 5),
                    comment=random.choice(comments)
                )
                try:
                    db.session.add(r)
                    db.session.flush()
                except Exception:
                    db.session.rollback()

            # ── Orders ──
            statuses = ['Pending', 'Processing', 'Shipped', 'Delivered']
            for _ in range(15):
                buyer = random.choice(buyers)
                num_items = random.randint(1, 3)
                order_products = random.sample(products, min(num_items, len(products)))
                subtotal = sum(p.price for p in order_products)
                tax = round(subtotal * 0.08, 2)
                shipping = 12.99
                total = round(subtotal + tax + shipping, 2)
                order = Order(
                    buyer_id=buyer.id, subtotal=round(subtotal, 2),
                    tax=tax, shipping=shipping, total=total,
                    address='123 Test Street, New York, NY 10001',
                    phone='+15551234567',
                    payment_method=random.choice(['Cash on Delivery', 'Credit Card', 'PayPal']),
                    status=random.choice(statuses)
                )
                db.session.add(order)
                db.session.flush()
                for p in order_products:
                    db.session.add(OrderItem(
                        order_id=order.id, product_id=p.id,
                        quantity=1, price=p.price,
                        size=random.choice(p.sizes_list) if p.sizes_list else '10'
                    ))

            db.session.commit()
            click.echo('Database seeded successfully!')
            click.echo('Login credentials:')
            click.echo('  Admin:  admin / Admin123!')
            click.echo('  Seller: seller1..5 / Seller123!')
            click.echo('  Buyer:  buyer1..14 / Buyer123!')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
