import tweet_process as tp
import matplotlib.pyplot as plt
import glob
import time

if __name__ == "__main__":
    file_path = 'data_files/*.txt'
    data_files = glob.glob(file_path)

    print("Setting up database, please wait...")
    start = time.time()
    for files in data_files:  # set up database
        tp.set_up_database(files)
    end = time.time()
    set_up_time = end - start
    print("Database set up successfully :) for " + str("%.2f" % set_up_time)
          + "s")

    # draw a scatter plot for timeline_count v.s. retweet_count
    timeline = []
    retweet = []
    for data_entry in tp.tweet_data.find():
        timeline.append(data_entry['activity']['timeline_count'])
        retweet.append(data_entry['activity']['retweet_count'])

    plt.scatter(timeline, retweet)
    plt.show()
