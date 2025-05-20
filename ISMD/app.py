import pandas as pd
import streamlit as st
from presenter import NetworkPresenter
from utils import create_user_network


class App:
    def __init__(self):
        self.user_network = None
        self.network_presenter = None
        self.top_neighbours_nodes = 10
        self.dataframe = None
        self.max_nodes = None

    def setup_page(self) -> None:
        st.set_page_config(layout="wide")
        st.title("📊 Interactive Social Media Dashboard with Community Detection")

    def load_data(self, uploaded_file) -> pd.DataFrame:
        df = pd.read_csv(uploaded_file)
        st.success(f"Loaded {len(df)} tweets!")
        self.dataframe = df

    def get_file(self) -> str:
        default_file = "data/Tweets.csv"
        uploaded_file = st.sidebar.file_uploader("Upload Tweet CSV", type=["csv"])
        if uploaded_file:
            return uploaded_file
        return default_file

    def show_data_sample(self, df: pd.DataFrame) -> None:
        st.subheader("Raw Data Sample")
        st.dataframe(df.head())

    def show_network(self) -> None:
        graph_html = self.network_presenter.visualize_network(self.top_neighbours_nodes)
        st.components.v1.html(graph_html, height=600, scrolling=False)

    def display_community_stats(self) -> None:
        partition = self.network_presenter.partition

        st.subheader("Detected Communities")
        communities_count = {}
        for node, community_id in partition.items():
            communities_count[community_id] = communities_count.get(community_id, 0) + 1

        community_df = pd.DataFrame.from_dict(
            communities_count, orient="index", columns=["Nodes in Community"]
        )
        community_df.index.name = "Community ID"
        st.dataframe(community_df.sort_values("Nodes in Community", ascending=False))

    def configure_graph(self) -> None:
        nodes_count = len(self.dataframe)
        st.sidebar.subheader("Graph Configuration")
        max_nodes = st.sidebar.number_input(
            "Number of nodes for the graph (Enter below the total rows in data)",
            min_value=1,
            max_value=nodes_count,
            value=min(100, nodes_count),
            step=1,
        )
        self.max_nodes = max_nodes

    def process_data(self) -> None:
        uploaded_file = self.get_file()
        self.load_data(uploaded_file)

    def init_network(self):
        # TODO to sampluje liczbe wierszy, jak jest inny df tzn. wiersz to nie uzytkownik to liczba nodów jest mniejsza
        sampled_df = self.dataframe.sample(self.max_nodes)
        self.user_network = create_user_network(sampled_df)
        self.network_presenter = NetworkPresenter(self.user_network)

    def run(self):
        self.setup_page()
        self.process_data()
        self.configure_graph()
        self.init_network()
        self.show_data_sample(self.dataframe)
        self.show_network()
        self.display_community_stats()


if __name__ == "__main__":
    app = App()
    app.run()
