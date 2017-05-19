#!/usr/bin/env python
from tootbot.twitter.api import TwitterApi
from tootbot.twitter import user_cache
from tootbot.config import Config


def build_on_status(user_ids):
    def on_status(status):
        # if str(status.user.id) in user_ids:
        print('*' * 80)
        print('%r: %s' % (status.user.screen_name, status.text))

    return on_status


if __name__ == '__main__':
    config = Config.read('config.json')
    twitter_api = TwitterApi(config.twitter_auth_info())

    user_cache.update_users(config.all_users_to_follow(), 'users.json', twitter_api)
    user_ids = list(map(str, user_cache.read_users('users.json').values()))

    try:
        twitter_api.start_stream(
            user_ids=user_ids,
            track=config.all_trackwords(),
            on_status=build_on_status(user_ids))
    except KeyboardInterrupt:
        print('Exiting gracefully')
