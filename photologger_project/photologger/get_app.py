from flask import Flask, jsonify
import os


def create_app(photo_path):
    app = Flask(__name__,
                static_url_path='/photos',
                static_folder=photo_path)

    @app.route('/')
    def root():
        return jsonify(sorted(os.listdir(photo_path)))

    return app
