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

    def get_min_degree(self):
        return min(dict(self.graph.degree()).values())

    def get_max_degree(self):
        return max(dict(self.graph.degree()).values())

    def detect_communities(
        self, graph: nx.Graph, method: str = "louvain", **kwargs
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

    def get_network_graph_stats(self):
        """
        Compute various graph metrics for each node in the network.

        Returns:
            dict: A dictionary containing the following metrics:

            - "pagerank" (dict): The PageRank score of each node, representing the importance of a node
            based on its connections.
            - "degree_centrality" (dict): The degree centrality of each node, calculated as the number of direct connections
            a node has, normalized by the maximum possible connections.
            - "closeness_centrality" (dict): The closeness centrality of each node, indicating how close a node is to all
            other nodes in terms of the shortest paths. Higher values mean the node can reach others more efficiently.
            - "betweenness_centrality" (dict): The betweenness centrality of each node, showing how often a node lies on the
            shortest paths between other pairs of nodes. High values indicate "bridge" nodes in the network.
            - "triadic_closure" (dict): The number of triangles (3-node fully connected subgraphs) a node is part of.
            Triangles are a key indicator of social clustering or tight-knit groups.
            - "clustering_coefficient" (dict): The local clustering coefficient of each node, representing the likelihood
            that a node's neighbors are also connected to each other. Values range from 0 (no clustering) to 1 (fully connected neighbors).

        These metrics provide insights into the structure of the network, identifying important nodes, tightly-knit communities,
        and the overall connectivity of the graph.
        """
        return {
            "pagerank": nx.pagerank(self.graph),
            "degree_centrality": nx.degree_centrality(self.graph),
            "closeness_centrality": nx.closeness_centrality(self.graph),
            "betweenness_centrality": nx.betweenness_centrality(self.graph),
            "triadic_closure": nx.triangles(self.graph),
            "clustering_coefficient": nx.clustering(self.graph),
        }

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
