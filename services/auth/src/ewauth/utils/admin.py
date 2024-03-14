from flask import Flask

from ewauth import CONFIG, db
from ewauth.models import User, Email


def add_admin(app: Flask) -> None:
    """Adds the admin user to the database"""
    with app.app_context():
        admin_email = CONFIG.ADMIN_USER

        if not Email.is_email_valid(admin_email):
            email = Email(email=admin_email)
            db.session.add(email)
            db.session.commit()

        user = User.get_user(admin_email)
        if user is None:
            user = User(email=admin_email, password=CONFIG.ADMIN_PASSWORD, confirmed=True)
            db.session.add(user)
            db.session.commit()
