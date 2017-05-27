from .bot import Bot
import json


class Router:
    def __init__(self, config):
        self._bots = list(
           Bot(bot_name, config.get_bot(bot_name))
            for bot_name in config.bots())

    def route(self, tweet):
        bots = set(
            bot
            for bot in self._bots
            if (bot.is_following(tweet.user.screen_name) or
                bot.is_tracking(tweet.text)))
        for bot in bots:
            bot.repost(tweet, private=True)
