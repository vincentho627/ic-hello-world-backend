from flask import Flask, request
from flask_cors import cross_origin
from sqlalchemy import desc
from sqlalchemy.orm import Session

from .database import database
from .cli import create_all
from .models import User, Item

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"] = "sqlite://///Users/vho001/Desktop/ic-hello-world/ic-hello-world-backend/ic-hello-world.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

database.init_app(app)

with app.app_context():
    app.cli.add_command(create_all)


@app.route('/')
def home():
    # database.session.add(
    #     Item(name="Wallet", contact_email="vincentkcho627@gmail.com", contact_number="9382 8913")
    # )
    # database.session.commit()
    return "<h1>Success</h1>"


@app.route('/upload', methods=["POST"])
@cross_origin()
def upload():
    api_return = {"success": True}
    json_data = request.get_json()
    print(json_data)
    try:
        item_name = json_data["name"]
        contact_email = json_data["contactEmail"]
        contact_number = json_data["contactNumber"]

        # adding the item object into the database
        item_object = Item(name=item_name, contact_email=contact_email, contact_number=contact_number)
        database.session.add(item_object)
        database.session.commit()
    except Exception as e:
        database.session.rollback()
        api_return["success"] = False
    finally:
        database.session.close()
        return api_return


@app.route('/items/<page_id>', methods=["GET"])
@cross_origin()
def get_items(page_id):
    api_return = {"success": True}
    page_id = int(page_id)
    previous_page_items = (page_id - 1) * 25
    current_page_items = previous_page_items + 25

    try:
        list_of_items = Item.query.order_by(desc(Item.date)).filter(Item.found == 0).all()[
                        previous_page_items:current_page_items]

        print(list_of_items)
        list_of_items = list(map(lambda x: {
            "id": x.id,
            "name": x.name,
            "contactEmail": x.contact_email,
            "contactNumber": x.contact_number,
            "date": x.date
        }, list_of_items))

        api_return["items"] = list_of_items
    except Exception as e:
        api_return["success"] = False
    finally:
        return api_return


@app.route('/found/<item_id>', methods=["GET"])
@cross_origin()
def found_item(item_id):
    api_return = {"success": True}

    try:
        item = Item.query.get(item_id)
        item.found = True
        database.session.commit()
    except Exception as e:
        database.session.rollback()
        api_return["success"] = False
    finally:
        database.session.close()
        return api_return
