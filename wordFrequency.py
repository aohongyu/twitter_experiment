import json
import os
import re
import nltk
import collections

from nltk.corpus import stopwords
from wordcloud import WordCloud
from collections import Counter

import twitter_client as tc
import matplotlib.pyplot as plt


def remove_url_hastag_user(text):
    """Replace URLs found in a text string with nothing 
    (i.e. it will remove the URL from the string).

    Parameters
    ----------
    text : string
        A text string that you want to parse and remove urls.

    Returns
    -------
    The same txt string with url's removed.
    """
    text = re.sub(r"\bhttps:\S*\b", "", text)
    text = re.sub(r"\b\d*\b", "", text)
    text = re.sub(r"[^\w\s@#]", "", text)

    processed_text_list = text.split()
    # hashtags, usernames
    for i in range(0, len(processed_text_list)):
        word = processed_text_list[i]
        if '#' in word or '@' in word:
            processed_text_list[i] = ''

    processed_text_list = list(filter(lambda x: x != '', processed_text_list))
    
    #stemming the word
    sno = nltk.stem.SnowballStemmer('english')
    processed_text_list = [sno.stem(word) for word in processed_text_list]

    processed_text      = ' '.join(processed_text_list)

    return processed_text

def extract_english_word(txt):
    """Filter out Non-English word and common english stop words.

    Parameters
    ----------
    txt : string
        A text string that you want to filter out the Non-English lower case word and common english stop words.

    Returns
    -------
    The same txt string with Non-English word and common english stop words removed.
    """

    #set of common english stop words from nltk
    stop_words = stopwords.words('english')
    stop_words += ['https','year','years','rt','co','new','also','like','today']

    stop_words = set(stop_words)

    #regex for english words with length between 2 and 100 letters
    lower_case_english_regx = "[a-z]{2,100}"

    #filter out non-english words
    words = re.findall(lower_case_english_regx, txt.lower())


    #filter out common stop words
    words = [w for w in words if not w in stop_words] 
    return words

def user_word_count(user_id):
    """count the english word frequency of a given user from his retweet file

    Parameters
    ----------
    user_id : number/string
    user id of the desired user

    Returns
    -------
    return word frequency Counter object of user with user_id
    """
    
    file_path = "hardmaru_data_files/" + str(user_id) + "_retweets2019-10-01-2019-11-30.txt"
    
    # print(file_path)

    word_freq = collections.Counter()
    try:
        with open(file_path) as f:
            for line in f:

                data            = json.loads(line)

                # print("data load properly")
                #text for the retweet
                retweet_text    = data['full_text']
                #text of the original tweet
                original_text   = data['retweeted_status']['full_text']

                # print("field load properly")

                retweet_text_procssed   = remove_url_hastag_user(retweet_text)
                original_text_processed = remove_url_hastag_user(original_text)

                # print("text processed properly")

                retweet_word_list  = extract_english_word(retweet_text_procssed)
                original_word_list = extract_english_word(original_text_processed)

                word_freq = word_freq + collections.Counter(retweet_word_list) + collections.Counter(original_word_list)
    except:
        print(file_path)
        print("no file exist for this user {0}, skipping".format(str(user_id)))
        return word_freq

    return word_freq


def group_word_count(user_id_list):
    """count the english word frequency of a group of users

    Parameters
    ----------
    user_id_list : list of string/number
    a list of user id

    Returns
    -------
    return word frequency Counter object of this group of users id
    """
    
    word_freq = collections.Counter()
    for user in user_id_list:
        word_freq += user_word_count(user)

    return word_freq

def group_follower_count(user_id_list):
    """count the english word frequency of a group of users

    Parameters
    ----------
    user_id_list : list of string/number
    a list of user id

    Returns
    -------
    return word frequency Counter object of this group of users id
    """
    
    total_follower = {}
    for user in user_id_list:
        total_follower[user] = tc.get_user_follower_number(str(user))
        sorted_total_follower = sorted(total_follower, reverse=True, key=lambda x: total_follower[x])

    return sorted_total_follower

def cluster_word_frequency(word_vector):
    """calculate the word frequency of each word for a given cluster

    Parameters
    ----------
    word_vector: word vector count of a given cluster

    Returns
    -------
    return word frequency dictionary a given cluster
    frequency vector is calcualted as follow:
    for words in word_vector:
        word fequency = # of words/ total number of words in this cluster
    """

    sum = 0
    words_dict = dict(word_vector).keys()
    for word in words_dict:
        sum += word_vector[word]

    word_frequency_vector = {}
    for word in words_dict:
        word_frequency_vector[word] = word_vector[word]/sum

    return word_frequency_vector


def relative_word_frequency(cluster_word_freq_vector, global_word_freq_vector):
    """calculate the relative word frequency of a user with respect to a global
    word vector

    Parameters
    ----------
    word_vector: word vector count of a given cluster
    global_word_vector: global word vector

    Returns
    -------
    return relative word frequency dictionary a given user with respect to global word vector
    the relative frequency vector is calcualted as follow:
    for words in word_vector:
        if words is in global_word_vector then word_freq = f(word|cluster)/f(w|global)
        if words is not in globacl_word_vector then word_freq = f(word|cluster)
    """
    sno  = nltk.stem.SnowballStemmer('english')

    relative_frequency_vector_in_global  = {}
    relative_frequency_vector_not_global = {}

    cluster_word_dict   = dict(cluster_word_freq_vector).keys()
    global_word_dict    = global_word_freq_vector.keys()

    for word in cluster_word_dict:
        word_stem = sno.stem(word)        
        if word_stem in global_word_dict:
            word_relative_frequency = cluster_word_freq_vector[word]/global_word_freq_vector[word_stem]
            relative_frequency_vector_in_global[word] = word_relative_frequency
        else:
            # relative_frequency_vector[word] = cluster_word_freq_vector[word]
            relative_frequency_vector_not_global[word] = cluster_word_freq_vector[word]

    sorted_relative_frequency_vector_in_global  = {k: v for k, v in sorted(relative_frequency_vector_in_global.items(),reverse = True, key=lambda item: item[1])}
    sorted_relative_frequency_vector_not_global = {k: v for k, v in sorted(relative_frequency_vector_not_global.items(),reverse = True, key=lambda item: item[1])}

    return sorted_relative_frequency_vector_in_global,sorted_relative_frequency_vector_not_global

def global_word_vector():
    """calculate the global word frequency from file

    Parameters
    ----------
    global_word_vector: global word vector

    Returns
    -------
    return global word frequency vector
    """
    file_path          = "global_word.json"
    global_word_vector = {}
    total              = 0

    with open(file_path,encoding="utf8") as f:
        for line in f:
            line = line.strip().strip(',')
            if line != '':
                word, count = line.split(':')
                word        = word.replace("\"","").strip()

                sno  = nltk.stem.SnowballStemmer('english')
                word = sno.stem(word)
                
                count       = int(count)
                total       += count 

                if word in global_word_vector.keys():
                    global_word_vector[word] = global_word_vector[word] + count
                else:
                    global_word_vector[word] = count

    global_word_frequency = {k: v / total for k, v in global_word_vector.items()}

    return global_word_frequency

def global_word_vector_stat():
    """calculate stat of the global word table from file

    Returns
    -------
    return total word count and total count of the global word vector
    """
    file_path          = "global_word.json"
    global_word_vector = {}
    total              = 0
    word_count         = 0
    with open(file_path,encoding="utf8") as f:
        for line in f:
            line = line.strip().strip(',')
            if line != '':
                word, count = line.split(':')
                word        = word.replace("\"","").strip()

                if word == "decis":
                    print("found it")
                    print(sno.stem(word))

                count       = int(count)
                total       += count 

                sno  = nltk.stem.SnowballStemmer('english')
                word = sno.stem(word)



                if word in global_word_vector.keys():
                    global_word_vector[word] = global_word_vector[word] + count
                else:
                    global_word_vector[word] = count
                    word_count               += 1

