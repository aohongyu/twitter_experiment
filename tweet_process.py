import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['twitter_project']  # database named 'twitter_project'
retweet_data = db['retweets']  # collection named 'retweets'


def is_retweet(tweet):
    """
    Given a tweet text, determine if it is a retweet from other user.
    :param tweet: a tweet text
    :type tweet: dict
    :return: whether it is a retweet
    :rtype: bool
    """
    return "retweeted_status" in tweet


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
    add the name to the database.
    :param screen_name: the user's screen name
    :type screen_name: str
    :return: None
    :rtype: None
    """
    data = {'name': screen_name}
    if retweet_data.find_one(data) is None:
        new_tweet = {'name': screen_name, 'source': {}}
        retweet_data.insert_one(new_tweet)


def set_up_database(file):
    """
    Given tweet_data.txt, setting up a database in the format of
    {'screen_name': name, 'source': {'source_name': count}}
    :param file: a tweet_data.txt file in json
    :type file: str
    :return: None
    :rtype: None
    """
    f = open(file, "r")
    tweets = f.readline()
    while tweets:
        json_data = json.loads(tweets)

        # check user existence
        screen_name = get_tweet_usrname(json_data)
        exist_or_add(screen_name)

        # check if the tweet is a retweet
        if is_retweet(json_data):
            source_name = get_retweet_source_usrname(json_data)
            exist_or_add(source_name)
            data = retweet_data.find_one({'name': screen_name})
            original_source = data['source']

            # if this user retweet from the source before
            if source_name in original_source:
                source_count = original_source[source_name] + 1
                original_source[source_name] = source_count
            else:
                original_source[source_name] = 1
            # update data to the database
            retweet_data.update({'name': screen_name}, {'$set': data})
        else:
            source_name = get_tweet_usrname(json_data)
            exist_or_add(source_name)
        tweets = f.readline()
    f.close()


if __name__ == "__main__":
    # TODO: for me to test the first line of data file, plz ignore it
    # f = open('test_case.txt', "r")
    # tweets = f.readline()
    # t = json.loads(tweets)
    # print(get_tweet_usrname(t))
    # f.close()
    #
    # TODO:test for 12_tweets.txt, two outputs should be the same
    # source = retweet_data.find_one({'name': 'jack'})['source']
    # count = 0
    # for y in source:
    #     count += source[y]
    # print(count)
    # print(count_retweet('12_tweets.txt'))  # 259

    set_up_database('12_tweets.txt')
    for x in retweet_data.find():
        print(x)
