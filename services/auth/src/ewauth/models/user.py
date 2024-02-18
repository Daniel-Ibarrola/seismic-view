import re
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired, BadSignature
from typing import Union, Optional
from werkzeug.security import generate_password_hash, check_password_hash

from ewauth import CONFIG, db
from ewauth.models.email import Email
from ewauth.models.email_status import EmailStatus


class ValidationError(ValueError):
    pass


class EmailValidationError(ValidationError):
    pass


class PasswordValidationError(ValidationError):
    pass


class User(db.Model):
    __tablename__ = "users"
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    email: db.Mapped[str] = db.mapped_column(db.String(64), unique=True, index=True)
    password_hash: db.Mapped[str] = db.mapped_column(db.String(128))
    confirmed: db.Mapped[bool] = db.mapped_column(default=False)

    def __init__(self, **kwargs):
        self.validate_email(kwargs.get("email"))
        self.validate_password(kwargs.get("password"))
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError("Cannot get password")

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def validate_email(email: str) -> None:
        """ Validate if the given string is an email. """
        pattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if not re.search(pattern, email):
            raise EmailValidationError("Invalid email")

    @staticmethod
    def validate_password(password: str) -> None:
        if len(password) == 0:
            raise PasswordValidationError("Invalid password")

    @staticmethod
    def _get_serializer() -> URLSafeTimedSerializer:
        return URLSafeTimedSerializer(CONFIG.SECRET_KEY, signer_kwargs={"sep": b"$"})

    def generate_auth_token(self) -> Union[bytes, str]:
        serializer = self._get_serializer()
        return serializer.dumps({"confirm": self.id})

    def generate_reset_token(self) -> Union[bytes, str]:
        serializer = self._get_serializer()
        return serializer.dumps({"reset": self.id})

    @staticmethod
    def _verify_token(token: Union[bytes, str],
                      msg: str,
                      expiration: Union[int, None] = 3600) -> Union["User", None]:
        serializer = User._get_serializer()
        try:
            data = serializer.loads(token, max_age=expiration)
        except (SignatureExpired, BadSignature):
            return
        user_id = data[msg]
        if user_id is None:
            return
        return db.session.get(User, data[msg])

    @staticmethod
    def verify_auth_token(token: Union[bytes, str],
                          expiration: Union[int, None] = 3600) -> Union["User", None]:
        return User._verify_token(token, "confirm", expiration)

    @staticmethod
    def check_email_status(email: str, check_valid_emails: bool = True) -> EmailStatus:
        """ Check if the given email is valid and a new user can be
            created with it.
        """
        if check_valid_emails and not Email.is_email_valid(email):
            return EmailStatus.INVALID

        result = db.session.execute(
            db.select(User).filter_by(email=email)
        ).scalar_one_or_none()
        if result is not None:
            return EmailStatus.IN_USE

        return EmailStatus.VALID

    def confirm(self, token: Union[bytes, str]) -> bool:
        user = self.verify_auth_token(token)
        if user is not None and user.id == self.id:
            self.confirmed = True
            db.session.add(self)
            return True
        return False

    @staticmethod
    def reset_password_token(email: str) -> Union[bytes, str]:
        user = db.session.execute(
            db.select(User).filter_by(email=email)
        ).scalar_one_or_none()
        if user is not None:
            return user.generate_reset_token()
        return ""

    @staticmethod
    def reset_password(
            token: Union[bytes, str],
            new_password: str,
            expiration: int = 3600) -> bool:
        user = User._verify_token(token, "reset", expiration)
        if user is not None:
            user.password = new_password
            db.session.add(user)
            return True
        return False

    @staticmethod
    def get_user(email: str) -> Optional["User"]:
        """ Get the user with given email if it exists.
        """
        return db.session.execute(
            db.select(User).filter_by(email=email)
        ).scalar_one_or_none()
