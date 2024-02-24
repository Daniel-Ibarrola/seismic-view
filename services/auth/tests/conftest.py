import time
import pytest
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from ewauth import config, create_app, db
from ewauth.utils import add_admin
from ewauth.services.api_client import APIClient


@pytest.fixture
def wait_for_api() -> None:
    start = time.time()
    url = config.get_api_url()
    while time.time() - start < 10:
        try:
            requests.get(url)
            return
        except requests.ConnectionError:
            continue

    pytest.fail("Could not connect to API")


def create_app_and_db(config_name: str):
    app = create_app(config.get_app_config(config_name))
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    add_admin(app)
    return app_context


def tear_down(app_context) -> None:
    db.session.remove()
    db.drop_all()
    app_context.pop()


@pytest.fixture
def in_memory_db() -> None:
    """ In memory db for unit testing.
    """
    app_context = create_app_and_db("test")
    yield
    tear_down(app_context)


def get_users_emails(session: Session):
    results = session.execute(
        text(
            "SELECT email FROM users "
        ),
    )
    return results.scalars().all()


def get_emails(session: Session):
    results = session.execute(
        text(
            "SELECT email FROM emails "
        ),
    )
    return results.scalars().all()


def insert_valid_emails(session: Session):
    emails = ["daniel@example.com"]
    valid_emails = get_emails(session)

    for email in emails:
        if email not in valid_emails:
            session.execute(
                text(
                    "INSERT INTO emails (email) VALUES "
                    "(:email)"
                ),
                dict(email=email)
            )
            session.commit()


def clear_database(session: Session) -> None:
    session.execute(
        text("DELETE FROM users WHERE email = :email"),
        dict(email="daniel@example.com")
    )
    session.commit()


@pytest.fixture
def sqlite_session() -> Generator[Session, None, None]:
    dev_config = config.DevAPIConfig

    engine = create_engine(dev_config.SQLALCHEMY_DATABASE_URI)
    session = sessionmaker(bind=engine)()

    insert_valid_emails(session)
    clear_database(session)

    yield session

    clear_database(session)
    session.close()


@pytest.fixture
def client() -> APIClient:
    """ Returns a client with the credentials of the admin user.
    """
    dev_config = config.DevAPIConfig
    credentials = dev_config.ADMIN_USER, dev_config.ADMIN_PASSWORD
    api_client = APIClient(credentials)
    res = api_client.request_token()
    assert res.ok, res.json()["message"]
    return api_client
