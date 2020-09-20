import logging

import twitter_client as tc

# log setup
logging.basicConfig(level=logging.INFO,
                    filename='app.log',
                    filemode='a',
                    format='%(asctime)s; %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    user_id = 0
    while True:
        try:
            user_id = int(input("Please enter user ID. If you don't have it, "
                                "you can search on https://tweeterid.com/.\n"))
        except ValueError:
            print("The user ID should be an integer, please try again.")
            continue
        else:
            break

    command = None
    while True:
        try:
            command = int(input("Please tell us what you want to do:\n1: write "
                                "timeline items\n2: write following IDs\n"))
        except ValueError:
            print("The input should be an integer, please try again.")
            continue

        if command != 1 and command != 2:
            print("Sorry, we don't have option " + str(command) + " for now.")
            continue
        else:
            break

    if command == 1:
        print("Please tell us the period you'd like to query.")
        start = input("What's the start date? (yyyy-mm-dd)\n")
        end = input("What's the end date? (yyyy-mm-dd)\n")
        option = input("What kind of timeline items you'd like to query, "
                       "tweets or retweets?\n")
        tc.write_timeline_item(str(user_id), start, end, option)
    elif command == 2:
        tc.write_following_user_id(str(user_id))

