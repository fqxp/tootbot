class MastodonUser:

    def __init__(self, auth):
        self._auth = auth

    def toot(self, text, private):
        print('TOOT (%s): %s' % (private, text))
