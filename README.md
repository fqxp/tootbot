_„A toot for a tweet”_

# What is it?

Currently, nothing working.

Will be a bot that uses the Twitter Stream API to forward tweets from certain
users and/or with certain content (e. g., hashtags) to one or more Mastodon
accounts.

# Installation

Create and activate a virtualenv and install requirements:

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

Copy the file `config.json.example` to `config.json` and
edit it:

    $ cp config.json.example config.json
    $ $EDITOR config.json

Run it:

  $ ./bot.py

# Run it at system startup

t.b.d. (use systemd ...)
