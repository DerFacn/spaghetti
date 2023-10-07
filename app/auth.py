from flask import Blueprint, request, make_response
from app.models import User
from app import session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin
from uuid import uuid4
from flask_jwt_extended import create_access_token, create_refresh_token, unset_jwt_cookies, jwt_required, \
    get_jwt_identity


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
@cross_origin()
def register():
    # Collect username and password
    username = request.form.get('username')
    password = request.form.get('password')
    # Validate data
    if not username:
        return {'msg': 'Username is required!'}, 422
    elif not password:
        return {'msg': 'Password is required!'}, 422
    # Check if this user exists
    user = session.query(User).filter_by(username=username).first()
    if user is not None:
        return {'msg': 'User already exists!'}, 409
    # Create new user
    hashed_passwd = generate_password_hash(password)
    user = User(
        uuid=str(uuid4()),
        username=username,
        password=hashed_passwd)
    session.add(user)
    session.commit()
    return {'msg': 'User successfully created!'}, 200


@bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    # Collect data
    username = request.form.get('username')
    password = request.form.get('password')
    # Validate data
    if not username:
        return {'msg': 'Username is required!'}, 422
    elif not password:
        return {'msg': 'Password is required!'}, 422
    # Search user
    user = session.query(User).filter_by(username=username).first()
    if not user:
        return {'msg': 'User with this username don\'t exists'}, 401
    if not check_password_hash(user.password, password):
        return {'msg': 'Wrong password!'}, 401
    # Create tokens for authentication
    access_token = create_access_token(identity=user.uuid)
    refresh_token = create_refresh_token(identity=user.uuid)
    response = make_response('Authorized!', 200)
    response.set_cookie('access_token_cookie', access_token, secure=True, httponly=True, path='/')
    response.set_cookie('refresh_token_cookie', refresh_token, secure=True, httponly=True, path='/auth/refresh')
    # Return successful response with tokens to user
    return response


@bp.route('/refresh', methods=['POST'])
@cross_origin()
@jwt_required()
def refresh():
    # If user authorized it must get user identity
    user_identity = get_jwt_identity()
    # Create new tokens for this user
    access_token = create_access_token(identity=user_identity)
    refresh_token = create_refresh_token(identity=user_identity)
    response = make_response('', 200)
    response.set_cookie('access_token_cookie', access_token, secure=True, httponly=True, path='/')
    response.set_cookie('refresh_token_cookie', refresh_token, secure=True, httponly=True, path='/auth/refresh')
    # And send these refreshed new tokens to user
    return response


@bp.route('/logout')
@cross_origin()
@jwt_required()
def logout():
    response = make_response()
    unset_jwt_cookies(response)
    return response
