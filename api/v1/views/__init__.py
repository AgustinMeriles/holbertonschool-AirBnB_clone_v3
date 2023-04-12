#!/usr/bin/python3
"""Shebang"""
from flask import Blueprint


app_views = Blueprint("app_views", url_prefix="/api/v1")
