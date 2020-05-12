from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['twitter_project']  # database
retweet_data = db['retweets']  # collection


test_list = [
    {'name': 'Jhon', 'source': {'Alice': 3, 'Bob': 4}},
    {'name': 'Amy', 'source': {'Jhon': 3, 'Bob': 12}},
    {'name': 'Mike', 'source': {'Jhon': 5, 'Amy': 2, 'Alice': 1}},
    {'name': 'Penny', 'source': {}}
]
# tweet_data.insert_many(test_list)
# tweet_data.drop()


# for x in tweet_data.find():
#   print(x)


myquery = {'name': 'Jhon'}
mydoc = retweet_data.find_one(myquery)
# print(mydoc)
mydoc['source']['Bob'] = 10
mydoc['source']['Alice'] = 15
# mydoc['source']['Penny'] = 1
# tweet_data.update(myquery, {'$set': mydoc})

myquery = {'name': 'Penny'}
mydoc = retweet_data.find_one(myquery)
mydoc['source']['Bob'] = 10
mydoc['source']['Alice'] = 15
retweet_data.update(myquery, {'$set': mydoc})
for x in retweet_data.find():
    print(x)
