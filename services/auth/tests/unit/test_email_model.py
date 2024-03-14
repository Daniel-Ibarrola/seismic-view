import pytest

from ewauth.app import db
from ewauth.models.email import Email


class TestEmailValidation:

    @pytest.mark.usefixtures("in_memory_db")
    def test_email_in_table_is_valid(self):
        email_address = "triton@example.com"
        email = Email(email=email_address)
        db.session.add(email)
        db.session.commit()
        assert Email.is_email_valid(email_address) is True

    @pytest.mark.usefixtures("in_memory_db")
    def test_email_not_in_table_is_invalid(self):
        assert Email.is_email_valid("sanson@example.com") is False
