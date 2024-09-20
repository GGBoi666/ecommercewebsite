# Importing the products from user_routes
from routes.user_routes import products
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

# Blueprint for admin-related routes
admin_blueprint = Blueprint('admin_blueprint', __name__)

# Check if user is an admin
def admin_only(view_func):
    def wrapper(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('You do not have access to this page!', 'danger')
            return redirect(url_for('user_blueprint.home'))
        return view_func(*args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper

# Admin Dashboard Route
@admin_blueprint.route('/admin_dashboard')
@admin_only
def admin_dashboard():
    return render_template('admin/admin_dashboard.html', products=products)

# Add Product Route
@admin_blueprint.route('/add_product', methods=['GET', 'POST'])
@admin_only
def add_product():
    if request.method == 'POST':
        new_product = {
            "id": len(products) + 1,
            "name": request.form['name'],
            "price": request.form['price'],
            "description": request.form['description'],
            "image_url": request.form['image_url'],
            "category": request.form['category']
        }
        products.append(new_product)
        return redirect(url_for('admin_blueprint.admin_dashboard'))

    return render_template('admin/add_product.html')

# Edit Product Route
@admin_blueprint.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@admin_only
def edit_product(product_id):
    product = next((prod for prod in products if prod["id"] == product_id), None)
    if request.method == 'POST':
        product['name'] = request.form['name']
        product['price'] = request.form['price']
        product['description'] = request.form['description']
        product['image_url'] = request.form['image_url']
        product['category'] = request.form['category']
        return redirect(url_for('admin_blueprint.admin_dashboard'))

    return render_template('admin/edit_product.html', product=product)

# Delete Product Route
@admin_blueprint.route('/delete_product/<int:product_id>', methods=['POST'])
@admin_only
def delete_product(product_id):
    global products
    products = [prod for prod in products if prod["id"] != product_id]
    return redirect(url_for('admin_blueprint.admin_dashboard'))
