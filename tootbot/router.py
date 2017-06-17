from .forwarder import Forwarder
from .mastodon_connection import MastodonConnection
import json


class Router:
    def __init__(self, config):
        self._config = config
        self._mastodon_connections_by_account = {}
        self._forwarders = list(
            self._build_forwarder(forwarder_config)
            for forwarder_config in self._config.forwarder_configs())

    def route(self, tweet):
        forwarders = set(
            forwarder
            for forwarder in self._forwarders
            if (forwarder.is_following(tweet) and
                forwarder.is_tracking(tweet)))

        for forwarder in forwarders:
            forwarder.repost(tweet)

    def _build_forwarder(self, forwarder_config):
        return Forwarder(
            trackwords=forwarder_config['twitter'].get('track', []),
            follow=forwarder_config['twitter'].get('follow', []),
            mastodon_connection=self._build_mastodon_connection(
                forwarder_config['mastodon']['account']),
            private=forwarder_config['mastodon'].get('private', False))

    def _build_mastodon_connection(self, account):
        if account not in self._mastodon_connections_by_account:
            self._mastodon_connections_by_account[account] = \
                MastodonConnection(
                    self._config.mastodon_instance_url(),
                    **self._config.mastodon_account_credentials(account))

        return self._mastodon_connections_by_account[account]
