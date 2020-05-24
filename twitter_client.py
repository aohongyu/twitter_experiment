import json
import time

import tweepy
from tweepy import API
from tweepy import Cursor

import twitter_authenticator as ta

TOKEN = ta.authenticate_twitter_app()
TWITTER_RATE_LIMIT = 15 * 60  # 15 MINUTES
TWITTER_CLINET = API(TOKEN)


def get_user_screen_name(user_id):
    """
    Given a user id, return the screen name for the corresponding user id.
    :param user_id: user id
    :type user_id: int
    :return: user screen name
    :rtype: str
    """
    try:
        user = TWITTER_CLINET.get_user(user_id)
        return user.screen_name
    except tweepy.RateLimitError:
        print("Rate limit exceeded.")
        print("Sleeping for rate limit.")
        time.sleep(TWITTER_RATE_LIMIT)
    except tweepy.TweepError as tt:
        error_message(tt)


def get_following_user_id(user_id):
    """
    Given a user screen name, return the a list of user id that the given
    user is following.
    :param user_id: user id
    :type user_id: int
    :return: a list of id
    :rtype: List[str]
    """
    friend_list = []
    try:
        for friend in Cursor(TWITTER_CLINET.friends_ids, id=user_id).items():
            friend_list.append(friend)
    except tweepy.RateLimitError:
        print("Rate limit exceeded.")
        print("Sleeping for rate limit.")
        time.sleep(TWITTER_RATE_LIMIT)
    except tweepy.TweepError as tt:
        print(tt)
    return friend_list


def error_message(e):
    """
    Given a tweet error, print out the error message.
    :param e: a tweet error
    :type e: TweepError
    :return: an error message
    :rtype: str
    """
    tojson = json.loads(
        e.reason.replace("[", "").replace("]", "").replace("'", "\""))
    print(tojson['message'])


if __name__ == "__main__":
    # print(get_user_screen_name(1171128033312411648))
    print(get_following_user_id(1171128033312411648))
