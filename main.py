import json

from networkx.readwrite import json_graph

import twitter_client as tc
import twitter_graph as tg
import twitter_processor as tp

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
                                "timeline items\n2: write followings' "
                                "timeline items\n3: write following IDs\n4: "
                                "plot community graph\n"))
        except ValueError:
            print("The input should be an integer, please try again.")
            continue

        if command not in range(1, 5):
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
        print("Please tell us the period you'd like to query.")
        start = input("What's the start date? (yyyy-mm-dd)\n")
        end = input("What's the end date? (yyyy-mm-dd)\n")
        option = input("What kind of timeline items you'd like to query, "
                       "tweets or retweets?\n")
        tc.write_following_timeline(str(user_id), start, end, option)
    elif command == 3:
        tc.write_following_user_id(str(user_id))
    elif command == 4:
        option = 0
        while True:
            try:
                option = int(
                    input("Please select the type of graph:\n1: directde "
                          "graph\n2: undireted graph\n"))
            except ValueError:
                print("The input should be an integer, please try again.")
                continue

            if option not in range(1, 3):
                print(
                    "Sorry, we don't have option " + str(option) + " for now.")
                continue
            else:
                break

        followings = tp.get_following_list(str(user_id))
        followings_following = tp.get_following_following_list(str(user_id))
        path = 'json_graph/' + str(user_id)
        if option == 1:
            g = tg.community_graph_directed(str(user_id), followings, followings_following)
            with open(path + '_directed_graph.json', 'w', encoding='utf-8') as f:
                json.dump(json_graph.node_link_data(g), f, ensure_ascii=False, indent=4)
            print("Done! You can find " + str(user_id) + "_directed_graph.json in json_graph/")
        elif option == 2:
            g = tg.community_graph_undirected(str(user_id), followings, followings_following)
            with open(path + '_undirected_graph.json', 'w', encoding='utf-8') as f:
                json.dump(json_graph.node_link_data(g), f, ensure_ascii=False, indent=4)
            print("Done! You can find " + str(user_id) + "_undirected_graph.json in json_graph/")

