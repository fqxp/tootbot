import json
import itertools


class Config:
    @classmethod
    def read(cls, filename):
        with open(filename, 'r') as fd:
            data = json.load(fd)
            return Config(data)

    def __init__(self, data):
        self._data = data

    def twitter_auth_info(self):
        return self._data['twitter']

    def all_users_to_follow(self):
        print('%r' % self._data['repost'])
        return set(itertools.chain.from_iterable(
            repost_config['twitter'].get('follow', [])
            for repost_config in self._data['repost'].values()))

    def all_trackwords(self):
        return set(itertools.chain.from_iterable(
            repost_config['twitter'].get('track', [])
            for repost_config in self._data['repost'].values()))
