import getpass
import time

import click

from ewauth import CONFIG, create_app, db
from ewauth.models import Email, User
from ewauth.config import DevAPIConfig
from ewauth.utils import add_admin, clear_database, wait_for_postgres


app = create_app(CONFIG)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


@app.route("/")
def index():
    return "OK", 200


def cli_authenticate() -> bool:
    auth_email = input("Enter your email: ")
    auth_password = getpass.getpass("Enter your password: ")
    user = User.get_user(auth_email)
    return user is not None and user.verify_password(auth_password)


@app.cli.command("wait-for-db")
def wait_for_db():
    """ Wait for the database to start. """
    postgres_uri = CONFIG.SQLALCHEMY_DATABASE_URI
    if "dev" in CONFIG.NAME:
        print(f"Attempting to connect to database in {postgres_uri}...")
    else:
        print(f"Attempting to connect to database...")
    wait_for_postgres(postgres_uri)
    time.sleep(0.5)


@app.cli.command("add-email")
@click.argument("email")
def add_email(email: str):
    """ Add a new email to the valid emails list.

        Requires authentication.
    """
    pass


@app.cli.command("add-user")
@click.argument("email")
@click.argument("password")
def add_user(email: str, password: str):
    """ Add a new user to the database.

        Requires authentication.
    """
    if cli_authenticate():
        if User.check_email_status(email, False) == Email.VALID:
            new_user = User(email=email, password=password, confirmed=True)
            db.session.add(new_user)
            db.session.commit()
            print(f"Added new user with email {email}")
        else:
            print(f"User with given email already exists")
    else:
        print("Invalid email or password")


@app.cli.command("update-password")
@click.argument("email")
@click.argument("new_password")
def update_password(email: str, new_password: str):
    """ Update the password of a user in the database.

        Requires authentication
    """
    if cli_authenticate():
        user = User.get_user(email)
        if not user:
            print(f"There is no user with email {email}")
        else:
            user.password = new_password
            db.session.add(user)
            db.session.commit()
            print("Updated password")
    else:
        print("Invalid email or password")


@app.cli.command("remove-user")
@click.argument("email")
def remove_user(email: str):
    """ Remove a user from the database

        Requires authentication
    """
    if cli_authenticate():
        user = User.get_user(email)
        if not user:
            print(f"There is no user with email {email}")
        else:
            db.session.delete(user)
            db.session.commit()
            print("Removed user")
    else:
        print("Invalid email or password")


@app.cli.command("list-users")
def list_users():
    if cli_authenticate():
        users = db.session.execute(db.select(User)).scalars()
        print("\nUsers:\n")
        for user in users:
            print(user.email)
    else:
        print("Invalid email or password")


@app.cli.command("clear-db")
def clear_db():
    """ Clears the database if in development mode
    """
    if isinstance(CONFIG, DevAPIConfig):
        clear_database()
        print("Database cleared")
    raise ValueError("Cannot clear database in production mode")


@app.cli.command("insert-admin")
def insert_admin():
    """ Inserts a user that can be used to authenticate.

        Only use in development mode.
    """
    add_admin(app)
    print("Inserted admin user")
