import os
import logging
import re


def get_api_url() -> str:
    host = os.environ.get("API_HOST", "localhost")
    port = 5000 if host == "localhost" else 80
    return f"http://{host}:{port}"


def get_db_path(filename: str) -> str:
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, filename + ".db")
    return f"sqlite:///{full_path}"


class MissingEnvVariableError(ValueError):
    pass


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
    SQLALCHEMY_DATABASE_URI = ""
    # Logging
    LOGGING_LEVEL = logging.WARNING
    LOG_FILES = False
    # Flask mail config
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "triton@gmail.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "dog")

    @staticmethod
    def init_app(app):
        pass

    @staticmethod
    def valid_emails() -> list[str]:
        return ["triton@example.com", "daniel@example.com", "daniel.ibarrola.sanchez@gmail.com"]


class DevAPIConfig(Configuration):
    """ Configuration used for developing the API and the main voltage module.

        It uses a Postgres database hosted in a docker container. The data in the
        database is expected to be constantly added, deleted or updated.
    """
    NAME = "dev"
    SQLALCHEMY_DATABASE_URI = get_db_path("users-dev")
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
    SQLALCHEMY_DATABASE_URI = f"sqlite:////db/users.db"
    SECRET_KEY = get_env_variable("SECRET_KEY")
    DOMAIN_NAME = get_env_variable("DOMAIN_NAME")

    LOG_FILES = True

    MAIL_USERNAME = get_env_variable('MAIL_USERNAME')
    MAIL_PASSWORD = get_env_variable('MAIL_PASSWORD')

    @staticmethod
    def valid_emails() -> list[str]:
        email_list = []
        pattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        with open(get_emails_file_path()) as fp:
            for line in fp.readlines():
                if not line.startswith("#"):
                    email = line.strip()
                    if re.search(pattern, email):
                        email_list.append(email)
        return email_list


def get_app_config(config_name: str) -> Configuration:
    config = {
        "dev": DevAPIConfig,
        "test": TestSqlLiteConfig,
        "prod": ProdConfig,
    }
    return config[config_name]()
