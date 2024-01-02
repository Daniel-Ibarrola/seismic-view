import pytest
from ewauth.services.api_client import APIClient


class TestRegister:
    @pytest.mark.usefixtures("sqlite_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_fails_to_register_an_invalid_email(self, client):
        res = client.register_user("invalid-mail@example.com", "dog")
        assert res.status_code == 401
        contents = res.json()
        assert contents["error"] == "unauthorized"
        assert contents["message"].lower() == "invalid email"

    @pytest.mark.usefixtures("sqlite_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_fails_to_register_an_email_already_in_db(self, client):
        res = client.register_user(*client.credentials)
        assert res.status_code == 400
        contents = res.json()
        assert contents["error"] == "bad request"
        assert contents["message"].lower() == "email already in use"

    @pytest.mark.usefixtures("sqlite_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_registering_new_user(self, client):
        res = client.register_user("daniel@example.com", "6MonkeysRLooking^")
        assert res.ok
        contents = res.json()
        assert contents["email"] == "daniel@example.com"


class TestConfirmUser:

    @pytest.mark.usefixtures("sqlite_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_unconfirmed_user_cannot_get_token(self, client):
        credentials = "daniel@example.com", "6MonkeysRLooking^"
        res = client.register_user("daniel@example.com", "6MonkeysRLooking^")
        assert res.ok

        new_client = APIClient(credentials)
        res = new_client.request_token()
        assert res.status_code == 400
        contents = res.json()
        assert contents["error"] == "bad request"
        assert contents["message"].lower() == "unconfirmed account"

    @pytest.mark.usefixtures("sqlite_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_resend_confirmation(self, client):
        credentials = "daniel@example.com", "6MonkeysRLooking^"
        res = client.register_user("daniel@example.com", "6MonkeysRLooking^")
        assert res.ok

        new_client = APIClient(credentials)
        res = new_client.request_account_confirmation()
        assert res.ok
        content = res.json()
        assert content["email"] == "daniel@example.com"


class TestPassword:

    @pytest.mark.usefixtures("sqlite_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_change_password(self, client):
        email, old_password = client.credentials
        new_client = APIClient((email, old_password))
        new_client.request_token()

        new_password = "666NewPassword$"
        res = new_client.change_password(old_password, new_password)
        assert res.ok

        # Change the password to the original one so the other test can work
        res = new_client.change_password(new_password, old_password)
        assert res.ok

    @pytest.mark.usefixtures("sqlite_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_request_reset_password(self, client):
        res = client.request_password_reset()
        assert res.ok
        contents = res.json()
        assert contents["email"] == client.credentials[0]
