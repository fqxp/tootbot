_„A toot for a tweet”_

# What is it?

Currently, some things are working.

Will be a bot that uses the Twitter Stream API to forward tweets from certain
users and/or with certain content (e. g., hashtags) to one or more Mastodon
accounts.

# Requirements
* python 3
* virtualenv

# Installation

Create and activate a virtualenv and install requirements:

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

Copy the file `config.json.example` to `config.json` and
edit it:

    $ cp config.json.example config.json
    $ $EDITOR config.json

(You need to set up Twitter API secrets and stuff.)

Run it:

  $ ./run.py


# How it works

In the configuration file, you define one or more "forwarders", which each
will follow a list of Twitter users and/or track a list of words.

_tootbot_ collects all the trackwords and usernames and will open a connection
to the Twitter streaming API to follow those.

For each tweet coming in, _tootbot_ will try to determine which forwarder is
listening. A tweet matches if a tweet was posted by one of the listed followers
and if at least one trackword matches.

For each matching forwarder, _tootbot_ will toot a message containing the text of
the tweet after adding "(via _twitter user_, https://twitter.com/_twitter user
screenname_)" to it. Retweets will be ignored to avoid spamming the Mastodon
timeline with duplicate messages.

# Run it at system startup

t.b.d. (use systemd ...)

# To do

* handle Twitter delete request
