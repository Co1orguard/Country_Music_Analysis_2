from unittest import TestCase
from applayer.artist import Artist
from applayer.artistlist import ArtistList
from applayer.artistgraph import ArtistGraph
from applayer.collaboration import Collaboration


class TestArtistGraph(TestCase):

    def setUp(self) -> None:
        self.artistlist = ArtistList([1141491, 1420640, 2867359])
        self.artistgraph = ArtistGraph(self.artistlist, 3)
        self.a = Artist(0, "Jerry Gannod", "Jerry Gannod", "", 0)
        self.b = Artist(1, "Gerald Gannod", "Gerald Gannod", "", 0)
        self.emptygraph = ArtistGraph()

    def test_add_collaboration(self):
        c = Collaboration(self.a, self.b)
        self.emptygraph.add_collaboration(c)
        self.assertTrue(self.emptygraph.has_edge(self.a, self.b))
        self.assertTrue(self.emptygraph.has_edge(self.b, self.a))
        self.assertTrue(self.emptygraph.has_node(self.a))
        self.assertTrue(self.emptygraph.has_node(self.b))

    def test_buildgraph(self):
        self.assertEqual(66, len(self.artistgraph.artists))
        self.assertEqual(91, len(self.artistgraph.collaborations))
        self.assertEqual(0, len(self.emptygraph.artists))
        self.assertEqual(0, len(self.emptygraph.collaborations))

    def test_add_artist(self):
        self.emptygraph.add_artist(self.a)
        self.assertTrue(self.emptygraph.has_node(self.a))
        self.assertFalse(self.emptygraph.has_node(self.b))
