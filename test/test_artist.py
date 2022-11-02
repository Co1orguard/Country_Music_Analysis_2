from unittest import TestCase
from applayer.artist import Artist


class TestArtist(TestCase):

    def setUp(self) -> None:
        self.artist_0 = Artist(2309551, "Frank Stamps", "", "", 0)
        testdata_1 = {
          "_id": {
            "$oid": "630176cbc210d497ecd5db2e"
          },
          "artistID": 2309551,
          "artistName": "Frank Stamps",
          "realname": None,
          "profile": "Hello, Frank",
          "collaborators": [],
          "level": 0
        }
        self.artist_1 = Artist(testdata_1)
        testdata_2 = {
          "_id": {
            "$oid": "63016fde0f877215590c12a3"
          },
          "artistID": 2968305,
          "artistName": "Mr. & Mrs. Ernest Stoneman",
          "realname": None,
          "profile": "",
          "collaborators": [
            {
              "collaboratorID": 938895,
              "collaboratorName": "Ernest Stoneman",
              "releaseID": 10594844,
              "roles": None
            },
            {
              "collaboratorID": 1448909,
              "collaboratorName": "Hattie Stoneman",
              "releaseID": 10594844,
              "roles": [
                "Fiddle [Uncredited]"
              ]
            }
          ],
          "level": 0
        }
        self.artist_2 = Artist(testdata_2)

    def test_collaborators(self):
        self.assertEqual(2, len(self.artist_2.collaborators))

    def test_realname(self):
        self.assertIsNone(self.artist_1.realName)
        self.assertIsNone(self.artist_2.realName)

    def test_profile(self):
        self.assertEqual("Hello, Frank", self.artist_1.profile)
        self.assertEqual("", self.artist_2.profile)

    def test_ids(self):
        self.assertEqual(2968305, self.artist_2.artistID)
        self.assertNotEqual(0, self.artist_2.artistID)

    def test_artistName(self):
        self.assertEqual("Frank Stamps", self.artist_0.artistName)
        self.assertEqual("Mr. & Mrs. Ernest Stoneman", self.artist_2.artistName)

    def test_str(self):
        self.assertEqual("Frank Stamps (2309551)", self.artist_0.__str__())
        self.assertEqual("Frank Stamps (2309551)", self.artist_1.__str__())

