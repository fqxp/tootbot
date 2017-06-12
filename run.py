#!/usr/bin/env python
from tootbot.config import Config
from tootbot.tootbot import TootBot
from tootbot.twitter import user_cache
from tootbot.twitter.api import TwitterApi
import logging

CONFIG_FILENAME = 'config.json'
USERS_CACHE_FILENAME = 'users.json'

def setup_logging():
    logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(name)s [%(levelname)s]: %(message)s')
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    logging.getLogger('requests_oauthlib').setLevel(logging.CRITICAL)
    logging.getLogger('oauthlib').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    logging.getLogger('tweepy').setLevel(logging.CRITICAL)


if __name__ == '__main__':
    setup_logging()
    config = Config.read(CONFIG_FILENAME)
    twitter_api = TwitterApi(config.twitter_auth_info())
    tootbot = TootBot(config, twitter_api, USERS_CACHE_FILENAME)

    try:
        tootbot.run()
    except KeyboardInterrupt:
        logging.info('Exiting gracefully ...')
