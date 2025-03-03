#!/usr/bin/python3
"""File appy.py"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def destroy(exception):
    """Function that closes the API"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if getenv("HBNB_API_HOST") is None:
        host = "0.0.0.0"
    else:
        host = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT") is None:
        port = 5000
    else:
        port = getenv("HBNB_API_PORT")
    app.run(host=host, port=port, threaded=True)
