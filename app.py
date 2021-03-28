import base64

from flask import Flask, request, session
from flask_cors import cross_origin
from sqlalchemy import desc
from PIL import Image
from flask_googlemaps import GoogleMaps
import os
import io

from .database import database
from .cli import create_all, drop_all
from .models import User, Item

app = Flask(__name__)
app.secret_key = 'wherethe'
app.config[
    "SQLALCHEMY_DATABASE_URI"] = "sqlite://///Users/vho001/Desktop/ic-hello-world/ic-hello-world-backend/ic-hello-world.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://///home/jyjulianwong/ic-hello-world.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['GOOGLEMAPS_KEY'] = "wherethe"

database.init_app(app)
GoogleMaps(app)

with app.app_context():
    app.cli.add_command(create_all)
    app.cli.add_command(drop_all)


@app.route('/', methods=["GET"])
@cross_origin()
def home():
    # database.session.add(
    #     Item(name="Wallet", contact_email="vincentkcho627@gmail.com", contact_number="9382 8913")
    # )
    # database.session.commit()
    api_return = {"currUsername": "You're not signed in!"}

    if 'username' in session:
        api_return["currUsername"] = session['username']

    return api_return


def save_image(image_path):
    if image_path:
        img = Image.open(image_path)
        if not os.path.exists("images"):
            os.mkdir("images")
        filename = image_path.filename
        filename = filename.split(".")[0]
        filename += ".png"
        img.save(f"images/{filename}", "PNG")


@app.route('/signup', methods=["POST"])
@cross_origin()
def signup():
    api_return = {
        "success": True,
        "error": "An unknown error has occurred."
    }
    json_data = request.form
    try:
        username = json_data["username"]
        password = json_data["password"]

        # checking if the user object exists in the database
        if User.query.filter_by(username=username).first():
            api_return['error'] = "A user with that username already exists."
            raise Exception()

        # adding the user object into the database
        user_object = User(username=username, password=password)
        database.session.add(user_object)
        database.session.commit()

        # signing the user into the current session
        session['username'] = username
    except Exception as e:
        database.session.rollback()
        api_return["success"] = False
    finally:
        database.session.close()
        return api_return


@app.route('/signin', methods=["POST"])
@cross_origin()
def signin():
    api_return = {
        "success": True,
        "error": "An unknown error has occurred."
    }
    json_data = request.form
    try:
        username = json_data["username"]
        password = json_data["password"]

        # checking if the user object exists in the database
        user_object = User.query.filter_by(username=username).first()

        # signing the user into the current session
        if user_object and password == user_object.password:
            session['username'] = username
        else:
            api_return['error'] = "Invalid username or password detected."
            raise Exception()
    except Exception as e:
        api_return["success"] = False
    finally:
        return api_return


@app.route('/signout')
@cross_origin()
def signout():
    session.clear()


@app.route('/upload', methods=["POST"])
@cross_origin()
def upload():
    api_return = {"success": True}
    json_data = request.form
    try:
        # a user needs to be signed in before they can upload
        # if session['username'] is None:
        #     raise Exception("A user must be signed in before they can upload.")

        item_name = json_data["name"]
        contact_email = json_data["contactEmail"]
        contact_number = json_data["contactNumber"]
        last_seen_location = json_data["lastSeenLocation"]
        image_path = request.files.get('image')

        save_image(image_path)
        filename = image_path.filename
        filename = filename.split(".")[0]
        filename += ".png"

        # adding the item object into the database
        item_object = Item(name=item_name, contact_email=contact_email, contact_number=contact_number,
                           last_seen_location=last_seen_location, image_path=filename)
        database.session.add(item_object)
        database.session.commit()
    except Exception as e:
        database.session.rollback()
        api_return["success"] = False
    finally:
        database.session.close()
        return api_return


@app.route('/users', methods=["GET"])
@cross_origin()
def get_users():
    api_return = {"success": True}
    try:
        list_of_users = User.query.order_by(desc(User.username)).all()[:]
        list_of_users = list(map(lambda x: {
            "id": x.id,
            "username": x.username,
            "password": x.password
        }, list_of_users))

        api_return["users"] = list_of_users
    except Exception as e:
        api_return["success"] = False
    finally:
        return api_return


def convert_to_json(x):
    image = Image.open("images/" + x.image_path)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    labelled_image = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    return {
        "id": x.id,
        "name": x.name,
        "contactEmail": x.contact_email,
        "contactNumber": x.contact_number,
        "date": x.date,
        "image": labelled_image,
        "lastSeenLocation": x.last_seen_location
    }


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

        list_of_items = list(map(lambda x: convert_to_json(x), list_of_items))
        api_return["items"] = list_of_items
    except Exception as e:
        api_return["success"] = False
    finally:
        return api_return


@app.route('/search/<keywords>', methods=["GET"])
@cross_origin()
def search_items(keywords):
    api_return = {"success": True}

    try:
        keywords = keywords.replace("+", " ")
        list_of_items = Item.query.order_by(desc(Item.date)).filter(
            any((keyword in Item.name) or (keyword in Item.last_seen_location) for keyword in keywords)).all()[:]

        list_of_items = list(map(lambda x: convert_to_json(x), list_of_items))

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
