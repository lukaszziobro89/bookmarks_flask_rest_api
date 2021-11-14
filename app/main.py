from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

main = Blueprint("main", __name__, url_prefix="/api/v1/")


@main.route('/home')
def welcome():
    return render_template('welcome.html')


@main.route('/')
@jwt_required(refresh=True)
def home():
    return render_template('home.html')


@main.route('/register-user')
def register_user():
    return render_template('register.html')


@main.route('/login')
def login():
    return render_template('login.html')

