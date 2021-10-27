from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# from auth import token_required
from database import User

main = Blueprint("main", __name__, url_prefix="/api/v1/bookmarks")


@main.route('/home')
def home():
    inp = request.form.get('SOME_INPUT')
    todo_item = request.form.get('add-todo')
    # print(request.args)
    # print(todo_item)
    # print(inp)
    return render_template('home.html')


@main.route('/register-user')
def register_user():
    return render_template('register.html')


@main.route('/login')
def login():
    return render_template('login.html')


@main.route('/handle_data', methods=['GET'])
@jwt_required()
def handle_data():
    user = get_jwt_identity()
    # current_user_id = get_jwt_identity()
    # user = User.filter.get(current_user_id)
    return jsonify({'user': user})


@main.post('/add_todo')
def add_todo():
    # todo_item = request.form['add-todo']
    email = request.form['register-email']
    password = request.form['input-password']
    print(email)
    print(password)
    return jsonify({'s': 'x'})
