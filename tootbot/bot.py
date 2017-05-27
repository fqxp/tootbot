from .mastodon.mastodon_user import MastodonUser


class Bot:

    def __init__(self, name, bot_config):
        self._name = name
        self._mastodon_user = MastodonUser(bot_config['mastodon'])
        self._trackwords = list(map(str.lower, bot_config['twitter'].get('track', [])))
        self._follow = list(map(str.lower, bot_config['twitter'].get('follow', [])))

    def repost(self, tweet, private):
        self._mastodon_user.toot(tweet.text, private)

    def is_following(self, screen_name):
        return screen_name.lower() in self._follow

    def is_tracking(self, text):
        lower_text = text.lower()
        return any(
            trackword in lower_text
            for trackword in self._trackwords)

    def __str__(self):
        return '<Bot name=%s follow=%r track=%r>' %(
            self._name, list(self._follow), list(self._trackwords))
