from Menu_things import read_file

class Controls():
    def __init__(self):
        list = [None]*10
        address = 'Languages/Controls.txt'
        file = open(address, 'r')
        list = read_file(file, list)

        self.jump = int(list[0])
        self.up = int(list[1])
        self.down = int(list[2])
        self.left = int(list[3])
        self.right = int(list[4])
        self.sprint = int(list[5])
        self.inventory = int(list[6])
        self.torch = int(list[7])
        self.drop = int(list[8])
        self.interact = int(list[9])

    def update_controls(self):
        list = [None]*10
        address = 'Languages/Controls.txt'
        file = open(address, 'r')
        list = read_file(file, list)

        self.jump = int(list[0])
        self.up = int(list[1])
        self.down = int(list[2])
        self.left = int(list[3])
        self.right = int(list[4])
        self.sprint = int(list[5])
        self.inventory = int(list[6])
        self.torch = int(list[7])
        self.drop = int(list[8])
        self.interact = int(list[9])

controls = Controls()

