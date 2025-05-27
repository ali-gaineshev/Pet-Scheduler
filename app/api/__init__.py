# app/api/__init__.py
from flask import Blueprint
from .task_routes import task_bp
from .family_routes import family_bp
from .person_routes import person_bp
