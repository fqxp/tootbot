import json
import itertools


class Config:
    @classmethod
    def read(cls, filename):
        with open(filename, 'r') as fd:
            config = json.load(fd)
            return Config(config)

    def __init__(self, config):
        self._config = config

    def twitter_auth_info(self):
        return self._config['twitter']

    def mastodon_instance_url(self):
        return self._config['mastodon']['instance_url']

    def all_users_to_follow(self):
        return set(itertools.chain.from_iterable(
            forwarder_config['twitter'].get('follow', [])
            for forwarder_config in self.forwarder_configs()))

    def all_trackwords(self):
        return set(itertools.chain.from_iterable(
            forwarder_config['twitter'].get('track', [])
            for forwarder_config in self.forwarder_configs()))

    def forwarder_configs(self):
        return self._config['forwarders']
