from flask import Flask
from .database import database

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://///Users/vho001/Desktop/ic-hello-world/ic-hello-world-backend.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

database.init_app(app)


@app.route('/')
def home():
    pass
