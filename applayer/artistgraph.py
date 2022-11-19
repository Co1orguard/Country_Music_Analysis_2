from typing import List
from applayer.artist import Artist
from datalayer.mongobridge import MongoBridge
from applayer.collaboration import Collaboration
from applayer.graphbase import GraphBase
from datalayer.artistnotfound import ArtistNotFound
from applayer.artistlist import ArtistList
from multipledispatch import dispatch
class ArtistGraph(GraphBase):

    @dispatch()
    def __init__(self) -> None:
        super().__init__()
        self.__artists: List[Artist] = []
        self.__collaborations: List[Collaboration] = []

    @dispatch(ArtistList, int)
    def __init__(self, artistlist: ArtistList, depth: int) -> None:
        super().__init__()
        self.__artists: List[Artist] = []
        self.__collaborations: List[Collaboration] = []
        collab_art: Artist

        #declare a queue used to hold the
        self.__next_queue: List[Artist] = artistlist.artist_objects.copy()
        self.__curr_queue: List[Artist]
        self.__visited: List[Artist] = []
        collab_art: Artist = None

        #declare a bridge object
        self.__bridge = MongoBridge()

        #initialize depth to be 0
        current_depth: int = 0

        for element in artistlist.artist_objects:
            self.add_artist(element)
            #self.__next_queue.append(element)
            self.__visited.append(element)

        #for as many layers as the specified depth and as long as there are still artists to add
        while current_depth < depth and self.__next_queue:

            #increment depth to signify we're in the next layer of collaborators
            current_depth += 1

            #empty next_queue for use in next pass and copy it to curr_queue for us to iterate through
            self.__curr_queue = self.__next_queue
            self.__next_queue = []

            #iterate through artist objects
            for art in self.__curr_queue:

                #add artists to graph if they haven't been visited
                #if(art not in self.__visited):
                #   self.__visited.append(art)

                if art.collaborators:

                    #iterate through collaborations for art
                    for collab in art.collaborators:

                        try:
                            #create artist object from collaboration
                            collab_art = Artist(self.__bridge.get_artist_by_id(collab.get("collaboratorID")))

                            collab_art.level = current_depth

                            if (collab_art not in self.__visited) and (collab_art.artistID != 0):

                                self.__next_queue.append(collab_art)

                            if (collab_art not in self.__visited):
                                self.add_artist(collab_art)
                                self.__visited.append(collab_art)


                        except ArtistNotFound:

                            collab_art = Artist(collab.get("collaboratorID"), collab.get("collaboratorName"), "", "", current_depth)

                            if collab_art not in self.__visited:
                                self.add_artist(collab_art)
                            self.__visited.append(collab_art)

                        finally:

                            if collab_art is not None:
                                temp_collab = Collaboration(art, collab_art, collab.get("role"))
                                if temp_collab not in self.__collaborations:
                                    #append collaboration to graph and __collaborations
                                    self.add_collaboration(temp_collab)
    def add_collaboration(self, collab: Collaboration):
        if not super().has_edge(collab.artist0, collab.artist1):
            super().add_edge(collab.artist0, collab.artist1)
            self.__collaborations.append(collab)
        else:
            super().incr_edge(collab.artist0, collab.artist1)

    def add_artist(self, artist: Artist):
        if(not super().has_node(artist)):
            super().add_node(artist)
            self.__artists.append(artist)
    @property
    def artists(self):
        return self.__artists
    @property
    def collaborations(self):
        return self.__collaborations

