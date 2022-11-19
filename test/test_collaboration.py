from unittest import TestCase
from applayer.artist import Artist
from datalayer.mongobridge import MongoBridge
from applayer.collaboration import Collaboration



class TestCollaboration(TestCase):

    def setUp(self) -> None:
        self.bridgeObj = MongoBridge()
        self.collab_1 = Collaboration(Artist(self.bridgeObj.get_artist_by_id(1141487)), Artist(self.bridgeObj.get_artist_by_id(5766040)), self.bridgeObj.get_artist_by_id(5766040).get("roles"))


    def test_Artist0(self):
        self.assertIsNotNone(self.collab_1.artist0)
        self.assertEqual(Artist(self.bridgeObj.get_artist_by_id(1141487)), self.collab_1.artist0)
        self.assertIsInstance(self.collab_1.artist0, Artist)

    def test_Artist1(self):
        self.assertIsNotNone(self.collab_1.artist1)
        self.assertEqual(Artist(self.bridgeObj.get_artist_by_id(5766040)), self.collab_1.artist1)
        self.assertIsInstance(self.collab_1.artist1, Artist)

    def test_Roles(self):
        self.assertEqual(self.bridgeObj.get_artist_by_id(5766040).get("roles"), self.collab_1.roles)
