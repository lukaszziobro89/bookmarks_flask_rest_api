import functools
import os

from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, g, session
from werkzeug.security import check_password_hash, generate_password_hash
from constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, \
    HTTP_401_UNAUTHORIZED, HTTP_200_OK
import validators
from app.database import User, db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, set_refresh_cookies, set_access_cookies
import jwt

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
def register():
    username = request.form['register-username']
    email = request.form['register-email']
    password = request.form['register-password']

    if len(password) < 6:
        flash("Password is too short"), HTTP_400_BAD_REQUEST
        return redirect(url_for('main.home'))

    if len(username) < 3:
        flash("Username is too short"), HTTP_400_BAD_REQUEST
        return redirect(url_for('main.home'))

    if not username.isalnum() or " " in username:
        flash("Username must be alphanumeric and must not contain space"), HTTP_400_BAD_REQUEST
        return redirect(url_for('main.home'))

    if not validators.email(email):
        flash("Not a valid email"), HTTP_400_BAD_REQUEST
        return redirect(url_for('main.home'))

    if User.query.filter_by(email=email).first() is not None:
        flash("Email already taken"), HTTP_409_CONFLICT
        return redirect(url_for('main.home'))

    if User.query.filter_by(username=username).first() is not None:
        flash("Username already exists"), HTTP_409_CONFLICT
        return redirect(url_for('main.home'))

    pwd_hash = generate_password_hash(password)
    user = User(username=username, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return render_template('home.html'), HTTP_201_CREATED

    # return jsonify({
    #     'message': "User created",
    #     'user': {
    #         'username': username, 'email': email
    #     }
    # }), HTTP_201_CREATED


@auth.post("/login")
def login():
    # email = request.json.get('email', '')
    # password = request.json.get('password', '')

    email = request.form['input-email']
    password = request.form['input-password']

    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)
        if is_pass_correct:
            refresh_token = create_refresh_token(identity=user.id)
            access_token = create_access_token(identity=user.id)
            # resp = jsonify({'login': True})
            # resp = redirect(url_for('main.home'))
            resp = redirect(url_for('main.home'), 302)
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            # resp.he

            # return jsonify({
            #     'user': {
            #         'refresh': refresh,
            #         'access': access,
            #         'username': user.username,
            #         'email': user.email
            #     }
            # }), HTTP_200_OK
            return resp#, 200
            # return render_template('home.html')
        # return jsonify(access_token=access)

    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED


@auth.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        'username': user.username,
        'email': user.email
    }), HTTP_200_OK


# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))
#         return view(**kwargs)
#     return wrapped_view


# @auth.before_request
# def load_user():
#     if session["user_id"]:
#         user = User.query.filter_by(id=session["id"]).first()
#     else:
#         user = {"name": "Guest"}
#     g.user = user


# def token_required(f):
#     @functools.wraps(f)
#     def decorator(*args, **kwargs):
#         token = None
#         if 'access' in request.headers:
#             token = request.headers['access']
#
#         if not token:
#             return jsonify({'message': 'a valid token is missing'})
#         try:
#             data = jwt.decode(token, os.environ.get("JWT_SECRET_KEY"))
#             print(data)
#             current_user = User.query.filter_by(id=data['id']).first()
#             print(current_user)
#             # User.query.filter_by(email=email)
#         except:
#             return jsonify({'message': 'token is invalid'})
#
#         return f(current_user, *args, **kwargs)
#
#     return decorator
