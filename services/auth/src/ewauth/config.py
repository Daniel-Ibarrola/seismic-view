import os
import logging


def get_env_variable(name: str) -> str:
    """ Check that an environment variable is set in production mode.
    """
    config = os.environ.get("CONFIG", "dev")
    if "prod" in config:
        value = os.environ.get(name, None)
        if value is None:
            raise MissingEnvVariableError(
                f"The env variable {name} is necessary to run the app"
            )
        return value
    return ""


def get_api_url() -> str:
    host = os.environ.get("API_HOST", "localhost")
    port = 5000 if host == "localhost" else 80
    return f"http://{host}:{port}"


def get_dev_postgres_uri(host: str = "localhost") -> str:
    password = os.environ.get("DB_PASSWORD", "abc123")
    port = os.environ.get("DB_PORT", 54321)
    user = os.environ.get("DB_USER", "ewauth")
    db_name = user
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_postgres_uri() -> str:
    """ Get the postgres uri for the production database. """
    host = get_env_variable("DB_HOST")
    user = get_env_variable("DB_USER")
    password = get_env_variable("DB_PASSWORD")
    port = get_env_variable("DB_PORT")
    db_name = get_env_variable("DB_NAME")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


class MissingEnvVariableError(ValueError):
    pass


def get_emails_file_path() -> str:
    """ Returns the path to the valid emails file.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "emails.txt")


class Configuration:
    NAME = ""
    DOMAIN_NAME = "localhost:5173"
    # Flask Configuration
    DEBUG = True
    SECRET_KEY = "SuperSecretKey"
    TOKEN_EXPIRATION = None
    TESTING = True
    # SQL alchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_dev_postgres_uri(
        host=os.environ.get("DB_HOST", "localhost")
    )
    # Logging
    LOGGING_LEVEL = logging.WARNING
    LOG_FILES = False
    # Flask mail config
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "triton@gmail.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "dog")
    # Admin
    ADMIN_USER = os.environ.get("ADMIN_USER", "admin@example.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "dog123")

    @staticmethod
    def init_app(app):
        pass


class DevAPIConfig(Configuration):
    """ Configuration used for developing the API and the main voltage module.

        It uses a Postgres database hosted in a docker container. The data in the
        database is expected to be constantly added, deleted or updated.
    """
    NAME = "dev"
    LOGGING_LEVEL = logging.DEBUG


class TestSqlLiteConfig(Configuration):
    """ Configuration used for unit testing with an in-memory database
    """
    NAME = "dev"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    LOGGING_LEVEL = logging.DEBUG


class ProdConfig(Configuration):
    """ Configuration used for production.

        The database user and password should be passed as environment
        variables.
    """
    NAME = "prod"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = get_postgres_uri()
    SECRET_KEY = get_env_variable("SECRET_KEY")
    DOMAIN_NAME = get_env_variable("DOMAIN_NAME")

    LOG_FILES = True

    MAIL_USERNAME = get_env_variable('MAIL_USERNAME')
    MAIL_PASSWORD = get_env_variable('MAIL_PASSWORD')

    ADMIN_USER = get_env_variable("ADMIN_USER")
    ADMIN_PASSWORD = get_env_variable("ADMIN_PASSWORD")


def get_app_config(config_name: str) -> Configuration:
    config = {
        "dev": DevAPIConfig,
        "test": TestSqlLiteConfig,
        "prod": ProdConfig,
    }
    return config[config_name]()
