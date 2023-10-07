from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = 'sqlite:///app.db'
cors = CORS(app, resources={r"/*": {"origins": []}})
jwt = JWTManager(app)

from app.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(db)
Base.metadata.create_all(engine)
session = scoped_session(sessionmaker(autoflush=False, bind=engine))
Base.session = session.query_property()


@app.teardown_appcontext
def shutdown_session(extension=None):
    session.remove()


from app import auth
app.register_blueprint(auth.bp)
