# app/main/routes.py
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/home')
def home():
    return render_template('homeM.html')


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@main_bp.route('/profile')
def profile():
    return render_template('profile.html')


@main_bp.route('/signup')
def signup():
    return render_template('signup.html')
