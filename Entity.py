import pygame
pygame.init()
from World import*

class TorchEntity(Entity):
    def __init__(self, pos_x, pos_y, battery):
        self.battery = battery
        image = pygame.image.load("Images/objects/Torch.png")
        super(TorchEntity, self).__init__(pos_x, pos_y, image)


class KeyEntity(Entity):
    def __init__(self, pos_x, pos_y, door_code):
        image = pygame.image.load("Images/objects/Key.png")
        self.door_code = door_code
        super(KeyEntity, self).__init__(pos_x, pos_y, image)


class BatteryEntity(Entity):
    def __init__(self, pos_x, pos_y):
        image = pygame.image.load("Images/objects/Battery.png")
        super(BatteryEntity, self).__init__(pos_x, pos_y, image)