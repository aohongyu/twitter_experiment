import unittest
import json
import tweet_process as tp

file_name = 'data_files/12_tweets.txt'  # the data file you wanna test
user_name = 'jack'  # user's screen name for this file
source = tp.tweet_data.find_one({'name': user_name})


class MyTestCase(unittest.TestCase):
    def test_database_retweet_count(self):
        retweet_source = source['retweet']
        count = 0
        for y in retweet_source:
            count += retweet_source[y]
        self.assertEqual(count, tp.count_retweet(file_name))

    def test_timeline_count(self):
        f = open(file_name, 'r')
        tweets = f.readline()
        count = 0
        while tweets:
            count += 1
            tweets = f.readline()
        f.close()
        self.assertEqual(count, source['activity']['timeline_count'])

    def test_database_tweet_and_retweet(self):
        tweet_count = source['activity']['tweet_count']
        retweet_count = source['activity']['retweet_count']
        reply_count = source['activity']['reply_count']
        f = open(file_name, 'r')
        tweets = f.readline()
        count = 0
        while tweets:
            count += 1
            tweets = f.readline()
        f.close()
        self.assertEqual(tweet_count + retweet_count + reply_count, count)


if __name__ == '__main__':
    unittest.main()
