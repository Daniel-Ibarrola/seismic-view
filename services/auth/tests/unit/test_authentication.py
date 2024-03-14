import pytest
from ewauth import db
from ewauth.models.user import User
from ewauth.api.authentication import _verify_password, _verify_token


class TestVerifyPassword:

    @staticmethod
    def add_user():
        email = "daniel@example.com"
        password = "6MonkeysRLooking^"
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return email, password

    def test_no_email_or_no_password(self):
        assert not _verify_password("", "password")
        assert not _verify_password("email@example.com", "")

    @pytest.mark.usefixtures("in_memory_db")
    def test_email_not_in_db(self):
        self.add_user()
        assert not _verify_password("email@example.com", "dog")

    @pytest.mark.usefixtures("in_memory_db")
    def test_incorrect_password(self):
        email, _ = self.add_user()
        assert not _verify_password(email, "dog")

    @pytest.mark.usefixtures("in_memory_db")
    def test_correct_password_and_email(self):
        email, password = self.add_user()
        assert _verify_password(email, password)


class TestVerifyToken:

    @staticmethod
    def add_user():
        user = User(email="email@example.com", password="6MonkeysRLooking^")
        db.session.add(user)
        db.session.commit()
        return user

    @pytest.mark.usefixtures("in_memory_db")
    def test_invalid_token(self):
        user = self.add_user()
        user.generate_auth_token()
        assert not _verify_token("invalidtoken")

    @pytest.mark.usefixtures("in_memory_db")
    def test_valid_token(self):
        user = self.add_user()
        token = user.generate_auth_token()
        assert _verify_token(token)
