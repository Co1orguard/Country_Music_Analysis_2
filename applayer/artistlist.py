from typing import List, Tuple
from applayer.artist import Artist
from datalayer.mongobridge import MongoBridge
from multipledispatch import dispatch
from pymongo.errors import ServerSelectionTimeoutError


class ArtistList(object):
    """
    The ArtistList class consists of two attributes:
        * __artist_objects: List[Artist] (must be Artist objects)
        * __artists: List[Tuple[int, str]] (ex. [(1141480, Alcoa Quartet), (1141491, Alfred G. Karnes)]
    """
    @dispatch(list)
    def __init__(self, ids: List[int]):
        """
        The constructor uses data in mongo to create attributes based on the input ids list;
        Use a Mongobridge object to pull data from the Mongo database
        """
        self.__artist_objects: List[Artist] = []
        self.__artists: List[Tuple[int, str]] = []
        mongo_if: MongoBridge = MongoBridge("mongodb://localhost:27017/", "BristolData", "Artists")
        artists_list = mongo_if.get_artists_from_list(ids)
        for a in artists_list:
            artist = Artist(a)
            self.__artist_objects.append(artist)
            self.__artists.append((artist.artistID, artist.artistName))
        self.__artists.sort(key=lambda x: x[1])

    @dispatch(str, str, str, list)
    def __init__(self, uri: str, db: str, coll: str, ids: List[int]):
        """
        The constructor uses data in mongo to create attributes based on the input ids list;
        Use a Mongobridge object to pull data from the Mongo database
        """
        self.__artist_objects: List[Artist] = []
        self.__artists: List[Tuple[int, str]] = []
        mongo_if: MongoBridge = MongoBridge(uri, db, coll)
        artists_list = mongo_if.get_artists_from_list(ids)
        for a in artists_list:
            artist = Artist(a)
            self.__artist_objects.append(artist)
            self.__artists.append((artist.artistID, artist.artistName))
        self.__artists.sort(key=lambda x: x[1])


    @dispatch()
    def __init__(self):
        """
        Read all of the data from mongo and attributes for all artists; See comment at head of the
        class;
        Use a Mongobridge object to pull data from the Mongo database
        """
        self.__artist_objects: List[Artist] = []
        self.__artists: List[Tuple[int, str]] = []
        mongo_if: MongoBridge = MongoBridge("mongodb://localhost:27017/", "BristolData", "Artists")
        artists = mongo_if.get_all_artists()
        for a in artists:
            artist = Artist(a)
            self.__artist_objects.append(artist)
            self.__artists.append((artist.artistID, artist.artistName))
        self.__artists.sort(key=lambda x: x[1])

    @dispatch(str, str, str)
    def __init__(self, uri: str, db: str, coll: str):
        """
        Read all of the data from mongo and attributes for all artists; See comment at head of the
        class;
        Use a Mongobridge object to pull data from the Mongo database
        """
        self.__artist_objects: List[Artist] = []
        self.__artists: List[Tuple[int, str]] = []
        mongo_if: MongoBridge = MongoBridge(uri, db, coll)
        artists = mongo_if.get_all_artists()
        for a in artists:
            artist = Artist(a)
            self.__artist_objects.append(artist)
            self.__artists.append((artist.artistID, artist.artistName))
        self.__artists.sort(key=lambda x: x[1])

    @property
    def artists(self) -> List[Tuple[int, str]]:
        """
        Returns the list of artists as list of tuples of (artistid: int, name: str)
        :return: list of artists
        """
        return self.__artists

    @property
    def artist_objects(self) -> List[Artist]:
        """
        Returns the list of Artist objects
        :return:
        """
        return self.__artist_objects

    def __str__(self) -> str:
        """
        Prints a list of Artist objects separated by a comma ','
        ex: Alcoa Quartet (1141480), Alfred G. Karnes (1141491)
        Note that the formatting of the print of the Artist object is determined by
        the Artist class
        :return: str
        """
        return ', '.join(x.__str__() for x in self.__artist_objects)
