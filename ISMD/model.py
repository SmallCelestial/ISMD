import re
from datetime import datetime
from typing import List

import networkx as nx
from community import community_louvain


class User:
    def __init__(self, name: str, tweets: List['Tweet'] = None):
        self.name = name
        self.tweets = tweets if tweets else []

    def add_tweet(self, tweet: 'Tweet'):
        if self.tweets is None:
            self.tweets = []
        self.tweets.append(tweet)

    def get_all_mentions(self):
        mentions = set()
        for tweet in self.tweets:
            mentions.update(tweet.mentioned_users_names)

        return mentions

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class Tweet:
    def __init__(self, content: str, retweets_count: int = 0, tweet_created_at: datetime = None):
        self.content = content
        # self.retweet_count = retweets_count
        # self.tweet_created_at = tweet_created_at

    def find_mentioned_users(self):
        mentions = re.findall(r"@(\w+)", self.content)
        return mentions

class Interaction:
    def __init__(self, user1: User, user2: User, tweet: Tweet = None):
        self.user1 = user1
        self.user2 = user2
        self.tweet = tweet

class UserNetwork:
    def __init__(self, users: List[User], interactions: List[Interaction] = None):
        self.graph = nx.Graph()
        self.__init_graph(users, interactions)

    def detect_communities(self):
        return community_louvain.best_partition(self.graph)

    def __init_graph(self, users: List[User], interactions: List[Interaction]):
        self.graph.add_nodes_from(users)
        for interaction in interactions:
            self.graph.add_edge(
                interaction.user1,
                interaction.user2,
                tweet=interaction.tweet)
