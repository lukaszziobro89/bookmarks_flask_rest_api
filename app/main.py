from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

main = Blueprint("main", __name__, url_prefix="/api/v1/bookmarks")


@main.route('/home')
def welcome():
    return render_template('welcome.html')


@main.route('/')
def home():
    return render_template('home.html')


@main.route('/register-user')
def register_user():
    return render_template('register.html')


@main.route('/login')
def login():
    return render_template('login.html')


@main.route('/handle_data', methods=['GET'])
@jwt_required(refresh=True)
def handle_data():
    user = get_jwt_identity()
    return jsonify({'user': user})


@main.route('/exp', methods=['GET'])
@jwt_required(refresh=True)
def exp():
    return jsonify({'user': "IAM"})


@main.post('/add_todo')
def add_todo():
    email = request.form['register-email']
    password = request.form['input-password']
    return jsonify({'s': 'x'})
