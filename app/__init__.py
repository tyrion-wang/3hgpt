from flask import Flask, jsonify

from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here

    # Register blueprints here

    @app.route('/')
    def index():
        return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app