import click
from flask.cli import with_appcontext

from .database import database


@click.command("create_all", help="Create all tables in the app's database")
@with_appcontext
def create_all():
    database.create_all()
