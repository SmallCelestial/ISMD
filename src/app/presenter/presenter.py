import matplotlib.colors as mcolors
import networkx as nx
from matplotlib import cm
from pyvis.network import Network

from src.app.model import UserNetwork
from src.app.utils.constants import NodeSizeMetric


class NetworkPresenter:
    def __init__(
        self, user_network: UserNetwork, min_node_size: int = 5, max_node_size: int = 20
    ):
        self.user_network = user_network
        self.partition = None
        self.min_node_size = min_node_size
        self.max_node_size = max_node_size
        self.metric = self.node_degree_metric

    def visualize_network(
        self, params, top_neighbours_nodes=None, algorithm: str = "louvain"
    ) -> str:
        graph = self.user_network.graph
        if top_neighbours_nodes is not None:
            graph = self.get_subgraph_with_top_degree_vertices(top_neighbours_nodes)

        self.partition = self.user_network.detect_communities(
            graph, algorithm, **params
        )
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
            nodes_with_sizes[node] = self.__calculate_node_size(
                value, min_degree, max_degree
            )

        return nodes_with_sizes

    def betweenness_centrality_metric(self, nodes, centrality) -> dict[str, float]:
        min_val = min(centrality.values())
        max_val = max(centrality.values())
        return {
            node: self.__calculate_node_size(centrality[node], min_val, max_val)
            for node in nodes
        }

    def closeness_centrality_metric(self, nodes, closeness) -> dict[str, float]:
        min_val = min(closeness.values())
        max_val = max(closeness.values())
        return {
            node: self.__calculate_node_size(closeness[node], min_val, max_val)
            for node in nodes
        }

    def pagerank_metric(self, nodes, pagerank) -> dict[str, float]:
        min_val = min(pagerank.values())
        max_val = max(pagerank.values())
        return {
            node: self.__calculate_node_size(pagerank[node], min_val, max_val)
            for node in nodes
        }

    def set_metric(self, metric_name: str):
        graph_stats = self.user_network.get_network_graph_stats()
        match metric_name:
            case NodeSizeMetric.DEGREE:
                self.metric = self.node_degree_metric
            case NodeSizeMetric.BETWEENNESS:
                self.metric = lambda nodes: self.betweenness_centrality_metric(
                    nodes, centrality=graph_stats["betweenness_centrality"]
                )
            case NodeSizeMetric.CLOSENESS:
                self.metric = lambda nodes: self.closeness_centrality_metric(
                    nodes, closeness=graph_stats["closeness_centrality"]
                )
            case NodeSizeMetric.PAGERANK:
                self.metric = lambda nodes: self.pagerank_metric(
                    nodes, pagerank=graph_stats["pagerank"]
                )
            case _:
                raise ValueError(f"Unknown metric: {metric_name}")

    def __calculate_node_size(
        self, value: int | float, min_value: int | float, max_value: int | float
    ) -> float:

        scaler = self.max_node_size - self.min_node_size
        return (
            self.min_node_size + (value - min_value) / (max_value - min_value) * scaler
        )
