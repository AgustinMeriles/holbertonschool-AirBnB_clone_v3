#!/usr/bin/python3
"""Shebang"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    """Function that returns a JSON status"""
    return jsonify({"status": "OK"})
