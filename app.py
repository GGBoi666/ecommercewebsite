from flask import Flask
from routes.user_routes import user_blueprint
from routes.admin_routes import admin_blueprint
from routes.gambling_routes import gambling_blueprint
from routes.poker_routes import poker_blueprint

app = Flask(__name__, static_url_path='/static')  # Ensure the static folder is set
app.secret_key = 'your_secret_key'

# Register blueprints
app.register_blueprint(user_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(gambling_blueprint, url_prefix='/gambling')
app.register_blueprint(poker_blueprint, url_prefix='/poker')

if __name__ == '__main__':
    app.run(debug=True)
