import re
from typing import List

import networkx as nx
from community import community_louvain


class User:
    def __init__(self, name: str):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class Tweet:
    def __init__(self, content: str, username: str):
        self.content = content
        self.username = username

    def find_mentioned_users(self):
        return re.findall(r"@(\w+)", self.content)

class Interaction:
    def __init__(self, user1: User, user2: User, tweet: Tweet = None):
        self.user1 = user1
        self.user2 = user2
        self.tweet = tweet

class UserNetwork:
    def __init__(self, users: List[User], interactions: List[Interaction] = None):
        self.graph = nx.Graph()
        self.__init_graph(users, interactions)

    @staticmethod
    def detect_communities(graph: nx.Graph) -> dict[User, int]:
        return community_louvain.best_partition(graph)

    def __init_graph(self, users: List[User], interactions: List[Interaction]):
        self.graph.add_nodes_from(users)
        for interaction in interactions:
            self.graph.add_edge(
                interaction.user1,
                interaction.user2,
                tweet=interaction.tweet)


