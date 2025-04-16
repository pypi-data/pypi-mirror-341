import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from requests_oauthlib import OAuth1Session
from requests_oauthlib.oauth1_session import TokenMissing, TokenRequestDenied

from evernote_backup.cli_app_util import is_inside_docker
from evernote_backup.evernote_client import EvernoteClientBase


class OAuthDeclinedError(Exception):
    """Raise when user cancels authentication"""


class CallbackHandler(BaseHTTPRequestHandler):
    http_codes = {
        "OK": 200,
        "NOT FOUND": 404,
    }

    def do_GET(self) -> None:
        if not self.path.startswith("/oauth_callback?"):
            self.send_response(self.http_codes["NOT FOUND"])
            self.end_headers()
            return

        self.server.callback_response = self.path

        self.send_response(self.http_codes["OK"])
        self.end_headers()
        self.wfile.write(
            "<html><head><title>OAuth Callback</title></head>"
            "<body>You can close this tab now...</body></html>".encode("utf-8")
        )

    def log_message(self, *args, **kwargs) -> None:  # type: ignore
        """Silencing server log"""


class StoppableHTTPServer(HTTPServer):
    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super().__init__(*args, **kwargs)

        self.callback_response: str = ""

    def run(self) -> None:
        try:  # noqa: WPS501
            self.serve_forever()
        finally:
            self.server_close()


class EvernoteOAuthCallbackHandler(object):
    def __init__(
        self, oauth_client: "EvernoteOAuthClient", oauth_port: int, server_host: str
    ) -> None:
        self.client = oauth_client

        self.server_host = server_host
        self.server_port = oauth_port

    def get_oauth_url(self) -> str:
        return self.client.get_authorize_url(
            f"http://{self.server_host}:{self.server_port}/oauth_callback"
        )

    def wait_for_token(self) -> str:
        return self.client.get_access_token(self._wait_for_callback())

    def _wait_for_callback(self) -> str:
        if is_inside_docker():
            server_param = ("0.0.0.0", self.server_port)  # noqa: S104
        else:
            server_param = (self.server_host, self.server_port)

        callback_server = StoppableHTTPServer(server_param, CallbackHandler)

        thread = threading.Thread(target=callback_server.run)
        thread.start()

        try:  # noqa: WPS501
            while not callback_server.callback_response:
                time.sleep(0.1)
        finally:
            callback_server.shutdown()
            thread.join()

        return callback_server.callback_response


class EvernoteOAuthClient(EvernoteClientBase):
    def __init__(
        self,
        backend: str,
        consumer_key: str,
        consumer_secret: str,
    ) -> None:
        super().__init__(backend=backend)

        self.client_key = consumer_key
        self.client_secret = consumer_secret

        self._session = None

    def get_authorize_url(self, callback_url: str) -> str:
        self._session = OAuth1Session(
            client_key=self.client_key,
            client_secret=self.client_secret,
            callback_uri=callback_url,
        )

        self._session.fetch_request_token(self._get_endpoint("oauth"))

        return self._session.authorization_url(self._get_endpoint("OAuth.action"))

    def get_access_token(self, callback_response_raw: str) -> str:
        try:
            self._session.parse_authorization_response(callback_response_raw)
        except TokenMissing:
            raise OAuthDeclinedError

        try:
            access_token = self._session.fetch_access_token(self._get_endpoint("oauth"))
        except TokenRequestDenied:
            raise OAuthDeclinedError

        return access_token["oauth_token"]
