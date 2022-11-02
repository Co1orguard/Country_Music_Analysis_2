class ArtistNotFound(Exception):
    def __init__(self, msg: str, index: int):
        super().__init__(str)
        self.__msg = msg
        self.__index = index

    def __str__(self):
        return "ArtistNotFound {}: {}".format(self.__msg, self.__index)