from flask import Blueprint, request
from app.models import User
from app import session
from werkzeug.security import generate_password_hash


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    # Collect username and password
    username = request.form['username']
    password = request.form['password']
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
