
from Menu_things import read_file

class Options():
    def __init__(self):
        list = [None]*7
        address = 'Languages/Options.txt'
        file = open(address, 'r')
        list = read_file(file, list)

        self.language = list[0]
        self.resolution = int(list[1])
        self.resolution_changed = int(list[2])
        self.master_volume = int(list[3])
        self.music_volume = int(list[4])
        self.world_volume = int(list[5])
        self.brightness = int(list[6])

options = Options()

def resolution_factor():
    return float(float(options.resolution)/720)

def inv_resolution_factor():
    return float(720/float(options.resolution))
