import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import community as community_louvain
import networkx as nx
from networkx.algorithms.community import girvan_newman, label_propagation_communities


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
    def detect_communities(
        graph: nx.Graph, method: str = "louvain", **kwargs
    ) -> Dict[Any, int]:

        method = method.lower()

        if method == "louvain":
            return community_louvain.best_partition(
                graph,
                partition=kwargs.get("partition", None),
                weight=kwargs.get("weight", "weight"),
                resolution=kwargs.get("resolution", 1.0),
                randomize=kwargs.get("randomize", True),
            )
        elif method == "label propagation":
            communities = list(label_propagation_communities(graph))
            return {
                node: idx
                for idx, community in enumerate(communities)
                for node in community
            }

        elif method == "girvan newman":
            k = kwargs.get("max_communities", 5)
            comp = girvan_newman(graph)
            limited = []
            try:
                for _ in range(k - 1):
                    limited = next(comp)
            except StopIteration:
                pass
            communities = list(limited) if limited else list(next(comp))
            return {
                node: idx
                for idx, community in enumerate(communities)
                for node in community
            }
        else:
            raise ValueError(f"Unknown community detection method: {method}")

    def __init_graph(self, users: List[User], interactions: List[Interaction]):
        self.graph.add_nodes_from(users)
        for interaction in interactions:
            self.graph.add_edge(
                interaction.user1, interaction.user2, tweet=interaction.tweet
            )


@dataclass(frozen=True)
class SocialInteraction:
    who_id: str
    to_whom_id: str
    interaction_type: str
    who_username: Optional[str]
    to_whom_username: Optional[str]
    item: Optional[str]
