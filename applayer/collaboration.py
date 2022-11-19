from typing import List
from applayer.artist import Artist


class Collaboration(object):

    def __init__(self, art0: Artist, art1: Artist, role: List[str] = None):
        self.artist0: Artist = art0
        self.artist1: Artist = art1
        self.roles: List[str] = role

    @property
    def get_artist0(self) -> Artist:
        return self.artist0
    @property
    def get_artist1(self) -> Artist:
        return self.artist1

    @property
    def get_roles(self) -> List[str]:
        return self.roles
    
