import glob
import logging

import matplotlib.pyplot as plt

import twitter_processor as tp

# log setup
logging.basicConfig(level=logging.INFO,
                    filename='app.log',
                    filemode='a',
                    format='%(asctime)s; %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    file_path = 'data_files/*.txt'
    data_files = glob.glob(file_path)

    logging.info("Setting up database, please wait...")
    print("Setting up database, please wait...")
    for files in data_files:  # set up database
        tp.set_up_database(files)
    logging.info("Database set up successfully.")
    print("Database set up successfully.")

    # draw a scatter plot for timeline_count v.s. retweet_count
    timeline = []
    retweet = []
    for data_entry in tp.tweet_data.find():
        timeline.append(data_entry['activity']['timeline_count'])
        retweet.append(data_entry['activity']['retweet_count'])

    plt.scatter(timeline, retweet)
    plt.show()
