from Player import *


class Room(object):
    def __init__(self, world_obj, world_f):
        self.world_objects = world_obj
        self.world_factor = world_f


class Hallway(Room):
    def __init__(self):
        self.load_folder = -1
        self.room_number = 2
        self.world_factor = 3 * resolution_factor()
        self.left_wall = Obstacle(True, True, 1, options.resolution, 0, 0, None, None, None, None, None, self.world_factor)
        self.right_wall = Obstacle(True, True, 1, options.resolution, options.resolution*16/9, 0, None, None, None, None, None, self.world_factor)
        self.top_wall = Obstacle(True, True, options.resolution*16/9, 0, 0, 0, None, None, None, None, None, self.world_factor)
        self.room_top = Obstacle(True, True, 800*resolution_factor(), 300*resolution_factor(), 0, 0, None, None, None, None, None, self.world_factor)
        self.floor = Obstacle(True, True, options.resolution*16/9, 75*resolution_factor(), 0, 650*resolution_factor(), None, None, None, None, None, self.world_factor)
        self.bookshelf = Obstacle(True, False, None, None, 300*resolution_factor(), 300*resolution_factor(), pygame.image.load("Images/world_design/decoration/Bookshelf.png"), None, -39, False, None, self.world_factor)
        self.torch_entity = TorchEntity(900*resolution_factor(), 600*resolution_factor(), 100)

        self.world_objects = [self.left_wall, self.right_wall, self.top_wall, self.floor, self.torch_entity]


        super(Hallway, self).__init__(self.world_objects, self.world_factor)


class MartyRoom(Room):
    def __init__(self):
        self.load_folder = -1
        # define world list objects
        self.room_number = 1
        # Obstacle (collide all, collide sides, width, height, x position, y position, image, trim x, trim y, move by trim, rotate(in radians))
        self.world_factor = 3*resolution_factor()
        self.left_wall = Obstacle(True, True, 1, options.resolution, 0, 0, None, None, None, None, None, self.world_factor)
        self.right_wall = Obstacle(True, True, 1, options.resolution, options.resolution*16/9, 0, None, None, None, None, None, self.world_factor)
        self.top_wall = Obstacle(True, True, options.resolution*16/9, 0, 0, 0, None, None, None, None, None, self.world_factor)
        self.room_top = Obstacle(True, True, 800*resolution_factor(), 300*resolution_factor(), 0, 0, None, None, None, None, None, self.world_factor)
        self.hallway = Obstacle(True, True, 480*resolution_factor(), 475*resolution_factor(), 800*resolution_factor(), 0, None, None, None, None, None ,self.world_factor)
        self.floor = Obstacle(True, True, options.resolution*16/9, 75*resolution_factor(), 0, 650*resolution_factor(), None, None, None, None, None, self.world_factor)
        self.bed = Obstacle(True, False, None, None, 90*resolution_factor(), 628*resolution_factor(), pygame.image.load("Images/world_design/decoration/Bed.png"), None, -6, True, None, self.world_factor)
        self.ball = Obstacle(False, False, None, None, 340*resolution_factor(), 500*resolution_factor(), pygame.image.load("Images/world_design/decoration/Football.png"), None, None, None, -45, self.world_factor)
        self.bookshelf = Obstacle(True, False, None, None, 300*resolution_factor(), 528*resolution_factor(), pygame.image.load("Images/world_design/decoration/Bookshelf.png"), None, -39, False, None, self.world_factor)
        self.poster = Obstacle(False, False, None, None, 120*resolution_factor(), 500*resolution_factor(), pygame.image.load("Images/world_design/decoration/Poster.png"), None, None, None, None, self.world_factor)
        self.table = Obstacle(True, False, None, None, 400*resolution_factor(), 600*resolution_factor(), pygame.image.load("Images/world_design/decoration/Table.png"), None, None, False, None, self.world_factor)
        self.window = Obstacle(False, False, None, None, 500*resolution_factor(), 500*resolution_factor(), pygame.image.load("Images/world_design/decoration/Window.png"), None, None, None, None, self.world_factor)

        #OBJECTS:
        # Light(image_pass, x_pos, y_pos, angle, shift_x, shift_y, beam start size, beam_Scale, image_Scale, switch)
        self.lamp = Light("Images/world_design/decoration/Lamp.png", 410, 555, 90, 2, 7, 20, 100, 3, False)
        self.roof_light = Light("Images/world_design/decoration/RoomLight.png", 300, 300, 90, 0, 37, 35, 100, 3, True)
        self.roof_switch = Switch(700, 600, self.roof_light, self.world_factor)

        self.door = Door(800, 475, 123)
        self.chest = Chest(20, 617, self.world_factor)
        self.battery = BatteryEntity(1000, 600)
        self.key_entity = KeyEntity(900, 600, 123)
        self.torch_entity = TorchEntity(900, 600, 100)

        self.world_objects = [self.lamp,
                              self.chest,
                              self.roof_light,
                              self.roof_switch,
                              self.door,
                              self.battery,
                              self.torch_entity,
                              ]
        self.world_decorations = [   self.floor,
                                    self.left_wall,
                                    self.right_wall,
                                    self.top_wall,
                                    self.room_top,
                                    self.hallway,
                                    self.bed,
                                    self.ball,
                                    self.bookshelf,
                                    self.poster,
                                    self.table,
                                    self.window]

        super(MartyRoom, self).__init__(self.world_objects, self.world_factor)