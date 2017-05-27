import tweepy
import json


class TwitterApi:
    def __init__(self, auth_data):
        self._api = self.authenticate(auth_data)

    def authenticate(self, auth_data):
        auth = tweepy.OAuthHandler(
                auth_data['consumer_key'],
                auth_data['consumer_secret'])
        auth.set_access_token(
                auth_data['access_token'],
                auth_data['access_token_secret'])
        return tweepy.API(auth, wait_on_rate_limit_notify=True)

    def start_stream(self, user_ids, track, on_status, on_delete):

        stream_listener = StreamListener(self._api, on_status, on_delete)
        stream = tweepy.Stream(
                auth=self._api.auth,
                listener=stream_listener)
        stream.filter(follow=user_ids, track=track)

    def get_user_id(self, username):
        return self.api.get_user(username).id


class StreamListener(tweepy.StreamListener):
    def __init__(self, api, on_status, on_delete):
        self._api = api
        self._on_status = on_status
        self._on_delete = on_delete

    def on_status(self, status):
        self._on_status(status)

    def on_data(self, data):
        json_data = json.loads(data)

        if 'delete' in json_data:
            self._on_delete(json_data['delete']['status']['id'])
        else:
            status = tweepy.Status.parse(self._api, json_data)
            self._on_status(status)

    def on_error(self, status_code):
        print('got twitter stream error: %d' % status_code)
