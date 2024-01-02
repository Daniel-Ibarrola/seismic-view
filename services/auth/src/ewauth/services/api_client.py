import time
import requests
from requests.auth import AuthBase

from ewauth import config


class TokenAuth(AuthBase):
    def __init__(self, token: str, auth_scheme: str = 'Bearer'):
        self.token = token
        self.auth_scheme = auth_scheme

    def __call__(self, request):
        request.headers['Authorization'] = f'{self.auth_scheme} {self.token}'
        return request


class APIClient:
    """ API client that connects to the flask API.
    """

    def __init__(self, credentials: tuple[str, str]):
        self.base_url = config.get_api_url() + "/api/v1"
        self.credentials = credentials
        self.token_auth = None
        self._token_expiration = None

    def request_token(self) -> requests.Response:
        """ Request a token for authentication. """
        res = requests.post(f"{self.base_url}/tokens/", auth=self.credentials)
        if res.ok:
            json = res.json()
            self.token_auth = TokenAuth(token=json["token"])
            expiration = json["expiration"]
            if expiration is not None:
                self._token_expiration = expiration + time.time()
            else:
                self._token_expiration = None
        return res

    def token_expired(self) -> bool:
        """ Check if this client tokes is expired. """
        if self._token_expiration is not None:
            return time.time() > self._token_expiration
        return False

    def register_user(self, email: str, password: str) -> requests.Response:
        return requests.post(
            f"{self.base_url}/new_user/",
            json={
                "email": email,
                "password": password,
            }
        )

    def request_account_confirmation(self) -> requests.Response:
        return requests.get(
            f"{self.base_url}/confirm",
            auth=self.credentials
        )

    def change_password(self, old_password: str, new_password: str) -> requests.Response:
        res = requests.post(
            f"{self.base_url}/change_password/",
            json={
                "old": old_password,
                "new": new_password,
            },
            auth=self.token_auth
        )
        if res.ok:
            self.credentials = (self.credentials[0], new_password)
        return res

    def request_password_reset(self) -> requests.Response:
        return requests.post(
            f"{self.base_url}/reset",
            json={"email": self.credentials[0]}
        )
