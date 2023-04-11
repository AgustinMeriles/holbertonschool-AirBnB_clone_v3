#!/usr/bin/python3
"""Shebang"""
from models import storage
from api.v1.views import app_views
from flask import Flask
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def destroy(exception):
    storage.close()

if __name__ == "__main__":
    host = getenv(HBNB_API_HOST)
    port = getenv(HBNB_API_PORT)
    app.run(
        host="0.0.0.0" if host is None else host,
        port="5000" if port is None else port,
        threaded=True
    )