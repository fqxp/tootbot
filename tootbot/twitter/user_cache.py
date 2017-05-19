import os.path
import json

__all__ = ('update_users', 'read_users')


def update_users(usernames, users_filename, twitter_api):
    users = read_users(users_filename)

    missing_usernames = set(usernames) - set(users.keys())
    for username in missing_usernames:
        print('Fetching id for twitter user %s' % username)
        users[username] = twitter_api.get_user_id(username)

    write_users(users_filename, users)

def read_users(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as fd:
            return json.load(fd)
    else:
        return {}

def write_users(filename, users):
    with open(filename, 'w') as fd:
        json.dump(users, fd)

def read_lines(filename):
    with open(filename, 'r') as fd:
        return map(str.strip, fd.readlines())
