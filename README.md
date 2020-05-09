# Twitter Experiment
An API that can take in raw twitter object files(files with twitter object). Extracting useful information from the file, and store them into a simple database.


## Getting Started
Before running the program, you need to have MongoDB installed, click [here][1] to find the installation guide.

## Prerequisites
This program works with Python 3.5+.

## Description
High level structure of the project

**RAW Twitter Object Files  API  Database**

For the database, we want the data stored in the following format:  

{'name': name, 'source': {'source': count}}

Where,  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'name' is the unique identifier for a data item in the database, a.k.a. 'screen_name' in [Tweet objects][2].  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'source' is the user that this user retweet from.  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'count' is the number of tweets this user retweet from the source.  

For example, if user John retweets three tweets from user Alice, then in the data entries, there should be an item as:  

    {'name': 'John', 'source': {'Alice': 3}}  
If John also retweet four tweets from User Bob, then the entries should look like:  

    {'name': John, 'source': {'Alice': 3, 'Bob': 1}}




[1]:https://docs.mongodb.com/manual/installation/
[2]:https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object