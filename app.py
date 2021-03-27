from flask import Flask
from .database import database
from . import blueprints
from .cli import create_all
from .models import User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://///Users/vho001/Desktop/ic-hello-world/ic-hello-world-backend/ic-hello-world.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

database.init_app(app)

app.register_blueprint(blueprints.upload)

with app.app_context():
    app.cli.add_command(create_all)


@app.route('/')
def home():
    database.session.add(
        User(name="Vincent", email="vincentkcho627@gmail.com")
    )
    database.session.commit()
    return "<h1>Success</h1>"
