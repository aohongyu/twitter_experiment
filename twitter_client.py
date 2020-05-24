import json
import time

import tweepy
from tweepy import API
from tweepy import Cursor

import twitter_authenticator as ta
import twitter_processor as tp

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
        print(tt)


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
        for friends in Cursor(TWITTER_CLINET.friends_ids, id=user_id).items():
            friend_list.append(friends)
    except tweepy.RateLimitError:
        print("Rate limit exceeded.")
        print("Sleeping for rate limit.")
        time.sleep(TWITTER_RATE_LIMIT)
    except tweepy.TweepError as tt:
        print(tt)
    return friend_list


def write_timeline_item(user_id, start_date, end_date):
    """
    Given a user name id and a time period, query the all the tweets in this
    period and write these data into a file.
    :param user_id: user id
    :type user_id: str
    :param start_date: start date
    :type start_date: str
    :param end_date: end date
    :type end_date: str
    :return: None
    :rtype: None

    Requirement: input date should in the format of 'yyyy-mm-dd'
    """
    if not tp.is_valid_date(start_date, end_date):
        return None

    output_file = 'data_files/' + user_id + '_tweets.txt'
    f = open(output_file, 'w')

    try:
        for tweets in tweepy.Cursor(TWITTER_CLINET.user_timeline,
                                    user_id=int(user_id),
                                    tweet_mode='extended').items():
            # extract useful part in twitter objects
            tweet_json = tweets._json
            json_str = json.dumps(tweet_json)

            # check if the tweet is in the chosen tie period
            if tp.is_in_time_period(tweet_json, start_date, end_date):
                f.write(json_str)
                f.write('\n')
        print(user_id + "_tweets.txt write successfully :)")
    except tweepy.RateLimitError:
        print("Rate limit exceeded.")
        print("Sleeping for rate limit.")
        time.sleep(TWITTER_RATE_LIMIT)
    except tweepy.TweepError as tt:
        print(tt)
    f.close()


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
    write_timeline_item('1262160257008238597', '2020-01-30', '2020-12-23')
