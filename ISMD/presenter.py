import networkx as nx
from matplotlib import cm
from pyvis.network import Network

from ISMD.model import UserNetwork

import matplotlib.colors as mcolors

class NetworkPresenter:
    def __init__(self, user_network: UserNetwork):
        self.user_network = user_network

    def visualize_network(self, top_neighbours_nodes=None) -> tuple[str, dict]:

        graph = self.user_network.graph
        if top_neighbours_nodes is not None:
            graph = graph.subgraph(top_neighbours_nodes)

        partition = UserNetwork.detect_communities(graph)
        net = self.create_network(graph, partition)

        return net.generate_html(), partition

    def create_network(self, graph: nx.Graph, partition: dict) -> Network:

        net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white", directed=False)
        cmap = cm.get_cmap("tab20", max(partition.values()) + 1)

        for node in graph.nodes():
            group = partition.get(node, 0)
            color = mcolors.to_hex(cmap(group))
            net.add_node(str(node), label=str(node), color=color)

        for source, target in graph.edges():
            net.add_edge(str(source), str(target))

        net.repulsion(node_distance=120, spring_length=100)

        return net


    def get_subgraph_with_top_degree_vertices(self, number_of_top_vertices: int = 10) -> nx.Graph:
        graph = self.user_network.graph
        top_nodes_by_degree = sorted(graph, key=lambda node: graph.degree[node], reverse=True)[:number_of_top_vertices]

        subgraph_nodes = set(top_nodes_by_degree)
        for node in top_nodes_by_degree:
            subgraph_nodes.update(graph.neighbors(node))

        return graph.subgraph(subgraph_nodes)