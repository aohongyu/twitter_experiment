# Twitter Experiment
An API that can take in raw twitter object files(files with twitter object). Extracting useful information from the file, and store them into a simple database.


## Getting Started
Before running the program, you need to have the latest [MongoDB][1] and  [PyMongo][2] distribution installed.

## Prerequisites
This program works with Python 3.5+.

## Description
High level structure of the project

**RAW Twitter Object Files  API  Database**

For the database, the data is stored in the following format:  

    {'name': screen_name,
     'retweet': {'retweet_source': retweet count, ...},
     'activity': {
         'timeline_count': count,
         'retweet_count': count,
         'tweet_count': count,
         'reply_count': count},
     'following': [list of followings]
    }

Where,
* 'name': the unique identifier for a data entry in the database, a.k.a. 'screen_name' in [Tweet objects][3].  
* 'retweet': a list that stores all the retweet source.  
* 'retweet_source': the user's unique 'screen_name' that this user retweet from.  
* 'retweet count': the number of retweets this user retweet from the source.  
* 'activity': a list that stores user's activity.  
* 'timeline_count': the number of tweets this user posted.  
* 'retweet_count': the number of retweets this user posted.  
* 'tweet_count': the number of original tweets this user posted.  
* 'reply_count': the number of replies this user posted.  
* 'following': the list of user ids this user following.


For example, if user John has, **one original tweet**, **two replies**, and he **retweets three tweets** from user Alice,  
then in the data entries, there should be an item as:  

    {'name': 'John',
     'retweet': {'Alice': 3},
     'activity': {
         'timeline_count': 6,
         'retweet_count': 3,
         'tweet_count': 1,
         'reply_count': 2},
     'following': []
    } 
If John also **retweets four tweets** from user Bob, then the entry should look like:  

    {'name': 'John',
     'retweet': {'Alice': 3, 'Bob': 4},
     'activity': {
         'timeline_count': 10,
         'retweet_count': 7,
         'tweet_count': 1,
         'reply_count': 2},
     'following': []
    } 


## Installing
You can simply run the Main function from source code for now, further GUI might be added.


[1]:https://docs.mongodb.com/manual/installation/
[2]:https://pymongo.readthedocs.io/en/stable/
[3]:https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object