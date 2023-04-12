#!/usr/bin/python3
"""Shebang"""
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """Function that returns a JSON status"""
    return {'status': 'OK'}
