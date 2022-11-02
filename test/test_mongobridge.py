from unittest import TestCase

import pymongo.errors

import datalayer.artistnotfound
from datalayer.mongobridge import MongoBridge
from datalayer.artistnotfound import ArtistNotFound
from pymongo.errors import ServerSelectionTimeoutError


class TestMongoBridge(TestCase):

    def setUp(self) -> None:
        self.mongo_bridge = MongoBridge("mongodb://localhost:27017/", "BristolData", "Artists")

    def test_get_all_artists(self):
        artists = self.mongo_bridge.get_all_artists()
        self.assertEqual(179, len(artists))
        a0 = next(item for item in artists if item["artistID"] == 1826136)["artistName"]
        self.assertEqual("Stephen Tarter", a0)
        a1 = next(item for item in artists if item["artistID"] == 628155)["artistName"]
        self.assertEqual("A. P. Carter", a1)

    def test_get_no_artists(self):
        """
        Assumes that you have created an empty collection called "NoArtists"
        """
        with self.assertRaises(ArtistNotFound):
            self.mongo_bridge = MongoBridge("mongodb://localhost:27017/", "BristolData", "NoArtists")
            artists = self.mongo_bridge.get_all_artists()

    def test_get_artists_from_list(self):
        ids = [938895, 2634203, 1141486, 908705, 2411933, 2304638, 3895080, 1448909, 1448911, 1141474, 2916175, 353265, 1141476, 938862, 1141491, 1141484, 1141487, 307357, 1141480, 516930, 1001138, 1141475, 269365, 1141488, 1141483, 1141489, 2867358, 2867360, 2189637, 908699, 1420640, 2867359, 1826135]
        artists = self.mongo_bridge.get_artists_from_list(ids)
        self.assertEqual(33, len(artists))
        # tests whether the artistID at artists[2] is 1141486
        self.assertEqual(1141486, artists[2]["artistID"])

    def test_get_artists_from_bogus_list(self):
        # First part is good; skips the -1 but adds the good items
        ids = [938895, -1, 269365]
        artists = self.mongo_bridge.get_artists_from_list(ids)
        self.assertEqual(2, len(artists))
        # Second part is bad; should fail and thus raise the exception
        ids = [-1]
        with self.assertRaises(ArtistNotFound):
            artists = self.mongo_bridge.get_artists_from_list(ids)

    def test_get_artist_by_id(self):
        # Artist exists
        artist = self.mongo_bridge.get_artist_by_id(269365)
        self.assertEqual(269365, artist["artistID"])
        self.assertEqual("Jimmie Rodgers", artist["artistName"])
        self.assertEqual(0, artist["level"])
        self.assertEqual("James Charles Rodgers", artist["realname"])

    def test_uri_not_defined(self):
        with self.assertRaises(ServerSelectionTimeoutError):
            self.mongo_bridge = MongoBridge("mongodb://nohost:27017/", "Blah", "Artists")
            artist = self.mongo_bridge.get_artist_by_id(269365)
