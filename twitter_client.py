import json
import logging
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

RATE_LIMIT_ERROR_MSG = "rate limit exceeded, sleeping for 15 min."
FOLLOWING_WRITE_MSG = "_following.txt write successfully :)"
TWEETS_WRITE_MSG = "_tweets.txt write successfully :)"
TIMELINE_WRITE_MSG = "Writing user's timeline, please wait..."

# log setup
logging.basicConfig(level=logging.INFO,
                    filename='app.log',
                    filemode='a',
                    format='%(asctime)s; %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


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
        logging.warning("tc.get_user_screen_name: " + RATE_LIMIT_ERROR_MSG)
        print("tc.get_user_screen_name: " + RATE_LIMIT_ERROR_MSG)
        time.sleep(TWITTER_RATE_LIMIT)
    except tweepy.TweepError as tt:
        logging.warning("get_user_screen_name: userid=" + str(user_id) + ". "
                        + error_message(tt))
        print("get_user_screen_name: userid=" + str(user_id) + ". " +
              error_message(tt))


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
            f.write(str(friends) + '\n')

        logging.info(str(user_id) + FOLLOWING_WRITE_MSG)
        print(str(user_id) + FOLLOWING_WRITE_MSG)
    except tweepy.RateLimitError:
        logging.warning("tc.write_following_user_id: " + RATE_LIMIT_ERROR_MSG)
        print("tc.write_following_user_id: " + RATE_LIMIT_ERROR_MSG)
        time.sleep(TWITTER_RATE_LIMIT)
    except tweepy.TweepError as tt:
        logging.warning(
            "tc.write_following_user_id: userid=" + user_id + ". " + str(tt))
        print("tc.write_following_user_id: userid=" + user_id + ". " + str(tt))
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
                f.write(json_str + '\n')

        logging.info(user_id + TWEETS_WRITE_MSG)
        print(user_id + TWEETS_WRITE_MSG)
    except tweepy.RateLimitError:
        logging.warning("tc.write_timeline_item: " + RATE_LIMIT_ERROR_MSG)
        print("tc.write_timeline_item: " + RATE_LIMIT_ERROR_MSG)
        time.sleep(TWITTER_RATE_LIMIT)
    except tweepy.TweepError as tt:
        logging.warning(
            "tc.write_timeline_item: " + "userid=" + user_id + ". " + str(tt))
        print("tc.write_timeline_item: " + "userid=" + user_id + ". " + str(tt))
        os.remove(output_file)  # delete file if error occurs

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

    logging.info(TIMELINE_WRITE_MSG)
    print(TIMELINE_WRITE_MSG)

    for following in following_list:
        logging.info("Writing user " + following)
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
        logging.warning("tc.is_following: " + RATE_LIMIT_ERROR_MSG)
        print("tc.is_following: " + RATE_LIMIT_ERROR_MSG)
        time.sleep(TWITTER_RATE_LIMIT)
    except tweepy.TweepError:
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
    return tojson['message'] + " Error code: " + str(tojson['code'])


if __name__ == "__main__":
    write_timeline_item('1262160257008238597', '2020-05-20', '2020-05-30')
