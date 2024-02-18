import time
import pytest
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from werkzeug.security import generate_password_hash
from typing import Generator

from ewauth import config, create_app, db
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


def insert_fake_user(session: Session, auth: tuple[str, str], confirmed: bool) -> None:
    """ Insert a user into the database, so we can pass the http auth"""
    email, password = auth
    if email not in get_users_emails(session):
        password_hash = generate_password_hash(password)
        session.execute(
            text(
                    "INSERT INTO users (email, password_hash, confirmed) VALUES "
                    "(:email, :password_hash, :confirmed )"
                 ),
            dict(email=email, password_hash=password_hash, confirmed=confirmed)
        )
        session.commit()


def insert_valid_emails(session: Session):
    emails = ["daniel@example.com", "triton@example.com"]
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
    engine = create_engine(config.DevAPIConfig.SQLALCHEMY_DATABASE_URI)
    session = sessionmaker(bind=engine)()

    credentials = "triton@example.com", "6MonkeysRLooking^"
    insert_valid_emails(session)
    insert_fake_user(session, credentials, True)
    clear_database(session)

    yield session

    clear_database(session)
    session.close()


@pytest.fixture
def client() -> APIClient:
    credentials = "triton@example.com", "6MonkeysRLooking^"
    api_client = APIClient(credentials)
    res = api_client.request_token()
    assert res.ok, res.json()["message"]
    return api_client
