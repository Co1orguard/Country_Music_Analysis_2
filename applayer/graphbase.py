from typing import Any
from networkx import Graph
from bokeh.palettes import d3
from applayer.artist import Artist


class GraphBase(object):
    """
    The GraphBase class uses composition to adapt the NetworkX.Graph class. It acts as a superclass for ArtistGraph
    """
    def __init__(self):
        self.__graph = Graph()

    @property
    def graph(self) -> Graph:
        """
        Getter for the __graph composite
        :return:
        """
        return self.__graph

    def add_node(self, artist: Artist, **attr: Any) -> None:
        """
        Adapter for the Graph.add_node method; Should use the artistID attribute for the node
        :param artist: Node to be added to graph
        """
        colors = d3['Category10'][8]
        size = 15 if artist.level == 0 else 10
        self.__graph.add_node(artist.artistID, **attr, artistName=artist.artistName, size=size,
                              color=colors[artist.level])

    def has_node(self, node0: Artist, **attr: Any) -> bool:
        """
        Adapter for the Graph.has_node method; should use the artistID as the node
        :param node0: Node to be found
        :param attr: optional attributes
        """
        return self.__graph.has_node(node0.artistID, **attr)

    def add_edge(self, node0: Artist, node1: Artist, **attr: Any) -> None:
        """
        Adapter for the Graph.add_edge method; should use the artistID as the node
        :param node0:
        :param node1:
        """
        self.__graph.add_edge(node0.artistID, node1.artistID, **attr, weight=1)

    def has_edge(self, node0: Artist, node1: Artist, **attr: Any) -> bool:
        """
        Adapter for the Graph.has_edge method; should use the artistID as the node
        :param node0:
        :param node1:
        :param attr:
        :return:
        """
        return self.__graph.has_edge(node0.artistID, node1.artistID, **attr)

    def incr_edge(self, node0: Artist, node1: Artist) -> None:
        """
        Adapter for getting the weight attribute for an edge;
        :param node0:
        :param node1:
        """
        self.__graph[node0.artistID][node1.artistID]["weight"] += 2
