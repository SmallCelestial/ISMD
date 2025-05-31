from enum import Enum

class NodeSizeMetric(str, Enum):
    DEGREE = "Degree"
    BETWEENNESS = "Betweenness"
    CLOSENESS = "Closeness"
    PAGERANK = "PageRank"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
