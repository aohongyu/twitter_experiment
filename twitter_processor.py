import datetime
import json
import logging
import math
import os

import matplotlib.pyplot as plt
import mplcursors
import networkx as nx
import sympy
from pymongo import MongoClient
from sympy import *

import twitter_client as tc

client = MongoClient('localhost', 27017)
db = client['twitter_project']  # database named 'twitter_project'
tweet_data = db['tweet_data']  # collection named 'tweet_data'

INVALID_DATE_MSG = "Input date is invalid. The date should in the format of " \
                   "yyyy-mm-dd."
CHECK_ID_MSG = "There's something wrong with this account, please check " \
               "user's id."

USERS = []
TIMELINE = []
RETWEET = []

# log setup
logging.basicConfig(level=logging.INFO,
                    filename='app.log',
                    filemode='a',
                    format='%(asctime)s; %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def is_retweet(tweet):
    """
    Given a tweet text, determine if it is a retweet from other user.
    :param tweet: a tweet text
    :type tweet: dict
    :return: whether it is a retweet
    :rtype: bool
    """
    return 'retweeted_status' in tweet


def is_reply(tweet):
    """
    Given a tweet text, determine if it is a reply from other user.
    :param tweet: a tweet text
    :type tweet: dict
    :return: whether it is a reply
    :rtype: bool
    """
    return tweet['in_reply_to_status_id'] is not None


def count_retweet(data_file):
    """
    Given a list of tweets, text only, count the number of retweet among the
    user return a list of user and their retweet count from this community.
    :param data_file: a data file with tweet objects
    :type data_file: str
    :return: the number of retweets
    :rtype: int
    """
    retweet_count = 0
    f = open(data_file, 'r')
    tweets = f.readline()
    while tweets:
        if is_retweet(json.loads(tweets)):  # check if the tweet is a retweet
            retweet_count += 1
        tweets = f.readline()
    f.close()
    return retweet_count


def get_retweet_source_id(tweet):
    """
    Given a tweet text, if it is a reweet, get the source id.
    requirement: this tweet must be a retweet.
    :param tweet: a tweet text
    :type tweet: dict
    :return: the id of source
    :rtype: str
    """
    return tweet['retweeted_status']['id_str']


def get_retweet_source_usrname(tweet):
    """
    Given a tweet text, if it is a reweet, get the source id.
    requirement: this tweet must be a retweet.
    :param tweet: a tweet text
    :type tweet: dict
    :return: the screen name of source
    :rtype: str
    """
    return tweet['retweeted_status']['user']['screen_name']


def get_tweet_usrname(tweet):
    """
    Given a tweet text, get the author of this tweet.
    :param tweet: a tweet text
    :type tweet: dict
    :return: the author(screen_name) of this tweet
    :rtype: str
    """
    return tweet['user']['screen_name']


def exist_or_add(screen_name):
    """
    Check if a user is already in the database, if so, do nothing; if not, then
    add the name with a entry to the database.
    :param screen_name: the user's screen name
    :type screen_name: str
    :return: None
    :rtype: None
    """
    data = {'name': screen_name}
    if tweet_data.find_one(data) is None:
        new_tweet = {'name': screen_name,
                     'retweet': {},
                     'activity': {
                         'timeline_count': 0,
                         'retweet_count': 0,
                         'tweet_count': 0,
                         'reply_count': 0}
                     }
        tweet_data.insert_one(new_tweet)


def is_valid_date(start_date, end_date):
    """
    Given start date and end date, check if they are valid dates.
    :param start_date: a date in format of 'yyyy-mm-dd'
    :type start_date: str
    :param end_date: a date in format of 'yyyy-mm-dd'
    :type end_date: str
    :return: if it is a valid date
    :rtype: bool
    """
    # check if the input date format is valid
    try:
        start_year, start_month, start_day = start_date.split('-')
        end_year, end_month, end_day = end_date.split('-')
    except ValueError:
        logging.warning(INVALID_DATE_MSG)
        print(INVALID_DATE_MSG)
        return False

    try:
        start = datetime.datetime(int(start_year), int(start_month),
                                  int(start_day))
        end = datetime.datetime(int(end_year), int(end_month), int(end_day))

        if end < start:  # check if start date and end date is logical
            logging.warning("The input date period is invalid.")
            print("The input date period is invalid.")
            return False
    except ValueError:
        logging.warning(INVALID_DATE_MSG)
        print(INVALID_DATE_MSG)
        return False

    return True


def str_to_date(date):
    """
    Given a string date, convert it to date object.
    :param date: a date in format of 'yyyy-mm-dd'
    :type date: str
    :return: date object
    :rtype: datetime.pyi
    """
    if not is_valid_date(date, '9999-12-31'):
        return None

    year, month, day = date.split('-')
    return datetime.datetime(int(year), int(month), int(day))


def is_in_time_period(tweet, start_date, end_date):
    """
    Given start date and end date, check if the tweet posted during the time
    period.
    :param tweet: a tweet text
    :type tweet: dict
    :param start_date: a date in format of 'yyyy-mm-dd'
    :type start_date: str
    :param end_date: a date in format of 'yyyy-mm-dd'
    :type end_date: str
    :return: if the tweet posted during the time period
    :rtype: bool

    Requirement: start and end date should in the format of 'yyyy-mm-dd'
    """
    if not is_valid_date(start_date, end_date):
        return False

    posted_year = int(tweet['created_at'][-4:])
    posted_month = month_to_num(tweet['created_at'][4:7])
    posted_day = int(tweet['created_at'][8:10])
    posted_date = datetime.datetime(posted_year, posted_month, posted_day)
    start = str_to_date(start_date)
    end = str_to_date(end_date)

    if start <= posted_date <= end:
        return True

    return False


def is_above_time_period(tweet, date):
    """
    Given a tweet and a date, check if the tweet posted after the given date.
    :param tweet: a tweet text
    :type tweet: dict
    :param date: str
    :type date: a date in the format of 'yyyy-mm-dd'
    :return: if the tweet posted after the given date
    :rtype: bool
    """
    if not is_valid_date(date, '9999-12-31'):
        return True

    posted_year = int(tweet['created_at'][-4:])
    posted_month = month_to_num(tweet['created_at'][4:7])
    posted_day = int(tweet['created_at'][8:10])
    posted_date = datetime.datetime(posted_year, posted_month, posted_day)
    target_date = str_to_date(date)

    if posted_date > target_date:
        return True

    return False


def month_to_num(short_month):
    """
    Given an abbreviation for the month, return the corresponding number.
    :param short_month: an abbreviation for the month
    :type short_month: str
    :return: month number
    :rtype: int
    """
    return {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }[short_month]


def get_following_list(user_id):
    """
    Given a user id, return a list contains all the user's following.
    :param user_id: user id
    :type user_id: str
    :return: a list of followings
    :rtype: List[str]
    """
    following_list = []
    user = 'following_list/' + user_id + '_following.txt'

    if not os.path.exists(user):  # check file existence
        tc.write_following_user_id(user_id)

    try:
        f = open(user, 'r')
        following = f.readline()
        while following:
            following_list.append(following[:-1])
            following = f.readline()
        f.close()
    except FileNotFoundError:
        logging.warning(CHECK_ID_MSG)
        print(CHECK_ID_MSG)

    return following_list


def set_up_database(file):
    """
    Given tweet_data.txt, setting up a database in the format of
    {'name': screen_name,
     'retweet': {'retweet_source': retweet count, ...},
     'activity': {
         'timeline_count': count,
         'retweet_count': count,
         'tweet_count': count,
         'reply_count': count},
     'following': []
    }
    :param file: a tweet_data.txt file, whose data in json format
    :type file: str
    :return: None
    :rtype: None
    """
    timeline_count = 0
    retweet_count = 0
    tweet_count = 0
    reply_count = 0

    f = open(file, "r")
    tweets = f.readline()

    if tweets is "":  # make sure to skip some empty files
        logging.warning(file[11:] + " is an empty file, skip")
        print(file[11:] + " is an empty file, skip")
        f.close()
        return

    # get user's following list
    following_list = get_following_list(json.loads(tweets)['user']['id_str'])

    while tweets:
        json_data = json.loads(tweets)

        # check user existence
        screen_name = get_tweet_usrname(json_data)
        exist_or_add(screen_name)
        timeline_count += 1

        # check if the tweet is a retweet
        if is_retweet(json_data):
            retweet_count += 1
            source_name = get_retweet_source_usrname(json_data)
            data = tweet_data.find_one({'name': screen_name})
            original_source = data['retweet']

            # if this user retweet from the source before
            if source_name in original_source:
                source_count = original_source[source_name] + 1
                original_source[source_name] = source_count
            else:
                original_source[source_name] = 1
            # update data to the database
            tweet_data.update({'name': screen_name}, {'$set': data})
        else:
            if is_reply(json_data):  # check if it is a reply
                reply_count += 1
            else:
                tweet_count += 1
                source_name = get_tweet_usrname(json_data)
                exist_or_add(source_name)
        tweets = f.readline()

        # update data
        target_data = tweet_data.find_one({'name': screen_name})
        target_data['activity']['timeline_count'] = timeline_count
        target_data['activity']['retweet_count'] = retweet_count
        target_data['activity']['tweet_count'] = tweet_count
        target_data['activity']['reply_count'] = reply_count
        target_data['following'] = following_list
        tweet_data.update({'name': screen_name}, {'$set': target_data})

    f.close()


def get_database_tweet_info():
    """
    Puts user's information into the lists.
    :return: None
    :rtype: None
    """
    for data_entry in tweet_data.find():
        USERS.append(data_entry['name'])
        TIMELINE.append(data_entry['activity']['timeline_count'])
        RETWEET.append(data_entry['activity']['retweet_count'])


def get_min_distance(fx, p):
    """
    Given a function f(x) and a point p, return the shortest distance between
    the point and curve f(x).
    :param fx: function f(x)
    :type fx: str
    :param p: a point in 2D plane
    :type p: tuple
    :return: the shortest distance between p and f(x)
    :rtype: float
    """
    x = Symbol('x')
    eqn = '(x - ' + str(p[0]) + ')**2 + (' + fx + ' - ' + str(p[1]) + ')**2'

    try:
        deri = diff(eval(eqn))
        r = sympy.solve(deri, x)
        dist_list = []

        for sol in r:
            # prevent round off error
            x = str(sol).replace("I", "0")
            x = eval(x)
            dist_list.append(math.sqrt(eval(eqn)))

        return min(dist_list)

    except NameError:
        print("The input function f(x) is not valid.")
        return None


def get_within_distance_user_list(fx, dist):
    """
    Given a function f(x) and a distance d, return a list of user whose data
    point is within d from f(x).
    :param fx: function f(x)
    :type fx: str
    :param dist: the distance between data point and f(x)
    :type dist: int
    :return: list of user whose data point is within d from f(x)
    :rtype: List[str]
    """
    get_database_tweet_info()
    exp_user = []

    for i in range(len(USERS)):
        p = (TIMELINE[i], RETWEET[i])
        # get distance from every data point to the curve
        dist_p_f = get_min_distance(fx, p)

        if dist_p_f is None:
            continue

        if dist_p_f <= dist:
            exp_user.append(USERS[i])

    return exp_user


def plot_scatter():
    """
    Draw a scatter plot for timeline_count v.s. retweet_count.
    :return: None
    :rtype: None
    """
    get_database_tweet_info()

    fig, ax = plt.subplots()
    ax.scatter(TIMELINE, RETWEET)
    ax.set_title("Timeline Items v.s. Retweets")
    plt.xlabel("Timeline Items")
    plt.ylabel("Retweets")

    # mouse hover
    cursor = mplcursors.cursor(hover=True)
    cursor.connect('add',
                   lambda sel: sel.annotation.set_text(USERS[sel.target.index]))

    plt.show()


def plot_following_graph(user):
    """
    Given a user screen_name, plot a relation graph of this user's followings.
    :param user: user screen_name
    :type user: str
    :return: None
    :rtype: None

    Requirement: input user should in the database
    """
    following_graph = nx.DiGraph()

    try:
        following_list = tweet_data.find_one({'name': user})['following']
        for following in following_list:
            following_graph.add_edge(user, following)

        plt.figure(figsize=(50, 50))  # graph size
        plt.subplot(111)
        nx.draw(following_graph)
        plt.show()
    except TypeError:
        print("User is not found in the database.")


if __name__ == "__main__":
    # plot_following_graph('StanfordHCI')
    plot_following_graph('clarifai')
