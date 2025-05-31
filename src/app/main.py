from src.app.components.dashboard import Dashboard
from src.app.components.sidebar import Sidebar


class App:
    def __init__(self):
        self.dashboard = Dashboard()
        self.side_bar = Sidebar(
            on_load_file=self.dashboard.on_load_file,
            on_display_graph=self.dashboard.on_display_graph,
            on_display_data_sample=self.dashboard.on_display_data_sample
        )
