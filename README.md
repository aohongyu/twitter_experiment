# Twitter Experiment
An API that can take in raw twitter object files(files with twitter object). Extracting useful information from the file, and store them into a simple database.


## Getting Started
Before running the program, you need to have the latest [MongoDB][1] and  [PyMongo][2] distribution installed.

## Prerequisites
This program works with Python 3.5+.

## Description
High level structure of the project

**RAW Twitter Object Files  API  Database**

For the database, we store data in the following format:  

{'name': name, 'source': {'source_name': count}}

Where,  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'name' is the unique identifier for a data item in the database, a.k.a. 'screen_name' in [Tweet objects][3].  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'source' is the user that this user retweet from.  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'source_name' is the user's unique 'screen_name' that this user retweet from.  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'count' is the number of tweets this user retweet from the source.  

For example, if user John retweets three tweets from user Alice, then in the data entries, there should be an item as:  

    {'name': 'John', 'source': {'Alice': 3}}  
If John also retweets four tweets from user Bob, then the entry should look like:  

    {'name': John, 'source': {'Alice': 3, 'Bob': 4}}


## Installing
You can simply run the Main function from source code for now, further GUI might be added.


[1]:https://docs.mongodb.com/manual/installation/
[2]:https://pymongo.readthedocs.io/en/stable/
[3]:https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object