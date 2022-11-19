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
        self.__collaboraitons: List[Collaboration] = []

    @dispatch(ArtistList, int)
    def __init__(self, artistlist: ArtistList, depth: int) -> None:
        super().__init__()
        self.__artists: List[Artist] = artistlist.artist_objects
        self.__collaborations: List[Collaboration] = []
        collab_art: Artist

        #declare a queue used to hold the
        self.__next_queue: List[Artist] = artistlist.artist_objects.copy()
        self.__curr_queue: List[Artist]
        self.__visited: List[Artist] = []
        temp_art: Artist = None

        #declare a bridge object
        self.__bridge = MongoBridge()

        #initialize depth to be 0
        current_depth: int = 0

        for element in artistlist.artist_objects:
            self.add_artist(element)
            self.__next_queue.append(element)
            self.__visited.append(element)

        #for as many layers as the specified depth and as long as there are still artists to add
        while((current_depth < depth) and (len(self.__next_queue) > 0)):

            #increment depth to signify we're in the next layer of collaborators
            current_depth += 1

            #empty next_queue for use in next pass and copy it to curr_queue for us to iterate through
            self.__curr_queue = self.__next_queue
            self.__next_queue = []

            #iterate through artist objects
            for art in self.__curr_queue:

                #add artists to graph if they haven't been visited
                if(art not in self.__visited):
                    self.__visited.append(art)

                #iterate through collaborations for art
                for collab in art.collaborators:

                    try:
                        #create artist object from collaboration
                        collab_art = Artist(self.__bridge.get_artist_by_id(collab.get("collaborationID")))


                        if (collab_art not in self.__visited) and (collab_art.artistID != 0):
                            collab_art.level = current_depth
                            self.__next_queue.append(collab_art)

                        if (collab_art not in self.__visited):
                            self.add_artist(collab_art)
                            self.__visited.append(collab_art)


                    except ArtistNotFound:

                        temp_art = Artist(collab.get("collaborationID"), collab.get("collaboratorName"), "", "", current_depth)

                        if temp_art not in self.__visited:
                            self.add_artist(temp_art)
                        self.__visited.append(temp_art)

                    finally:

                        if temp_art is not None:
                            temp_collab = Collaboration(art, temp_art, collab.get("role"))
                            if temp_collab not in self.__collaborations:
                                #append collaboration to graph and __collaborations
                                self.add_collaboraiton(temp_collab)
    def add_collaboraiton(self, collab: Collaboration):
        if not super().has_edge(collab.artist0, collab.artist1):
            super().add_edge(collab.artist0, collab.artist1)
            self.__collaboraitons.append(collab)
        else:
            super().incr_edge(collab.artist0, collab.artist1)

    def add_artist(self, artist: Artist):
        if(not super().has_node(artist)):
            super().add_node(artist)
            self.__artists.append(artist)
    @property
    def get_artists(self):
        return self.__artists
    @property
    def get_collaboration(self):
        return self.__collaboraitons

