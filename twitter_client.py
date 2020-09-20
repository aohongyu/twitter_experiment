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

RATE_LIMIT_ERROR_MSG = "Rate limit exceeded, sleeping for 15 min."
FOLLOWING_WRITE_MSG = "_following.txt write successfully."
TWEETS_WRITE_MSG = " write successfully."
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
        if tt.response.status_code in [429, 420, 88]:
            logging.warning("tc.get_user_screen_name: userid=" + str(user_id) +
                            ". " + error_message(tt))
            print("tc.get_user_screen_name: userid=" + str(user_id) + ". " +
                  error_message(tt))
            logging.warning("tc.get_user_screen_name: " + RATE_LIMIT_ERROR_MSG)
            print("tc.get_user_screen_name: " + RATE_LIMIT_ERROR_MSG)
            time.sleep(TWITTER_RATE_LIMIT)
            pass
        else:
            logging.warning("tc.get_user_screen_name: userid=" + str(user_id) +
                            ". " + error_message(tt))
            print("tc.get_user_screen_name: userid=" + str(user_id) + ". " +
                  error_message(tt))


def get_user_follower_num(user_id):
    """
    Given a user id, get the number of followers of this user.
    :param user_id: user id
    :type user_id: str
    :return: the number of followers
    :rtype: int
    """
    return TWITTER_CLINET.get_user(user_id).followers_count


def write_following_user_id(user_id):
    """
    Given a user id, ouput a file of user id that the given user is following.
    :param user_id: user id
    :type user_id: str
    :return: None
    :rtype: None
    """
    user_id = user_id.replace('\n', '')
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
        if tt.response.status_code in [429, 420, 88]:
            logging.warning("tc.write_following_user_id: userid=" + user_id +
                            ". " + str(tt))
            print("tc.write_following_user_id: userid=" + user_id + ". " +
                  str(tt))
            logging.warning(
                "tc.write_following_user_id: " + RATE_LIMIT_ERROR_MSG)
            print("tc.write_following_user_id: " + RATE_LIMIT_ERROR_MSG)
            time.sleep(TWITTER_RATE_LIMIT)
            pass
        else:
            logging.warning("tc.write_following_user_id: userid=" + user_id +
                            ". " + str(tt))
            print("tc.write_following_user_id: userid=" + user_id + ". " +
                  str(tt))

            f.close()
            os.remove(output_file)  # delete file if error occurs
            return

    f.close()


def write_timeline_item(user_id, start_date, end_date, tweet_type):
    """
    Given a user name id and a time period, query the all the tweets in this
    period and write these data into a file.
    :param user_id: user id
    :type user_id: str
    :param start_date: start date
    :type start_date: str
    :param end_date: end date
    :type end_date: str
    :param tweet_type: choose to write timeline or retweet
    :type tweet_type: str
    :return: None
    :rtype: None

    Requirement: 1. input date should in the format of 'yyyy-mm-dd'
                 2. tweet_type should be 'retweets' or 'tweets'
    """
    if tweet_type != 'tweets' and tweet_type != 'retweets':
        print("tweet_type is not valid.")
        return None

    if not tp.is_valid_date(start_date, end_date):
        return None

    output_file = 'data_files/' + user_id + '_' + tweet_type + '_' + \
                  start_date + '_' + end_date + '.txt'

    f = open(output_file, 'w')

    try:
        for tweets in tweepy.Cursor(TWITTER_CLINET.user_timeline,
                                    user_id=int(user_id),
                                    tweet_mode='extended').items():

            # extract useful part in twitter objects
            tweet_json = tweets._json
            json_str = json.dumps(tweet_json)
            is_retweet = tp.is_retweet(tweet_json)

            # check if the current tweet posted after the end date
            if tp.is_above_time_period(tweet_json, end_date):
                continue

            # check if the tweet is in the chosen time period
            if tp.is_in_time_period(tweet_json, start_date, end_date):
                if tweet_type is 'tweets':
                    f.write(json_str + '\n')
                elif tweet_type is 'retweets' and is_retweet:
                    f.write(json_str + '\n')

        logging.info(output_file[11:] + TWEETS_WRITE_MSG)
        print(output_file[11:] + TWEETS_WRITE_MSG)
    except tweepy.RateLimitError:
        logging.warning("tc.write_timeline_item: " + RATE_LIMIT_ERROR_MSG)
        print("tc.write_timeline_item: " + RATE_LIMIT_ERROR_MSG)
        time.sleep(TWITTER_RATE_LIMIT)
    except tweepy.TweepError as tt:
        if tt.response.status_code in [429, 420, 88]:
            logging.warning("tc.write_timeline_item: " + "userid=" + user_id +
                            ". " + str(tt))
            print("tc.write_timeline_item: " + "userid=" + user_id + ". " +
                  str(tt))
            logging.warning("tc.write_timeline_item: " + RATE_LIMIT_ERROR_MSG)
            print("tc.write_timeline_item: " + RATE_LIMIT_ERROR_MSG)
            time.sleep(TWITTER_RATE_LIMIT)
            pass
        else:
            logging.warning("tc.write_timeline_item: " + "userid=" + user_id +
                            ". " + str(tt))
            print("tc.write_timeline_item: " + "userid=" + user_id + ". " +
                  str(tt))

            f.close()
            os.remove(output_file)  # delete file if error occurs
            return

    f.close()


def write_following_timeline(user_id, start_date, end_date, tweet_type):
    """
    Given a user id, ouput all following's timeline in a specific time period.
    :param user_id: user id
    :type user_id: str
    :param start_date: start date
    :type start_date: str
    :param end_date: end date
    :type end_date: str
    :param tweet_type: choose to write timeline or retweet
    :type tweet_type: str
    :return: None
    :rtype: None

    Requirement: 1. input date should in the format of 'yyyy-mm-dd'
                 2. tweet_type should be 'retweets' or 'tweets'
    """
    following_list = tp.get_following_list(user_id)
    if len(following_list) == 0:
        return

    logging.info(TIMELINE_WRITE_MSG)
    print(TIMELINE_WRITE_MSG)

    for following in following_list:
        logging.info("Writing userid=" + following)
        print("Writing userid=" + following)
        write_timeline_item(following, start_date, end_date, tweet_type)


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
    except tweepy.TweepError as tt:
        if tt.response.status_code in [429, 420, 88]:
            logging.warning("tc.is_following: " + str(tt))
            print("tc.is_following: " + str(tt))
            logging.warning("tc.is_following: " + RATE_LIMIT_ERROR_MSG)
            print("tc.is_following: " + RATE_LIMIT_ERROR_MSG)
            time.sleep(TWITTER_RATE_LIMIT)
            pass
        else:
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


if __name__ == '__main__':
    # write_timeline_item('1262160257008238597', '2020-07-04', '2020-07-04',
    #                     'retweets')
    print(get_user_follower_num('1262160257008238597'))
