from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from werkzeug.security import generate_password_hash
from ewauth.config import DevAPIConfig


def get_users_emails(session: Session):
    results = session.execute(
        text(
            "SELECT email, password_hash, confirmed FROM users "
        ),
    )
    return [(row.email, row.password_hash, row.confirmed) for row in results]


def delete_users(session: Session):
    session.execute(text(
        "DELETE FROM users"
    ))


def insert_user() -> tuple[str, str]:
    engine = create_engine(DevAPIConfig.SQLALCHEMY_DATABASE_URI)
    engine.connect()
    session = sessionmaker(bind=engine)()

    email, password = "triton@example.com", "6MonkeysRLooking^"
    password_hash = generate_password_hash(password)
    session.execute(
        text(
            "INSERT INTO users (email, password_hash, confirmed) VALUES "
            "(:email, :password_hash, :confirmed )"
        ),
        dict(email=email, password_hash=password_hash, confirmed=True)
    )
    session.commit()

    return email, password
