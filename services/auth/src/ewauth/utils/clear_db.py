from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from ewauth.config import DevAPIConfig


def clear_database() -> None:
    engine = create_engine(DevAPIConfig.SQLALCHEMY_DATABASE_URI)
    engine.connect()
    session = sessionmaker(bind=engine)()

    # Clear database after running tests
    session.execute(text("DELETE FROM users"))
    session.commit()
    session.close()
