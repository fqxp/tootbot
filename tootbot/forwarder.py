import logging
import re


class Forwarder:

    def __init__(self, trackwords, follow, mastodon_connection, private=True):
        self._trackwords = list(map(str.lower, trackwords))
        self._follow = list(map(str.lower, follow))
        self._mastodon_connection = mastodon_connection
        self._private = private

    def repost(self, tweet):
        text = self._text_to_toot(tweet)
        logging.info('Re-tooting tweet %(tweet_id)d on %(mastodon_account)s (%(text)s…)' % {
            tweet_id: tweet.id,
            mastodon_account: self._mastodon_connection._username,
            text: re.sub(r'\n', '↵', text[:25])})
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
