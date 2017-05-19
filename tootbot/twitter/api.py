import tweepy
import json


class TwitterApi:
    def __init__(self, auth_data):
        self.api = self.authenticate(auth_data)

    def authenticate(self, auth_data):
        auth = tweepy.OAuthHandler(auth_data['consumer_key'], auth_data['consumer_secret'])
        auth.set_access_token(auth_data['access_token'], auth_data['access_token_secret'])
        return tweepy.API(auth, wait_on_rate_limit_notify=True)

    def start_stream(self, user_ids, track, on_status):
        class MyStreamListener(tweepy.StreamListener):
            def on_status(self, status):
                on_status(status)

            def on_data(self, data):
                status = tweepy.Status.parse(self.api, json.loads(data))
                on_status(status)

            def on_error(self, status_code):
                print('got twitter stream error: %d' % status_code)

        streamListener = MyStreamListener()
        stream = tweepy.Stream(auth=self.api.auth, listener=streamListener)
        stream.filter(follow=user_ids, track=track)

    def get_user_id(self, username):
        return self.api.get_user(username).id
