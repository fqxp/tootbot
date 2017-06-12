from mastodon import Mastodon
from urllib.parse import urlparse
import os.path

APP_ID = 'tootbot'
CREDENTIALS_FILE = 'tootbot_credentials.secret'


class MastodonConnection:

    def __init__(self, api_base_url, username, password):
        self.api_base_url = api_base_url
        self.username = username
        self.mastodon = self._create_mastodon()
        self._login(username, password)

    def toot(self, text, private):
        visibility = 'private' if private else 'public'
        self.mastodon.status_post(text, visibility=visibility)

    def _create_mastodon(self):
        (client_id, client_secret) = self._create_app()

        return Mastodon(
                api_base_url=self.api_base_url,
                client_id=client_id,
                client_secret=client_secret)

    def _create_app(self):
        client_secret_filename = self._client_secret_filename()

        if not os.path.exists(client_secret_filename):
            Mastodon.create_app(
                    client_name=APP_ID,
                    api_base_url=self.api_base_url,
                    to_file=client_secret_filename)

        return tuple(map(str.strip, open(client_secret_filename).readlines()))

    def _login(self, username, password):
        access_token = self.mastodon.log_in(
                username,
                password,
                to_file=self._user_secret_filename(username))

    def _client_secret_filename(self):
        return 'tootbot_%s_client.secret' % urlparse(self.api_base_url).netloc

    def _user_secret_filename(self, username):
        return 'tootbot_%s_%s_user.secret' % (urlparse(self.api_base_url).netloc, username)
