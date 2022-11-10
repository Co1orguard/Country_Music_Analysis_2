from unittest import TestCase
from applayer.artist import Artist
from datalayer.mongobridge import MongoBridge



class TestCollaboration(TestCase):

    def setUp(self) -> None:
        self.bridgeObj = MongoBridge
        self.collab_1 = Collaboration(Artist(self.bridgeObj.get_artist_by_id(1141487)), Artist(self.bridgeObj.get_artist_by_id(5766040)), self.bridgeObj.get_artist_by_id(5766040)["roles"])


    def test_Artist0(self):
        self.assertIsNotNone(self.collab_1.__artist0)
        self.assertEqual(self.bridgeObj.get_artist_by_id(1141487), self.collab_1.__artist0)
        self.assertIsInstance(self.collab_1.__artist0, Artist)

    def Test_Artist1(self):
        self.assertIsNotNone(self.collab_1.__artist1)
        self.assertEqual(self.bridgeObj.get_artist_by_id(5766040), self.collab_1.__artist1)
        self.assertIsInstance(self.collab_1.__artist1, Artist)

    def TestRoles(self):
        self.assertEqual(self.bridgeObj.get_artist_by_id(5766040)["roles"], self.collab_1.__artist1["roles"])
        self.assertIsInstance(self.collab_1.__artist1["roles"], list[str])