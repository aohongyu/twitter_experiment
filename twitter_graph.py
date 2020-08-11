import networkx as nx
import matplotlib.pyplot as plt

def community_graph_directed(user, user_following, user_neighbor_following):
    """
    Given a user, user's following, and user neighbors' following, output a
    directed community graph.
    :param user: user's id
    :type user: str
    :param user_following: a list contains user's following
    :type user_following: List[id]
    :param user_neighbor_following: ：List[List[str]]
    :type user_neighbor_following: a list contains user's neighbors' following
    :return: a community graph
    :rtype: networkx.Graph
    """
    G = nx.DiGraph()

    for following in user_following:
        G.add_edge(user, following)

    for i in range(len(user_neighbor_following)):
        for following in user_neighbor_following[i]:
            G.add_edge(user_following[i], following)

    return G


def community_graph_undirected(user, user_following, user_neighbor_following):
    """
    Given a user, user's following, and user neighbors' following, output a
    undirected community graph, that is, there is an edge between two users iff
    they are following each other.
    :param user: user's id
    :type user: str
    :param user_following: a list contains user's following
    :type user_following: List[id]
    :param user_neighbor_following: ：List[List[str]]
    :type user_neighbor_following: a list contains user's neighbors' following
    :return: a community graph
    :rtype: networkx.Graph
    """
    G = community_graph_directed(user, user_following, user_neighbor_following)
    # find users who didn't follow back
    unfollow = [(v, u) for v, u in G.edges() if not G.has_edge(u, v)]
    G.remove_edges_from(unfollow)
    G.remove_nodes_from(list(nx.isolates(G)))  # remove unconnected nodes
    G = G.to_undirected()
    return G

def neighbors_clustering(user, directed, algorithm_keywords):
    """
    Given a user id, this algorithm would automate the process of clustering on the 
    neighbor, using the algorithm indicated by the algorithm_keywrods
    :param user: user's id
    :type user: str
    :param algorithm_keywords: a key word indicate the algorithm use
    :type algorithm_keywords: str
    :param directed: boolean indicate if to constructed a directed/undirected graph
    :type directed: boolean
    """
    


if __name__ == "__main__":
    g = community_graph_directed('1', ['2', '3'], [['5', '6'], ['1', '2']])
    print(g.edges())
    nx.draw(g, with_labels=True)
    plt.show()
