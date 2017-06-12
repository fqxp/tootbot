from tootbot.utils import failsafe
from tootbot.router import Router
from tootbot.twitter import user_cache
import logging


class TootBot:

    def __init__(self, config, twitter_api, users_filename):
        self._config = config
        self._twitter_api = twitter_api
        self._users_filename = users_filename
        self._router = Router(self._config)

    def run(self):
        self._update_user_cache()
        user_ids = self._read_user_ids()
        trackwords = self._config.all_trackwords()

        logging.info('Following user ids: %s' % ','.join(user_ids))
        logging.info('Tracking words: %s' % ','.join(trackwords))

        while True:
            logging.info('Starting bot ...')
            self._twitter_api.start_stream(
                user_ids=user_ids,
                track=trackwords,
                on_status=self.on_status,
                on_delete=self.on_delete)

    @failsafe
    def on_status(self, tweet):
        self._router.route(tweet)

    @failsafe
    def on_delete(self, tweet_id):
        logging.debug('Got delete request: %r' % tweet_id)

    def _read_user_ids(self):
        user_ids_by_screenname = user_cache.read_users(self._users_filename)
        return [str(user_id) for user_id in user_ids_by_screenname.values()]

    def _update_user_cache(self):
        user_cache.update_users(
                self._config.all_users_to_follow(),
                self._users_filename,
                self._twitter_api)
