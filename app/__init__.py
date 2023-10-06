from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
db = 'sqlite:///app.db'
cors = CORS(app, resources={r"/*": {"origins": []}})

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
