import pandas as pd
import streamlit as st

from src.app.presenter.presenter import NetworkPresenter
from src.app.utils.utils import create_user_network


class Dashboard:
    def __init__(self):
        self.df = None
        st.set_page_config(layout="wide")
        st.title("📊 Interactive Social Media Dashboard with Community Detection")

    def on_load_file(self):
        self._load_data()
        self._show_data_sample()

    def on_display_graph(self):
        self._init_network()
        self._display_network()
        self._display_community_stats()

    def _load_data(self):
        uploaded_file = st.session_state.get("uploaded_file")

        if not uploaded_file:
            st.warning("No file uploaded yet. Please select a CSV file in the sidebar.")
            return

        try:
            df = pd.read_csv(uploaded_file)
        except (FileNotFoundError, OSError, pd.errors.EmptyDataError) as e:
            st.error(f"File not found or invalid file: {e}")
            return
        except Exception as e:
            st.error(f"An error occurred while loading the file: {e}")
            return

        st.session_state["dataframe"] = df
        st.success(f"Loaded {len(df)} tweets!")
        self.df = df

    def _show_data_sample(self):
        if self.df is not None:
            st.subheader("Raw Data Sample")
            st.dataframe(self.df.head())

    def _init_network(self):
        if self.df is not None and "max_nodes" in st.session_state:
            df = self.df.sample(st.session_state["max_nodes"])
            user_network = create_user_network(df)
            st.session_state["network_presenter"] = NetworkPresenter(user_network)

    def _display_network(self):
        presenter = st.session_state.get("network_presenter")
        if presenter:
            graph_html = presenter.visualize_network(st.session_state["max_nodes"])
            st.components.v1.html(graph_html, height=600, scrolling=False)

    def _display_community_stats(self):
        presenter = st.session_state.get("network_presenter")
        if presenter:
            partition = presenter.partition
            st.subheader("Detected Communities")
            communities_count = {}
            for _, community_id in partition.items():
                communities_count[community_id] = (
                    communities_count.get(community_id, 0) + 1
                )

            community_df = pd.DataFrame.from_dict(
                communities_count, orient="index", columns=["Nodes in Community"]
            )
            community_df.index.name = "Community ID"
            st.dataframe(
                community_df.sort_values("Nodes in Community", ascending=False)
            )
