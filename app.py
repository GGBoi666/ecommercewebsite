from flask import Flask
from routes.user_routes import user_blueprint
from routes.admin_routes import admin_blueprint

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set your secret key for session management

# Register blueprints
app.register_blueprint(user_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)
