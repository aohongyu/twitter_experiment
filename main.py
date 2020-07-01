import glob
import logging

import twitter_processor as tp
import twitter_client as tc
import json

# log setup
logging.basicConfig(level=logging.INFO,
                    filename='app.log',
                    filemode='a',
                    format='%(asctime)s; %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    # file_path = 'data_files/*.txt'
    # data_files = glob.glob(file_path)
    #
    # logging.info("Setting up database, please wait...")
    # print("Setting up database, please wait...")
    # for files in data_files:  # set up database
    #     logging.info("Reading file " + files[11:])
    #     print("Reading file " + files[11:])
    #     tp.set_up_database(files)
    #
    # logging.info("Database set up successfully.")
    # print("Database set up successfully.")
    #
    # tp.plot_scatter()

    tc.write_following_user_id('2895499182')

    f = open('following_list/2895499182_following.txt', 'r')
    following = f.readline()
    while following:
        tc.write_following_user_id(following)
        following = f.readline()

    tc.write_following_timeline('2895499182', '2019-10-01', '2020-11-30',
                                'retweets')
