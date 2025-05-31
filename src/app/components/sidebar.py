import streamlit as st


class Sidebar:
    def __init__(self, on_load_file, on_display_graph):
        self.default_file = "data/Tweets.csv"
        self.on_load_file = on_load_file
        self.on_display_graph = on_display_graph
        self.get_file()
        self.display_configure_graph()

    def get_file(self):
        uploaded_file = st.sidebar.file_uploader("Upload Tweet CSV", type=["csv"])
        if uploaded_file:
            st.session_state["uploaded_file"] = uploaded_file
        else:
            st.session_state["uploaded_file"] = "data/Tweets.csv"
            st.warning("No file uploaded yet. Used default one.")

        self.on_load_file()

    def display_configure_graph(self):
        if "dataframe" in st.session_state:
            nodes_count = len(st.session_state["dataframe"])
            st.sidebar.subheader("Graph Configuration")
            max_nodes = st.sidebar.number_input(
                "Number of nodes for the graph (Enter below the total rows in data)",
                min_value=1,
                max_value=min(250, nodes_count),
                value=st.session_state.get("max_nodes", min(100, nodes_count)),
                step=1,
            )
            st.session_state["max_nodes"] = max_nodes

            metric = st.sidebar.selectbox(
                "Metric for node size",
                # options=["Degree"],
                options=["Degree", "Betweenness", "Closeness", "PageRank"],
                index=0,
            )
            st.session_state["node_size_metric"] = metric

            self.on_display_graph()
