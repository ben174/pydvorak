class Mapper(object):
    """ A base clap from which to ineherit in order to create a keyboard mapper. """
    def __init__(self):
        self.base_map = None
        self.alt_map = None
        self.map = None

    def create_map(self):
        self.map = dict(zip(self.base_map, self.alt_map))

    def map_key(self, key):
        if key not in self.map.keys():
            return key
        return self.map[key]


class DvorakMapper(Mapper):
    """ Maps a qwerty key to its dvorak equivalent. """
    def __init__(self):
        super(DvorakMapper, self).__init__()
        self.base_map = '`1234567890-=QWERTYUIOP[]ASDFGHJKL;\'ZXCVBNM,./'
        self.alt_map = '`1234567890[]\',.PYFGCRL/=AOEUIDHTNS-;QJKXBMWVZ'
        super(DvorakMapper, self).create_map()
