from .mastodon_connection import MastodonConnection
import logging
import re


class Forwarder:

    def __init__(self, api_base_url, username, password, trackwords, follow, private=True):
        self._username = username
        self._private = private
        self._trackwords = list(map(str.lower, trackwords))
        self._follow = list(map(str.lower, follow))
        self._mastodon_connection = MastodonConnection(api_base_url, username, password)

    def repost(self, tweet):
        text = self._text_to_toot(tweet)
        logging.info('Re-tooting tweet %d on %s (%s…)' %
                (tweet.id, self._username, re.sub(r'\n', '↵', text[:25])))
        self._mastodon_connection.toot(text, self._private)

    def is_following(self, tweet):
        return tweet.user.screen_name.lower() in self._follow

    def is_tracking(self, tweet):
        text = tweet.text.lower()
        return not hasattr(tweet, 'retweeted_status') and any(
            trackword in text
            for trackword in self._trackwords)

    def _text_to_toot(self, tweet):
        return '%s (via %s, https://twitter.com/%s)' % (tweet.text, tweet.user.name, tweet.user.screen_name)

    def __str__(self):
        return '<Forwarder username=%s follow=%r track=%r private=%r>' %(
            self._username, list(self._follow), list(self._trackwords, self._private))
