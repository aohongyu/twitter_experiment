# Twitter Experiment
An API that crawling raw twitter object files(files with twitter object) from Twitter. Extracting useful information from the files, and plot the users' community graph only for academic research.


## Getting Started
Before running the program, you need to have the latest [NetworkX][1] and [tweepy 3.8.0][2] installed.

You may also need a user credential to get access to Twitter API, which can be applied from [Twitter Developer][3]. Once you got the token, just simply copy and paste it to twitter_credential.py

## Prerequisites
This program works with Python 3.5+.

## Description
* For back-end users  
Feel free to play with each function from the program as they are well-documented.

* For front-end users  
After downloading the program, navigating to twitter_experiment folder, run:

```
$ python3 main.py
```
Then just follow the instruction on the command prompt.

Notice that, after entering the user id, there are four options:

```
Please tell us what you want to do:
1: write timeline items
2: write followings' timeline items
3: write following IDs
4: plot community graph
```

* write timeline items & write followings' timeline items  
The program will crawl and write the user's or user's followings' timeline items in a specific time period. All the information will be stored in ./twitter_experiment/data_files/

* write following IDs  
The program will crawl and write the user's followings' IDs. All the information will be stored in ./twitter_experiment/following_list/

* plot community graph  
The program will output a json graph either directed or undirected of the user's community(the graph is NetworkX graph originally and only be converted in main). Each graph contains user, user's followings, and user's followings' followings. A directed graph will show all the relationship between each user, while an undirected graph will only show the users who are following each other. All the graphs will be stored in ./twitter_experiment/json_graph/


## Installing
Simply run the main function from source code for now, further GUI and features like NLP analysis might be added.


[1]:https://networkx.github.io/
[2]:http://docs.tweepy.org/en/v3.8.0/
[3]:https://developer.twitter.com/en/products/twitter-api