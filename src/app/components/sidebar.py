import streamlit as st


class Sidebar:
    def __init__(self, on_load_file, on_display_graph, on_display_exploration_view):
        self.view = "Data Exploration"
        self.default_file = "data/Tweets.csv"
        self.on_load_file = on_load_file
        self.on_display_graph = on_display_graph
        self.on_display_exploration_view = on_display_exploration_view
        self.get_file()
        self.get_view_selector()
        self.display_configure()

    def get_file(self):
        uploaded_file = st.sidebar.file_uploader("Upload Tweet CSV", type=["csv"])
        if uploaded_file:
            st.session_state["uploaded_file"] = uploaded_file
        else:
            st.session_state["uploaded_file"] = "data/Tweets.csv"
            st.warning("No file uploaded yet. Used default one.")

        self.on_load_file()

    def get_view_selector(self):
        self.view = st.sidebar.radio(
            "Select view:", ("Data Exploration", "Graph Analysis")
        )

    def display_configure(self):
        if self.view == "Data Exploration":
            self.display_configure_exploration()
        elif self.view == "Graph Analysis":
            self.display_configure_graph()

    def display_configure_graph(self):
        if "dataframe" in st.session_state:
            nodes_count = len(st.session_state["dataframe"])
            st.sidebar.subheader("Graph Configuration")
            max_nodes = st.sidebar.number_input(
                "Number of nodes for the graph (Enter below the total rows in data)",
                min_value=1,
                max_value=min(1000, nodes_count),
                value=st.session_state.get("max_nodes", min(100, nodes_count)),
                step=1,
            )

            algorithm = st.sidebar.selectbox(
                "Select community detection algorithm",
                ["Louvain", "Label Propagation", "Girvan Newman"],
            )
            algo_params = {}

            if algorithm == "Louvain":
                resolution = st.sidebar.number_input(
                    "Resolution (Louvain)",
                    value=1.0,
                    min_value=0.1,
                    max_value=5.0,
                    step=0.1,
                )
                algo_params["resolution"] = resolution

            elif algorithm == "Girvan Newman":
                max_communities = st.sidebar.number_input(
                    "Max number of communities (Girvan-Newman)",
                    value=5,
                    min_value=2,
                    max_value=50,
                    step=1,
                )
                algo_params["max_communities"] = max_communities

            elif algorithm == "Label Propagation":
                st.sidebar.info("No extra parameters for Label Propagation.")

            st.session_state["community_algorithm"] = algorithm
            st.session_state["community_params"] = algo_params
            st.session_state["max_nodes"] = max_nodes

            metric = st.sidebar.selectbox(
                "Metric for node size",
                options=["Degree", "Betweenness", "Closeness", "PageRank"],
                index=0,
            )
            st.session_state["node_size_metric"] = metric

            self.on_display_graph()

    def display_configure_exploration(self):
        self.on_display_exploration_view()
