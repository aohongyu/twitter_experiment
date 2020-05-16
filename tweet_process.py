import glob
import json
import matplotlib.pyplot as plt
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['twitter_project']  # database named 'twitter_project'
tweet_data = db['tweet_data']  # collection named 'tweet_data'


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
    return 'in_reply_to_status_id' in tweet


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
    f = open(data_file, "r")
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


def set_up_database(file):
    """
    Given tweet_data.txt, setting up a database in the format of
    {'name': screen_name,
     'retweet': {'retweet_source': retweet count, ...},
     'activity': {
         'timeline_count': count,
         'retweet_count': count,
         'tweet_count': count,
         'reply_count': count}
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
    while tweets:
        json_data = json.loads(tweets)

        # check user existence
        screen_name = get_tweet_usrname(json_data)
        exist_or_add(screen_name)
        timeline_count += 1

        # check if the tweet is a reply
        if is_reply(json_data):
            reply_count += 1

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
            tweet_count += 1
            source_name = get_tweet_usrname(json_data)
            exist_or_add(source_name)
        tweets = f.readline()

        # update activity data
        target_data = tweet_data.find_one({'name': screen_name})
        target_data['activity']['timeline_count'] = timeline_count
        target_data['activity']['retweet_count'] = retweet_count
        target_data['activity']['tweet_count'] = tweet_count
        target_data['activity']['reply_count'] = reply_count
        tweet_data.update({'name': screen_name}, {'$set': target_data})

    f.close()


if __name__ == "__main__":
    file_path = 'data_files/*.txt'
    data_files = glob.glob(file_path)

    # for files in data_files:  # set up database
    #     set_up_database(files)

    timeline = []
    retweet = []
    for data_entry in tweet_data.find():
        timeline.append(data_entry['activity']['timeline_count'])
        retweet.append(data_entry['activity']['reply_count'])

    plt.scatter(timeline, retweet)
    plt.show()
