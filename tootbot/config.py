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

    def all_users_to_follow(self):
        print('%r' % self._config['bots'])
        return set(itertools.chain.from_iterable(
            bot_config['twitter'].get('follow', [])
            for bot_config in self._config['bots'].values()))

    def all_trackwords(self):
        return set(itertools.chain.from_iterable(
            bot_config['twitter'].get('track', [])
            for bot_config in self._config['bots'].values()))

    def bots(self):
        return self._config['bots'].keys()

    def get_bot(self, bot_name):
        return self._config['bots'][bot_name]
