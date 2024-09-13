
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify

# Blueprint for user-related routes
user_blueprint = Blueprint('user_blueprint', __name__)

# List of products (Jewish Temples, Supermodels, and external products with direct links)
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

    # External products with direct links
    {"id": 16, "name": "Acer Nitro V Gaming Laptop", "price": 649.99, "description": "Intel Core i5-13420H Processor | NVIDIA GeForce RTX 4050 Laptop GPU | 15.6 FHD IPS 144Hz Display | 8GB DDR5 | 512GB Gen 4 SSD | WiFi 6 | Backlit KB | ANV15-51-51H9", "image_url": "amazon_1.png", "category": "Amazon", "external_link": "https://www.amazon.com/-/he/%D7%92%D7%99%D7%99%D7%9E%D7%99%D7%A0%D7%92-i5-13420H-NVIDIA-GeForce-ANV15-51-51H9/dp/B0CP8D4SM2"},
    {"id": 17, "name": "ASUS ROG Strix G16 (2024)", "price": 1164.99, "description": "16” 16:10 FHD 165Hz Display, NVIDIA® GeForce RTX™ 4060, Intel Core i7-13650HX, 16GB DDR5, 1TB PCIe Gen4 SSD, Wi-Fi 6E, Windows 11", "image_url": "amazon_2.png", "category": "Amazon", "external_link": "https://www.amazon.com/-/he/%D7%9E%D7%97%D7%A9%D7%91-%D7%A0%D7%99%D7%99%D7%93-%D7%92%D7%99%D7%99%D7%9E%D7%99%D7%A0%D7%92-ASUS-Strix/dp/B0CRDCXRK2"},
    {"id": 18, "name": "ACEMAGIC Laptop Computer", "price": 599.99, "description": "AMD Ryzen 7 5700U Gaming Laptop 16GB DDR4 512GB M.2 2280 NVMe SSD Windows Laptop Office Laptops Home Laptops Windows11 16.1-inch IPS FHD WIFI6 BT5.2 HDMI Type-C USB3.2", "image_url": "amazon_3.png", "category": "Amazon", "external_link": "https://www.amazon.com/-/he/ACEMAGIC-%D7%92%D7%99%D7%99%D7%9E%D7%99%D7%A0%D7%92-Windows-%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D-%D7%A0%D7%99%D7%99%D7%93%D7%99%D7%9D/dp/B0DBQR1PBQ"},
    {"id": 19, "name": "Acer Nitro 16 Gaming Laptop", "price": 957.47, "description": "AMD Ryzen 7 7840HS OctaCore CPU | NVIDIA GeForce RTX 4060 Laptop GPU | 16 WUXGA 165Hz IPS Display | 16GB DDR5 | 1TB Gen 4 SSD | WiFi 6E | RGB Backlit KB", "image_url": "amazon_4.png", "category": "Amazon", "external_link": "https://www.amazon.com/-/he/%D7%92%D7%99%D7%99%D7%9E%D7%99%D7%A0%D7%92-7840HS-OctaCore-GeForce-backlit/dp/B0CY3SS4VL"},
    {"id": 20, "name": "MSI Raider GE68HX", "price": 2649.99, "description": "144Hz MiniLED UHD+ Gaming Laptop: Intel Core i9-14900HX, NVIDIA Geforce RTX 4080, 64GB DDR5, 2TB NVMe SSD, Thunderbolt 4, Cooler Boost 5, Win 11 Home: Black 14VHG-286US", "image_url": "amazon_5.png", "category": "Amazon", "external_link": "https://www.amazon.com/-/he/Raider-GE68HX-144Hz-MiniLED-%D7%9C%D7%92%D7%99%D7%99%D7%9E%D7%99%D7%A0%D7%92/dp/B0CQBHZMSB"},

    {"id": 21, "name": "iPhone 15 Pro Max", "price": 1602.80, "description": "A3108 5G Smartphone 6.7'' Super Retina XDR Display IP68 Waterproof Dual SIM 1290x2796", "image_url": "aliexpress_1.png", "category": "AliExpress", "external_link": "https://he.aliexpress.com/item/1005007422390739.html"},
    {"id": 22, "name": "iPhone 14 Pro Max", "price": 1387.09, "description": "5G Mobile Phone Face ID 6GB RAM 128GB/256GB/512GB ROM eSIM NFC 6.7'' IOS Hexa Core SmartPhone", "image_url": "aliexpress_2.png", "category": "AliExpress", "external_link": "https://he.aliexpress.com/item/1005007007912420.html"},
    {"id": 23, "name": "Samsung Galaxy S24 Ultra", "price": 1906.98, "description": " 5G Smartphone Snapdragon 8 Gen 3 200MP Camera", "image_url": "aliexpress_3.png", "category": "AliExpress", "external_link": "https://www.aliexpress.com/item/1005007509996540.html"},
    {"id": 24, "name": "Google Pixel 8", "price": 1899.00, "description": "5G Global Version Tensor G3 Smartphone 50MP 120HZ ESIM 12+128/12+256GB IP68 dust/water resistant AI camera", "image_url": "aliexpress_4.png", "category": "AliExpress", "external_link": "https://www.aliexpress.com/item/1005006151200099.html"},
    {"id": 25, "name": "HUAWEI-Pura 70 Pro", "price": 1300.00, "description": "HarmonyOS 4.2,6.8 inch,12GB RAM 1TB ROM,50MP Camera,5G Network,5050mAh Battrey,Mobile phone", "image_url": "aliexpress_5.png", "category": "AliExpress", "external_link": "https://www.aliexpress.com/item/1005006860529467.html"},

    {"id": 26, "name": "Surfer Girl Necklace", "price": 23.12, "description": "Initial Necklace, Waterproof Beach Jewelry, Women Jewels, Non-tarnish Accessory, Adjustable Length 36+5cm, Boho", "image_url": "etsy_1.png", "category": "Etsy", "external_link": "https://www.etsy.com/il-en/listing/1567197890/surfer-girl-necklace-initial-necklace"},
    {"id": 27, "name": "Teal Imperial Jasper", "price": 19.97, "description": "Aquamarine Jade, Gold Accents, Gold Sea Turtle, Gemstone Bracelet, Beaded Bracelet, Mala Bracelet, Perfect Gift", "image_url": "etsy_2.png", "category": "Etsy", "external_link": "https://www.etsy.com/il-en/listing/1167539363/teal-imperial-jasper-aquamarine-jade"},
    {"id": 28, "name": "Natural Crystals Stretchy Chip Bracelets", "price": 2.04, "description": ",Bracelet For Women,Healing Crystals Chip Bracelet,For Gift Crystals Bracelets.Gemstone Bracelets", "image_url": "etsy_3.png", "category": "Etsy", "external_link": "https://www.etsy.com/il-en/listing/1513456244/natural-crystals-stretchy-chip"},
    {"id": 29, "name": "Raw Moonstone Gold Ring", "price": 19.81, "description": "14K Gold Plated Ring, Handmade Ring, Blue Fire Moonstone, Rough Stone Jewelry, July Birthstone, Gift For Women", "image_url": "etsy_4.png", "category": "Etsy", "external_link": "https://www.etsy.com/il-en/listing/1472084572/raw-moonstone-gold-ring-14k-gold-plated"},
    {"id": 30, "name": "Labradorite Gemstone Ring", "price": 28.75, "description": "Handmade 925 Sterling Silver Bracelet 925 Stamped Gemstone Labradorite Bracelet Labradorite Bracelet Gift For Love", "image_url": "etsy_5.png", "category": "Etsy", "external_link": "https://www.etsy.com/il-en/listing/1442857923/labradorite-gemstone-handmade-925"},

    {"id": 31, "name": "Mainstays 5-Piece Blue Floral Comforter", "price": 56.00, "description": "Mainstays 5-Piece Blue Floral Comforter Set, King", "image_url": "walmart_1.png", "category": "Walmart", "external_link": "https://www.walmart.com/ip/Mainstays-5-Piece-Blue-Floral-Comforter-Set-King/2853924944"},
    {"id": 32, "name": "Better Homes & Gardens Mira Swivel Chair", "price": 248.00, "description": "Better Homes & Gardens Mira Swivel Chair, Linen", "image_url": "walmart_2.png", "category": "Walmart", "external_link": "https://www.walmart.com/ip/Better-Homes-Gardens-Mira-Swivel-Chair-Linen/5161950924"},
    {"id": 33, "name": "Springwood 4-Drawer Dresser", "price": 229.00, "description": "Better Homes & Gardens Springwood Caning 4-Drawer Dresser, Charcoal Finish", "image_url": "walmart_3.png", "category": "Walmart", "external_link": "https://www.walmart.com/ip/Better-Homes-Gardens-Springwood-Caning-4-Drawer-Dresser-Charcoal-Finish/3350243326"},
    {"id": 34, "name": "Homall L-Shaped Gaming Desk", "price": 63.99, "description": "Homall L-Shaped Gaming Desk 47 Inches Corner Office Desk with Removable Monitor Riser, Black", "image_url": "walmart_4.png", "category": "Walmart", "external_link": "https://www.walmart.com/ip/Homall-L-Shaped-Gaming-Desk-47-Inches-Corner-Office-Desk-with-Removable-Monitor-Riser-Black/1362962707"},
    {"id": 35, "name": "Mr. Kate Roxanne Platform Bed", "price": 269.98, "description": "Mr. Kate Roxanne Metal Platform Bed Frame with Cane Headboard, Queen, Black", "image_url": "walmart_5.png", "category": "Walmart", "external_link": "https://www.walmart.com/ip/Mr-Kate-Roxanne-Metal-Platform-Bed-Frame-with-Cane-Headboard-Queen-Black/5214368376"}
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

    # Filter products by name and category (no longer by description)
    filtered_products = [product for product in products if search_query in product['name'].lower()]

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
        if "external_link" in product:
            return redirect(product['external_link'])  # Redirect to external link for external products
        return render_template('product_detail.html', product=product)
    else:
        return "Product not found", 404

# Cart route
@user_blueprint.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)  # Calculate total price
    return render_template('cart.html', cart_items=cart_items, total=total)

# Add to Cart route (AJAX-friendly, no redirect to cart page)
@user_blueprint.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart_route(product_id):
    cart = session.get('cart', [])
    product = next((prod for prod in products if prod["id"] == product_id), None)
    if product:
        cart.append(product)
        session['cart'] = cart
    return jsonify(success=True)  # Return JSON response for AJAX handling

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
