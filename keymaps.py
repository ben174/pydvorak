class DvorakMapper:
    """ Maps a qwerty key to its dvorak equivalent. """
    def __init__(self):
        qwerty_map = '`1234567890-=QWERTYUIOP[]ASDFGHJKL;\'ZXCVBNM,./'
        dvorak_map = '`1234567890[]\',.PYFGCRL/=AOEUIDHTNS-;QJKXBMWVZ'
        self.map = dict(zip(qwerty_map, dvorak_map))

    def map_key(self, key):
        if key not in self.map.keys():
            return key
        return self.map[key]
