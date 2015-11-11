import pickle
import pygame
pygame.init()

from Item import*
from World import*
from World_Light import*
from Player import*
from Levels import*

class Torch_save():
    def __init__(self, Old_torch):
        self.battery = Old_torch.battery
        self.brightness = Old_torch.brightness
        self.on = Old_torch.on
        self.flicker = Old_torch.flicker

class Key_save():
    def __init__(self, Old_key):
        self.door_code = Old_key.door_code

class Player_save():
    def __init__(self, Egg, marty):
        self.egg  = Egg
        self.rect_x = marty.rect.x
        self.rect_y = marty.rect.y
        self.inventory = [None]*3
        self.hand_number = marty.hand_number

        # inventory list and hand
        for x in range(0, len(marty.inventory)):
            if isinstance(marty.inventory[x], Torch):
                self.inventory[x] = Torch_save(marty.inventory[x])
            if isinstance(marty.inventory[x], Key):
                self.inventory[x] = Key_save(marty.inventory[x])

        self.in_hand = self.inventory[self.hand_number]

        # other stuff
        self.right = marty.right
        self.on_floor = marty.on_floor
        self.move_x = marty.move_x
        self.move_y = marty.move_y
        self.inv_temp = marty.inv_temp
        self.inv_on = marty.inv_on
        self.breath = marty.breath
        self.interact = marty.interact

    def load(self, object):
        object.rect_x = self.rect_x
        object.rect_y = self.rect_y
        object.hand_number = self.hand_number

        # inventory list and hand
        for x in range(0, len(self.inventory)):
            if isinstance(self.inventory[x], Torch_save):
                object.inventory[x] = Torch(0, 0, self.inventory[x].battery, self.inventory[x].on)
            if isinstance(self.inventory[x], Key_save):
                object.inventory[x] = Key(0, 0, self.inventory[x].door_code)

        object.in_hand = object.inventory[object.hand_number]

        # other stuff
        object.right = self.right
        object.on_floor = self.on_floor
        object.move_x = self.move_x
        object.move_y = self.move_y
        object.inv_temp = self.inv_temp
        object.inv_on = self.inv_on
        object.breath = self.breath
        object.interact = self.interact


#From now on is all for the room

class Entity_save(object):
    def __init__(self, Entity):
        self.factor = Entity.factor
        self.original_pos_x = Entity.rect.x
        self.original_pos_y = Entity.rect.y
        self.move_y = Entity.move_y
        self.move_x = Entity.move_x
        self.on_floor = Entity.on_floor

    def load(self, object):
        object.factor = self.factor
        object.factor = self.factor
        object.rect.x = self.original_pos_x
        object.rect.y = self.original_pos_y
        object.move_y = self.move_y
        object.move_x = self.move_x
        object.on_floor = self.on_floor

class Torch_Entity_save(Entity_save):
    def __init__(self, Old_torch):
        self.battery = Old_torch.battery
        super(Torch_Entity_save, self).__init__(Old_torch)

    def load_Torch(self, object):
        object.battery = self.battery

class Key_Entity_save(Entity_save):
    def __init__(self, Old_key):
        self.door_code = Old_key.door_code
        super(Key_Entity_save, self).__init__(Old_key)

    def load_Key(self, object):
        object.door_code = self.door_code

class Chest_save():
    def __init__(self, Old_chest):
        self.original_pos_x = Old_chest.original_pos_x
        self.original_pos_y = Old_chest.original_pos_y

        self.items = Old_chest.items

        self.closed = Old_chest.closed
        self.display_key = Old_chest.display_key

    def load(self, object):
        object.original_pos_x = self.original_pos_x
        object.original_pos_y = self.original_pos_y

        object.items = self.items

        object.closed = self.closed
        object.display_key = self.display_key

class Door_save():
    def __init__(self, Old_door):
        #original position
        self.original_pos_x = Old_door.original_pos_x
        self.original_pos_y = Old_door.original_pos_y
        self.original_factor = Old_door.original_factor

        self.closed = Old_door.closed
        self.key_code = Old_door.key_code

    def load(self, object):
        #original position
        object.original_pos_x = self.original_pos_x
        object.original_pos_y = self.original_pos_y
        object.original_factor = self.original_factor

        object.closed = self.closed

        object.key_code = self.key_code

class Light_save():
    def __init__(self, Old_light):
        #original values
        self.image_location = Old_light.image_location
        self.original_scale = Old_light.original_scale
        self.original_x = Old_light.original_x
        self.original_y = Old_light.original_y
        self.original_angle = Old_light.original_angle
        self.original_shift_x = Old_light.original_shift_x
        self.original_shift_y = Old_light.original_shift_y
        self.original_beam_start = Old_light.original_beam_start
        self.original_beam_scale = Old_light.original_beam_scale
        self.switch = Old_light.switch

        self.on = Old_light.on
        self.display_key = Old_light.display_key

    def load(self, object):
        #original values
        object.image_location = self.image_location
        object.original_scale = self.original_scale
        object.original_x = self.original_x
        object.original_y = self.original_y
        object.original_angle = self.original_angle
        object.original_shift_x = self.original_shift_x
        object.original_shift_y = self.original_shift_y
        object.original_beam_start = self.original_beam_start
        object.original_beam_scale = self.original_beam_scale
        object.switch = self.switch

        object.on = self.on
        object.display_key = self.display_key


class Room_save():
    def __init__(self, room):
        self.load_folder = room.load_folder
        self.room_number = room.room_number
        self.world_objects = [None]*len(room.world_objects)
        for x in range(0, len(self.world_objects)):
            if isinstance(room.world_objects[x], TorchEntity):
                self.world_objects[x] = Torch_Entity_save(room.world_objects[x])
            if isinstance(room.world_objects[x], BatteryEntity):
                self.world_objects[x] = Entity_save(room.world_objects[x])
            if isinstance(room.world_objects[x], KeyEntity):
                self.world_objects[x] = Key_Entity_save(room.world_objects[x])
            if isinstance(room.world_objects[x], Chest):
                self.world_objects[x] = Chest_save(room.world_objects[x])
            if isinstance(room.world_objects[x], Door):
                self.world_objects[x] = Door_save(room.world_objects[x])
            if isinstance(room.world_objects[x], Light):
                self.world_objects[x] = Light_save(room.world_objects[x])


def Save_Game(player, room, load_folder):
    if room.load_folder == -1:
        room.load_folder = load_folder
    room_to_save = Room_save(room)
    address = 'Saves/'
    address += str(room_to_save.load_folder)
    address += '/room'
    pickle.dump(room_to_save, open(address, "wb"))

    address = 'Saves/'
    address += str(room_to_save.load_folder)
    address += '/player'
    player_to_save = Player_save(0, player)
    pickle.dump(player_to_save, open(address, "wb"))

def Load_Game(load_folder):
    address = 'Saves/'
    address += str(load_folder)
    address += '/room'
    original_room = pickle.load(open(address, "rb"))
    if original_room.room_number == 1:
        room = MartyRoom()
    if original_room.room_number == 2:
        room = Hallway()

    world_objects = [None] * len(original_room.world_objects)
    for x in range(0, len(original_room.world_objects)):
        if isinstance(original_room.world_objects[x], Torch_Entity_save):
            for y in range(0,len(room.world_objects)):
                if isinstance(room.world_objects[y], TorchEntity):
                    original_room.world_objects[x].load(room.world_objects[y])
                    original_room.world_objects[x].load_Torch(room.world_objects[y])
                    world_objects[x] = room.world_objects[y]
        elif isinstance(original_room.world_objects[x], Key_Entity_save):
            for y in range(0,len(room.world_objects)):
                if isinstance(room.world_objects[y], KeyEntity):
                    original_room.world_objects[x].load(room.world_objects[y])
                    original_room.world_objects[x].load_Key(room.world_objects[y])
                    world_objects[x] = room.world_objects[y]
        elif isinstance(original_room.world_objects[x], Entity_save):
            for y in range(0,len(room.world_objects)):
                if isinstance(room.world_objects[y], BatteryEntity):
                    original_room.world_objects[x].load(room.world_objects[y])
                    world_objects[x] = room.world_objects[y]
        elif isinstance(room.world_objects[x], Switch):
            world_objects[x] = room.world_objects[x]
            continue
        else:
            original_room.world_objects[x].load(room.world_objects[x])
            world_objects[x] = room.world_objects[x]
            if isinstance(room.world_objects[x], Chest):
                if room.world_objects[x].closed:
                    room.world_objects[x].active_image = [room.world_objects[x].chest_closed, room.world_objects[x].closed_rect.x, room.world_objects[x].closed_rect.y]
                else:
                    room.world_objects[x].active_image = [room.world_objects[x].chest_open, room.world_objects[x].open_rect.x, room.world_objects[x].open_rect.y]

    room.world_objects = world_objects


    address = 'Saves/'
    address += str(load_folder)
    address += '/player'
    original_player = pickle.load(open(address, "rb"))
    if original_player.egg:
        player = PlayerCrab(original_player.rect_x, original_player.rect_y, room.world_factor)
    else:
        player = PlayerMarty(original_player.rect_x, original_player.rect_y, room.world_factor)

    original_player.load(player)

    room.load_folder = load_folder

    return room, player


