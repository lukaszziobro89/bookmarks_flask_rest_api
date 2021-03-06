from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

main = Blueprint("main", __name__)


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

