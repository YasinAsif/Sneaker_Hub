# SneakerHub — Sneaker Marketplace

> **Buy. Sell. Collect. Authentic Sneakers.**

A full-stack sneaker marketplace web application built with Flask, SQLAlchemy, SQLite, Bootstrap 5, and vanilla JavaScript. Designed for Selenium automation testing.

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Seed the database
flask seed --drop

# 4. Run the development server
python app.py
```

Open **http://localhost:5000** in your browser.

## Login Credentials

| Role   | Username        | Password     |
|--------|----------------|--------------|
| Admin  | `admin`        | `Admin123!`  |
| Seller | `seller1`–`seller5` | `Seller123!` |
| Buyer  | `buyer1`–`buyer14`  | `Buyer123!`  |

## Tech Stack

| Layer       | Technology                     |
|-------------|--------------------------------|
| Frontend    | HTML5, CSS3, Bootstrap 5, JS   |
| Backend     | Python, Flask                  |
| Database    | SQLite + SQLAlchemy ORM        |
| Auth        | Flask-Login                    |
| Forms       | Flask-WTF (CSRF protection)    |

## Features

- **Authentication**: Register, login, logout, forgot password
- **Role-Based Access**: Buyer, Seller, Admin
- **Product Catalog**: Browse, search, filter, sort, paginate
- **Shopping Cart**: Add, update quantity, remove (AJAX)
- **Checkout**: Place orders with shipping info
- **Wishlist**: Save favorites, move to cart
- **Reviews**: Rate & review products (1-5 stars)
- **Seller Dashboard**: CRUD products, manage orders
- **Admin Dashboard**: Manage users, products, orders, reviews
- **Live Search**: Debounced search with dropdown results
- **Responsive**: Mobile-first design with dark theme

## Project Structure

```
SNEAKER_HUB/
├── app.py              # Flask app factory + seed CLI
├── config.py           # Configuration settings
├── extensions.py       # SQLAlchemy & LoginManager init
├── requirements.txt    # Python dependencies
├── models/             # SQLAlchemy models
│   ├── user.py         # User model with roles
│   ├── product.py      # Product, Brand, Category
│   ├── order.py        # Order, OrderItem
│   ├── review.py       # Product reviews
│   ├── wishlist.py     # User wishlist
│   └── cart.py         # Shopping cart
├── routes/             # Flask blueprints
│   ├── auth.py         # Authentication routes
│   ├── buyer.py        # Buyer routes (catalog, cart, etc.)
│   ├── seller.py       # Seller dashboard routes
│   ├── admin.py        # Admin dashboard routes
│   └── utils.py        # Helpers (roles, image upload)
├── templates/          # Jinja2 templates
│   ├── base.html       # Master layout
│   ├── index.html      # Home page
│   ├── catalog.html    # Product catalog
│   ├── product.html    # Product detail
│   └── ...             # 20+ templates
└── static/
    ├── css/style.css   # Complete design system
    └── js/             # JavaScript modules
```

## Selenium Testing

All interactive elements have stable `id` attributes:
- Forms: `form-login`, `form-register`, etc.
- Inputs: `input-email`, `input-password`, etc.
- Buttons: `btn-submit-login`, `btn-add-to-cart`, etc.
- Cards: `card-product-{id}`
- Tables: `table-orders`, `table-users`, etc.
