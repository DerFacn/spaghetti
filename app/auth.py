from flask import Blueprint, request
from app.models import User
from app import session
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
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
    user = User(username=username, password=hashed_passwd)
    session.add(user)
    session.commit()
    return {'msg': 'User successfully created!'}, 200


@bp.route('/login', methods=['POST'])
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
    return {'msg': 'Authorised!'}, 200
