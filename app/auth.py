from flask import Blueprint, request, jsonify, flash, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_200_OK
import validators
from app.database import User, db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, \
    set_refresh_cookies, set_access_cookies, unset_jwt_cookies

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
def register():
    username = request.form['register-username']
    email = request.form['register-email']
    password = request.form['register-password']

    if len(password) < 6:
        flash("Password is too short", 'error'), HTTP_400_BAD_REQUEST
        return redirect(url_for('main.register_user'))

    if len(username) < 3:
        flash("Username is too short - need to contains at least 3 characters", 'error'), HTTP_400_BAD_REQUEST
        return redirect(url_for('main.register_user'))

    if not username.isalnum() or " " in username:
        flash("Username must be alphanumeric and must not contain space", 'error'), HTTP_400_BAD_REQUEST
        return redirect(url_for('main.register_user'))

    if not validators.email(email):
        flash("Not a valid email", 'error'), HTTP_400_BAD_REQUEST
        return redirect(url_for('main.register_user'))

    if User.query.filter_by(email=email).first() is not None:
        flash("Email already taken", 'error'), HTTP_409_CONFLICT
        return redirect(url_for('main.register_user'))

    if User.query.filter_by(username=username).first() is not None:
        flash("Username already exists", 'error'), HTTP_409_CONFLICT
        return redirect(url_for('main.register_user'))

    pwd_hash = generate_password_hash(password)
    user = User(username=username, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    refresh_token = create_refresh_token(identity=user.id)
    access_token = create_access_token(identity=user.id)
    resp = redirect(url_for('main.home'), 302)
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp


@auth.post("/login")
def login():

    email = request.form['input-email']
    password = request.form['input-password']

    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)
        if is_pass_correct:
            refresh_token = create_refresh_token(identity=user.id)
            access_token = create_access_token(identity=user.id)
            resp = redirect(url_for('main.home'), 302)
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp

    flash("Wrong credentials", 'error'), HTTP_400_BAD_REQUEST
    return redirect(url_for('main.home'))


@auth.route("/logout")
def logout():
    resp = redirect(url_for('main.welcome'), 302)
    unset_jwt_cookies(resp)
    return resp


@auth.get("/me")
@jwt_required(refresh=True)
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    # TODO: add new page with render_template instead of jsonify
    return jsonify({
        'username': user.username,
        'email': user.email
    }), HTTP_200_OK


def log_required():
    flash("You have to be logged in to access this page.", 'warning')
    return redirect(url_for('main.login'))
