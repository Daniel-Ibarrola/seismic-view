from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from ewauth import CONFIG, db
from ewauth.models.user import User, EmailStatus
from ewauth.api import api, errors, mail

auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme="Bearer")


def _verify_password(email: str, password: str) -> bool:
    if not email or not password:
        return False
    user = User.get_user(email)
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)


def _verify_token(token: str) -> bool:
    user = User.verify_auth_token(token, expiration=CONFIG.TOKEN_EXPIRATION)
    if not user:
        return False
    g.current_user = user
    return True


@auth.verify_password
def verify_password(email: str, password: str) -> bool:
    return _verify_password(email, password)


@token_auth.verify_token
def verify_token(token: str) -> bool:
    return _verify_token(token)


@auth.error_handler
def auth_error():
    return errors.unauthorized("Invalid credentials")


@api.route("/tokens/", methods=["POST"])
@auth.login_required()
def get_token():
    if g.current_user.confirmed:
        return jsonify({
            "token": g.current_user.generate_auth_token(),
            "expiration": CONFIG.TOKEN_EXPIRATION
        })
    return errors.bad_request("unconfirmed account")


@api.route("/new_user/", methods=["POST"])
def add_new_user():
    email, password = request.json["email"], request.json["password"]
    email_valid = User.check_email_status(email)
    if email_valid == EmailStatus.VALID:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        token = user.generate_auth_token()
        mail.send_confirmation_email(user.email, token)
        return jsonify({
            "email": email
        })
    elif email_valid == EmailStatus.IN_USE:
        return errors.bad_request("Email already in use")
    else:
        return errors.unauthorized("Invalid email")


@api.route("/confirm/<token>")
@auth.login_required()
def confirm_account(token):
    if g.current_user.confirmed:
        return jsonify({"confirmed": "User already confirmed"})
    if g.current_user.confirm(token):
        db.session.commit()
        return jsonify({"confirmed": "account confirmed"})
    return errors.bad_request("Invalid or expired link")


@api.route("/confirm")
@auth.login_required()
def resend_confirmation():
    token = g.current_user.generate_auth_token()
    mail.send_confirmation_email(g.current_user.email, token)
    return jsonify({"email": g.current_user.email})


@api.route("/change_password/", methods=["POST"])
@token_auth.login_required()
def change_password():
    old_password = request.json["old"]
    new_password = request.json["new"]
    user = g.current_user
    if not user.verify_password(old_password):
        return errors.unauthorized("Invalid password")
    user.password = new_password
    db.session.add(user)
    db.session.commit()
    return "OK", 201


@api.route("/reset", methods=["POST"])
def request_password_reset():
    email = request.json["email"]
    token = User.reset_password_token(email)
    if token:
        mail.send_reset_password_email(email, token)
        return jsonify({"email": email})
    return errors.not_found("Email is not associated with an account")


@api.route("/reset/<token>", methods=["POST"])
def reset_password(token):
    password = request.json["password"]
    if User.reset_password(token, password):
        db.session.commit()
        return "OK", 201
    return errors.bad_request("Invalid or expired link")
