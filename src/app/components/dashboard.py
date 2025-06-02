import pandas as pd
import streamlit as st
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from src.app.presenter.presenter import NetworkPresenter
from src.app.utils.constants import NodeSizeMetric
from src.app.utils.utils import create_user_network


class Dashboard:
    def __init__(self):
        self.df = None
        st.set_page_config(layout="wide")
        st.title("📊 Interactive Social Media Dashboard with Community Detection")

    def on_load_file(self):
        self._load_data()


    def on_display_graph(self):
        self._init_network()
        self._display_network()
        self._display_community_stats()
        self._display_graph_metrics()

    def on_display_exploration_view(self):
        # TODO: fix columns types
        self._show_data_sample()
        self._show_data_description()
        self._show_data_columns_types()
        self._show_data_missing_values()
        self._show_data_distribution()
        self._show_tweet_frequency_over_time()
        self._show_text_analysis()
        self._let_filter_data()

    def _show_data_description(self):
        st.subheader("Summary Statistics")
        st.write(self.df.describe(include='all'))

    def _show_data_columns_types(self):
        st.subheader("Column Data Types")
        st.write(self.df.dtypes)

    def _show_data_missing_values(self):
        st.subheader("Missing Values Per Column")
        missing = self.df.isnull().sum()
        missing = missing[missing > 0]
        if not missing.empty:
            st.bar_chart(missing)
        else:
            st.success("No missing values detected.")

    def _show_data_distribution(self):
        st.subheader("Top Users by Tweet Count")
        st.bar_chart(self.df['name'].value_counts().head(10))

    def _show_tweet_frequency_over_time(self):
        self.df['tweet_created'] = pd.to_datetime(self.df['tweet_created'])
        time_series = self.df.groupby(self.df['tweet_created'].dt.date).size()

        st.subheader("Tweet Frequency Over Time")
        st.line_chart(time_series)

    def _show_text_analysis(self):
        st.subheader("Most Common Words in Tweets")
        text_data = " ".join(self.df['text'].dropna())
        word_freq = Counter(text_data.lower().split())
        common_words = dict(word_freq.most_common(50))
        wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(common_words)

        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

    def _let_filter_data(self):
        st.subheader("Filter by User")
        users = st.multiselect("Select users", options=self.df['name'].unique())

        filtered_df = self.df
        if users:
            filtered_df = filtered_df[filtered_df['name'].isin(users)]

        st.dataframe(filtered_df)

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
            presenter = NetworkPresenter(user_network)

            metric_name = st.session_state.get(
                "node_size_metric", NodeSizeMetric.DEGREE
            )
            presenter.set_metric(metric_name)

            st.session_state["network_presenter"] = presenter

    def _display_network(self):
        presenter = st.session_state.get("network_presenter")
        if presenter:
            graph_html = presenter.visualize_network(
                top_neighbours_nodes=st.session_state["max_nodes"],
                algorithm=st.session_state["community_algorithm"],
                params=st.session_state["community_params"],
            )
            st.components.v1.html(graph_html, height=600, scrolling=False)

    def _display_graph_metrics(self):
        presenter = st.session_state.get("network_presenter")
        if presenter:
            network = presenter.user_network
            stats = network.get_network_graph_stats()
            users = [node for node in network.graph.nodes()]

            data = []
            for user in users:
                data.append(
                    {
                        "User": user.name,
                        "Degree Centrality": round(
                            stats["degree_centrality"].get(user, 0), 4
                        ),
                        "Closeness Centrality": round(
                            stats["closeness_centrality"].get(user, 0), 4
                        ),
                        "Betweenness Centrality": round(
                            stats["betweenness_centrality"].get(user, 0), 4
                        ),
                        "Triads": stats["triadic_closure"].get(user, 0),
                        "Clustering Coefficient": round(
                            stats["clustering_coefficient"].get(user, 0), 4
                        ),
                    }
                )

            df = pd.DataFrame(data)
            df = df.sort_values("Degree Centrality", ascending=False)

            st.subheader("User Network Metrics")
            st.dataframe(df, use_container_width=True)

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
