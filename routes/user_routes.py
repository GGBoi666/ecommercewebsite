from flask import Blueprint, render_template, request, redirect, url_for, session, flash

# Blueprint for user-related routes
user_blueprint = Blueprint('user_blueprint', __name__)

# List of products (Jewish Temples and Supermodels)
products = [
    {"id": 1, "name": "Jewish Temple 1", "price": 1000, "description": "Beautiful ancient temple.", "image_url": "Jewish_temple_1.jpg", "category": "Jewish Temple"},
    {"id": 2, "name": "Jewish Temple 2", "price": 2000, "description": "Stunning temple with gold.", "image_url": "Jewish_temple_2.jpeg", "category": "Jewish Temple"},
    {"id": 3, "name": "Jewish Temple 3", "price": 3000, "description": "Majestic temple from ancient times.", "image_url": "Jewish_temple_3.jpeg", "category": "Jewish Temple"},
    {"id": 4, "name": "Jewish Temple 4", "price": 4000, "description": "A temple of grandeur and history.", "image_url": "Jewish_temple_4.jpeg", "category": "Jewish Temple"},
    {"id": 5, "name": "Jewish Temple 5", "price": 5000, "description": "Temple with a grand view.", "image_url": "Jewish_temple_5.jpg", "category": "Jewish Temple"},
    {"id": 6, "name": "Jewish Temple 6", "price": 6000, "description": "Temple with ornate details.", "image_url": "Jewish_temple_6.jpg", "category": "Jewish Temple"},
    {"id": 7, "name": "Jewish Temple 7", "price": 7000, "description": "Beautiful temple on a hill.", "image_url": "Jewish_temple_7.jpeg", "category": "Jewish Temple"},
    {"id": 8, "name": "Jewish Temple 8", "price": 8000, "description": "A temple rich in history.", "image_url": "Jewish_temple_8.jpg", "category": "Jewish Temple"},
    {"id": 9, "name": "Jewish Temple 9", "price": 9000, "description": "A temple known for its beauty.", "image_url": "Jewish_temple_9.jpg", "category": "Jewish Temple"},
    {"id": 10, "name": "Jewish Temple 10", "price": 10000, "description": "An ancient site of worship.", "image_url": "Jewish_temple_10.jpeg", "category": "Jewish Temple"},

    {"id": 11, "name": "Supermodel 1", "price": 500, "description": "Supermodel in a fashionable pose.", "image_url": "supermodel1.webp", "category": "Supermodel"},
    {"id": 12, "name": "Supermodel 2", "price": 700, "description": "Supermodel in an elegant dress.", "image_url": "supermodel2.webp", "category": "Supermodel"},
    {"id": 13, "name": "Supermodel 3", "price": 800, "description": "Supermodel with stunning accessories.", "image_url": "supermodel3.webp", "category": "Supermodel"},
    {"id": 14, "name": "Supermodel 4", "price": 900, "description": "Supermodel striking a powerful pose.", "image_url": "supermodel4.webp", "category": "Supermodel"},
    {"id": 15, "name": "Supermodel 5", "price": 1000, "description": "Supermodel in glamorous attire.", "image_url": "supermodel5.webp", "category": "Supermodel"},
]

# Predefined users (Admin and Guest)
users = {
    "Giliboi": {"password": "admin", "role": "admin"},
    "guest": {"password": "guest", "role": "user"}
}

# Home route displaying all products with sorting and search functionality
@user_blueprint.route('/')
def home():
    # Get sorting option, search query, and category from request
    sort_by = request.args.get('sort_by', 'none')
    search_query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', 'all')

    # Filter products by search and category
    filtered_products = [product for product in products if (search_query in product['name'].lower() or search_query in product['description'].lower())]

    if category_filter != 'all':
        filtered_products = [product for product in filtered_products if product['category'] == category_filter]

    # Sort products
    if sort_by == 'price_asc':
        filtered_products = sorted(filtered_products, key=lambda x: x['price'])
    elif sort_by == 'price_desc':
        filtered_products = sorted(filtered_products, key=lambda x: x['price'], reverse=True)

    return render_template('home.html', products=filtered_products)

# Product details route
@user_blueprint.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((prod for prod in products if prod["id"] == product_id), None)
    if product:
        return render_template('product_detail.html', product=product)
    else:
        return "Product not found", 404

# Cart route
@user_blueprint.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)  # Calculate total price
    return render_template('cart.html', cart_items=cart_items, total=total)

# Add to Cart route
@user_blueprint.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart_route(product_id):
    cart = session.get('cart', [])
    product = next((prod for prod in products if prod["id"] == product_id), None)
    if product:
        cart.append(product)
        session['cart'] = cart
    return redirect(url_for('user_blueprint.cart'))

# Remove from Cart route
@user_blueprint.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    return redirect(url_for('user_blueprint.cart'))

# Login route
@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Authenticate the user
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('user_blueprint.home'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('user_blueprint.login'))
    
    return render_template('login.html')

# Logout route
@user_blueprint.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('user_blueprint.home'))

# Route to clear the cart
@user_blueprint.route('/clear_cart')
def clear_cart():
    session['cart'] = []  # Empty the cart
    return redirect(url_for('user_blueprint.cart'))

# Admin-only access route
def admin_only(f):
    def wrap(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Access denied. Admins only.', 'danger')
            return redirect(url_for('user_blueprint.home'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap
