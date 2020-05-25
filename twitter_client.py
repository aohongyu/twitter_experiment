import json
import os
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
    :type user_id: str
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


def write_following_user_id(user_id):
    """
    Given a user id, ouput a file of user id that the given user is following.
    :param user_id: user id
    :type user_id: str
    :return: None
    :rtype: None
    """
    output_file = 'following_list/' + user_id + '_following.txt'
    f = open(output_file, 'w')

    try:
        for friends in Cursor(TWITTER_CLINET.friends_ids, id=user_id).items():
            f.write(str(friends))
            f.write('\n')
        print(str(user_id) + "_following.txt write successfully :)")
    except tweepy.RateLimitError:
        print("Rate limit exceeded.")
        print("Sleeping for rate limit.")
        time.sleep(TWITTER_RATE_LIMIT)
    except tweepy.TweepError as tt:
        print(tt)
        os.remove(output_file)  # delete file if error occurs

    f.close()


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

            # check if the current tweet posted after the end date
            if tp.is_above_time_period(tweet_json, end_date):
                continue

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
        os.remove(output_file)  # delete file if error occurs
        print(tt)

    f.close()


def write_following_timeline(user_id, start_date, end_date):
    """
    Given a user id, ouput all following's timeline in a specific time period.
    :param user_id: user id
    :type user_id: str
    :param start_date: start date
    :type start_date: str
    :param end_date: end date
    :type end_date: str
    :return: None
    :rtype: None

    Requirement: start and end date should in the format of 'yyyy-mm-dd'
    """
    following_list = tp.get_following_list(user_id)
    if len(following_list) == 0:
        return

    print("Writing user's timeline, please wait...")
    for following in following_list:
        print("Writing user " + following)
        write_timeline_item(following, start_date, end_date)


def is_following(user_a, user_b):
    """
    Given two user ids, check if a is following b.
    :param user_a: user id for a
    :type user_a: str
    :param user_b: user id for b
    :type user_b: str
    :return: if a is following b
    :rtype: bool
    """
    try:
        status = TWITTER_CLINET.show_friendship(source_id=user_a,
                                                target_id=user_b)
        return status[0].following
    except tweepy.RateLimitError:
        print("Rate limit exceeded.")
        print("Sleeping for rate limit.")
        time.sleep(TWITTER_RATE_LIMIT)
    except tweepy.TweepError as tt:
        error_message(tt)
        return False


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
    print(tojson['message'] + " Error code: " + str(tojson['code']))


if __name__ == "__main__":
    write_following_timeline('1262160257008238597', '2020-01-01', '2020-05-25')
    # write_following_user_id('1262160257008238597')
