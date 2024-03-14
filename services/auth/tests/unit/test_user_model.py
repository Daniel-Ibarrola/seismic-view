import time
import pytest

from ewauth.app import db
from ewauth.config import DevAPIConfig
from ewauth.models import Email
from ewauth.models.email_status import EmailStatus
from ewauth.models.user import User, ValidationError


class TestUserModel:

    password = "6MonkeysRLooking^"

    def test_cannot_get_password(self):
        user = User(email="daniel@example.com", password=self.password)
        with pytest.raises(AttributeError):
            password = user.password

    def test_password_setter(self):
        user = User(email="daniel@example.com", password=self.password)
        assert user.password_hash is not None

    def test_password_verification(self):
        user = User(email="daniel@example.com", password=self.password)
        assert user.verify_password(self.password)

    def test_password_salts_are_random(self):
        user1 = User(email="daniel@example.com", password=self.password)
        user2 = User(email="triton@example.com", password=self.password)
        assert user1.password_hash != user2.password_hash

    @pytest.mark.usefixtures("in_memory_db")
    def test_verify_auth_token(self):
        user_1 = User(email="daniel@example.com", password=self.password)
        db.session.add(user_1)
        db.session.commit()

        token = user_1.generate_auth_token()

        user_2 = User.verify_auth_token(token)
        assert user_1 == user_2

    @pytest.mark.usefixtures("in_memory_db")
    def test_expired_token_doesnt_return_user(self):
        user = User(email="daniel@example.com", password=self.password)
        db.session.add(user)
        db.session.commit()

        token = user.generate_auth_token()
        time.sleep(2)
        user = User.verify_auth_token(token, expiration=1)
        assert user is None

    @pytest.mark.usefixtures("in_memory_db")
    def test_fails_to_confirm_token_of_different_user(self):
        user1 = User(email="daniel@example.com", password=self.password)
        user2 = User(email="triton@example.com", password=self.password)
        db.session.add(user1)
        db.session.add(user2)

        token = user1.generate_auth_token()
        assert not user2.confirm(token)
        assert not user2.confirmed

    @pytest.mark.usefixtures("in_memory_db")
    def test_confirm_user(self):
        user = User(email="daniel@example.com", password=self.password)
        db.session.add(user)
        db.session.commit()
        assert not user.confirmed

        token = user.generate_auth_token()
        assert user.confirm(token)
        assert user.confirmed

    @pytest.mark.usefixtures("in_memory_db")
    def test_no_reset_password_token_for_unregisted_email(self):
        assert not User.reset_password_token("unregistered@example.com")

    @pytest.mark.usefixtures("in_memory_db")
    def test_reset_password_token(self):
        email = "daniel@example.com"
        user = User(email="daniel@example.com", password=self.password)
        db.session.add(user)
        db.session.commit()

        token = User.reset_password_token(email)
        assert len(token) > 0

    @pytest.mark.usefixtures("in_memory_db")
    def test_cannot_reset_password_expired_token(self):
        user = User(email="daniel@example.com", password=self.password)
        db.session.add(user)
        db.session.commit()

        token = user.generate_reset_token()
        time.sleep(2)
        can_reset = User.reset_password(token, "dog", expiration=1)
        assert not can_reset

    @pytest.mark.usefixtures("in_memory_db")
    def test_can_reset_password(self):
        user = User(email="daniel@example.com", password=self.password)
        original_hash = user.password_hash
        db.session.add(user)
        db.session.commit()

        token = user.generate_reset_token()
        can_reset = User.reset_password(token, "dog")
        db.session.commit()
        assert can_reset
        assert user.password_hash != original_hash


class TestUserValidation:

    def test_empty_password_raises_error(self):
        with pytest.raises(ValidationError):
            User(email="daniel@example.com", password="")

    def test_empty_email_raises_error(self):
        with pytest.raises(ValidationError):
            User(email="", password="dog")


class TestEmailValidation:

    @staticmethod
    def add_valid_email(email_address: str):
        email = Email(email=email_address)
        db.session.add(email)
        db.session.commit()

    @pytest.mark.usefixtures("in_memory_db")
    def test_email_in_use(self):
        email_address = "daniel@example.com"

        self.add_valid_email(email_address)

        user = User(email=email_address, password="6MonkeysRLooking^")
        db.session.add(user)
        db.session.commit()

        assert User.check_email_status(email_address) == EmailStatus.IN_USE

    @pytest.mark.usefixtures("in_memory_db")
    def test_email_not_in_list(self):
        assert User.check_email_status("triton@example.com") == EmailStatus.INVALID

    @pytest.mark.usefixtures("in_memory_db")
    def test_valid_email(self):
        email_address = "daniel@example.com"
        self.add_valid_email(email_address)
        assert User.check_email_status(email_address) == EmailStatus.VALID


class TestAdminUser:

    @pytest.mark.usefixtures("in_memory_db")
    def test_add_admin_user(self):
        # Admin is added in app creation
        admin_email = DevAPIConfig.ADMIN_USER
        admin_password = DevAPIConfig.ADMIN_PASSWORD

        user = User.get_user(admin_email)
        assert user is not None

        assert user.verify_password(admin_password)

    @pytest.mark.usefixtures("in_memory_db")
    def test_user_is_admin(self):
        admin_email = DevAPIConfig.ADMIN_USER
        admin = User.get_user(admin_email)
        assert admin.is_admin is True

    @pytest.mark.usefixtures("in_memory_db")
    def test_user_is_not_admin(self):
        user = User(email="daniel@example.com", password="dog123")
        db.session.add(user)
        db.session.commit()

        assert user.is_admin is False
