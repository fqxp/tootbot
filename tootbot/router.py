from .forwarder import Forwarder
import json


class Router:
    def __init__(self, config):
        self._forwarders = list(
            self._build_forwarder(config.mastodon_instance_url(), forwarder_config)
            for forwarder_config in config.forwarder_configs())

    def route(self, tweet):
        forwarders = set(
            forwarder
            for forwarder in self._forwarders
            if (forwarder.is_following(tweet) or
                forwarder.is_tracking(tweet)))

        for forwarder in forwarders:
            forwarder.repost(tweet)

    def _build_forwarder(self, api_base_url, forwarder_config):
        return Forwarder(
            api_base_url=api_base_url,
            username=forwarder_config['mastodon']['username'],
            password=forwarder_config['mastodon']['password'],
            trackwords=forwarder_config['twitter'].get('track', []),
            follow=forwarder_config['twitter'].get('follow', []),
            private=forwarder_config['mastodon'].get('private', False))
