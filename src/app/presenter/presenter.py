import matplotlib.colors as mcolors
import networkx as nx
from matplotlib import cm
from pyvis.network import Network

from src.app.model import UserNetwork


class NetworkPresenter:
    def __init__(self, user_network: UserNetwork, min_node_size: int = 5, max_node_size: int = 20):
        self.user_network = user_network
        self.partition = None
        self.min_node_size = min_node_size
        self.max_node_size = max_node_size
        self.metric = self.node_degree_metric

    def visualize_network(self, top_neighbours_nodes=None) -> str:
        graph = self.user_network.graph
        if top_neighbours_nodes is not None:
            graph = self.get_subgraph_with_top_degree_vertices(top_neighbours_nodes)

        self.partition = UserNetwork.detect_communities(graph)
        net = self.create_network(graph, self.partition)

        return net.generate_html()

    def create_network(self, graph: nx.Graph, partition: dict) -> Network:

        net = Network(
            height="600px",
            width="100%",
            bgcolor="#222222",
            font_color="white",
            directed=False,
        )
        cmap = cm.get_cmap("tab20", max(partition.values()) + 1)

        nodes_with_sizes = self.metric(graph.nodes())
        for node, size in nodes_with_sizes.items():
            group = partition.get(node, 0)
            color = mcolors.to_hex(cmap(group))

            net.add_node(str(node), label=str(node), color=color, size=size)

            # net.add_node(str(node), label=str(node), color=color)

        for source, target in graph.edges():
            net.add_edge(str(source), str(target))

        net.repulsion(node_distance=120, spring_length=100)

        return net

    def get_subgraph_with_top_degree_vertices(
            self, number_of_top_vertices: int = 10
    ) -> nx.Graph:
        graph = self.user_network.graph
        top_nodes_by_degree = sorted(
            graph, key=lambda node: graph.degree[node], reverse=True
        )[:number_of_top_vertices]

        subgraph_nodes = set(top_nodes_by_degree)
        for node in top_nodes_by_degree:
            subgraph_nodes.update(graph.neighbors(node))

        return graph.subgraph(subgraph_nodes)

    def node_degree_metric(self, nodes) -> dict[str, float]:
        min_degree = self.user_network.get_min_degree()
        max_degree = self.user_network.get_max_degree()

        nodes_with_sizes = dict()
        for node in nodes:
            value = self.user_network.graph.degree[node]
            nodes_with_sizes[node] = self.__calculate_node_size(value, min_degree, max_degree)

        return nodes_with_sizes

    def __calculate_node_size(self, value: int | float, min_value: int | float, max_value: int | float) -> float:

        scaler = self.max_node_size - self.min_node_size
        return self.min_node_size + (value - min_value) / (max_value - min_value) * scaler
