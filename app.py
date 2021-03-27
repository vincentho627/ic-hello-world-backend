from flask import Flask, request
from flask_cors import cross_origin
from sqlalchemy import desc
from sqlalchemy.orm import Session

from .database import database
from .cli import create_all
from .models import User, Item

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://///Users/vho001/Desktop/ic-hello-world/ic-hello-world-backend/ic-hello-world.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

database.init_app(app)

with app.app_context():
    app.cli.add_command(create_all)


@app.route('/')
def home():
    # database.session.add(
    #     User(name="Vincent", email="vincentkcho627@gmail.com")
    # )
    # database.session.commit()
    return "<h1>Success</h1>"


@app.route('/upload', methods=["POST"])
@cross_origin()
def upload():
    api_return = {"success": True}
    session = Session()

    try:
        json_data = request.get_json()
        item_name = json_data["name"]
        contact_email = json_data["contact_email"]
        contact_number = json_data["contact_number"]

        # adding the item object into the database
        item_object = Item(name=item_name, contact_email=contact_email, contact_number=contact_number)
        item_object.add_to_session(session)
        session.commit()
    except Exception as e:
        session.rollback()
        api_return["success"] = False
    finally:
        session.close()
        return api_return


@app.route('/items/<page_id>', methods=["GET"])
def get_items(page_id):
    api_return = {"success": True}
    previous_page_items = (page_id - 1) * 25
    current_page_items = previous_page_items + 25

    try:
        list_of_items = Item.query.order_by(desc(Item.date)).filter()[previous_page_items:current_page_items].all()
        api_return["items"] = list_of_items
    except Exception as e:
        api_return["success"] = False
    finally:
        return api_return


@app.route('/found/<item_id>', methods=["POST"])
@cross_origin()
def found_item(item_id):
    api_return = {"success": True}
    session = Session()

    try:
        session.query(Item).get(item_id).update({Item.found: True}, synchronize_session=False)
        session.commit()
    except Exception as e:
        session.rollback()
        api_return["success"] = False
    finally:
        session.close()
        return api_return
