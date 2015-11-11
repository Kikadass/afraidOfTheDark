import pygame
import random
from abc import ABCMeta
from Rotation import rotate_polygon
from Options_class import*
pygame.init()

class Item():
    __metaclass__ = ABCMeta

    def __init__(self, pos_x, pos_y, image_pass, image_icon_pass):
        self.image = image_pass
        self.icon = image_icon_pass
        self.x, self.y = (pos_x, pos_y)

    def item_draw(self, main_surface, angle, sign):
        temp_image = pygame.transform.rotate(self.image, sign * angle)
        rect = temp_image.get_rect()
        main_surface.blit(temp_image, (self.x + 10*resolution_factor() +(rect[0]-(rect.width/2)), (self.y + 13*resolution_factor() + (rect[1]-(rect.height/2)))))

    def item_update(self, pos):
        self.x, self.y = pos


class Torch(Item):
    def __init__(self, pos_x, pos_y, battery_level, is_on):
        self.factor = 3*resolution_factor()
        self.icon_factor = 5*resolution_factor()
        self.battery = battery_level
        self.brightness = 2
        self.on = is_on
        self.batTemp = 0                # is it necessary?
        self.flicker = False
        self.frame = 0                  # is it necessary?

        self.beam_coordinates = [
            (0, 0),
            (0, -5*resolution_factor()),
            ((100 * 5*resolution_factor()), (-50 * 5*resolution_factor())),
            ((100 * 5*resolution_factor()), (50 * 5*resolution_factor())),
            (0, 5*resolution_factor())
        ]
        self.light_list = []

        # Load all images of Torch
        self.torch_image = pygame.image.load("Images/Objects/Torch.png")
        self.torch_icon = pygame.image.load("Images/Icons/Torch.png")
        self.battery_image = pygame.image.load("Images/Battery.png")

        # Record width and height of all images
        w1, h1 = self.torch_image.get_size()
        w2, h2 = self.torch_icon.get_size()
        w3, h3 = self.battery_image.get_size()

        # Scale all images by factor
        self.torch_image = pygame.transform.scale(self.torch_image, (int(w1 * self.factor), int(h1 * self.factor)))
        self.torch_icon = pygame.transform.scale(self.torch_icon, (int(w2 * self.icon_factor), int(h2 * self.icon_factor)))
        self.battery_image = pygame.transform.scale(self.battery_image, (int(w3 * self.icon_factor), int(h3 * self.icon_factor)))

        # Define the battery level icon
        self.battery_rect = self.battery_image.get_rect()
        self.battery_rect.x = 20
        self.battery_rect.y = 20

        self.battery_cell = pygame.Surface((7 * self.icon_factor, 11 * self.icon_factor))
        self.battery_cell.fill((255, 255, 255))
        self.cell_rect = self.battery_cell.get_rect()
        self.cell_rect.x = 3 * self.icon_factor
        self.cell_rect.y = 3 * self.icon_factor

        # Call to the super class constructor Item
        super(Torch, self).__init__(pos_x, pos_y, self.torch_image, self.torch_icon)

    def torch_flicker_1(self):
            if random.randint(0, 500) < 1:
                self.flicker = True
                self.frame = 0

    def torch_flicker_2(self):
            if random.randint(0, 450) < 1:
                self.flicker = True
                self.frame = 0

    def torch_flicker_3(self):
            if random.randint(0, 50) < 1:
                self.flicker = True
                self.frame = 0

    def alter_brightness(self, positive_negative):
        if ((self.brightness + 1 * positive_negative) < 3) and ((self.brightness + 1 * positive_negative) > 0):
            self.brightness += 1 * positive_negative

    def toggle(self):
        if self.batTemp == 0:
            self.on = not self.on
            return not self.on

    def draw(self, main_surface, angle, sign, dark):
        super(Torch, self).item_draw(main_surface, angle, sign)
        if self.on:
            pygame.draw.polygon(dark, (0, 0, 0, 0), (rotate_polygon(self.light_list, (-sign * angle), (self.light_list[0][0] - 15*resolution_factor(), self.light_list[0][1]))))

    def draw_indicator(self, main_surface):
        main_surface.blit(self.battery_image, self.battery_rect)

        cell_count = 0
        if self.battery > 0:
            cell_count += 1
        if self.battery > 33:
            cell_count += 1
        if self.battery > 66:
            cell_count += 1

        for x in range(0, cell_count):
            main_surface.blit(self.battery_cell, (((8 * self.icon_factor) * x) + (self.battery_rect.x + self.cell_rect.x), self.battery_rect.y + self.cell_rect.y))

    def update(self, frame, pos):
        super(Torch, self).item_update(pos)

        del self.light_list[:]
        self.light_list.append((self.beam_coordinates[0][0] + pos[0] + 25*resolution_factor(), self.beam_coordinates[0][1] + pos[1] + 12*resolution_factor()))
        self.light_list.append((self.beam_coordinates[1][0] + pos[0] + 25*resolution_factor(), self.beam_coordinates[1][1] + pos[1] + 12*resolution_factor()))
        self.light_list.append((self.beam_coordinates[2][0] + pos[0] + 25*resolution_factor(), self.beam_coordinates[2][1] + pos[1] + 12*resolution_factor()))
        self.light_list.append((self.beam_coordinates[3][0] + pos[0] + 25*resolution_factor(), self.beam_coordinates[3][1] + pos[1] + 12*resolution_factor()))

        if self.on:
            if self.battery > 80:
                self.torch_flicker_1()
            else:
                if 40 < self.battery < 80:
                    self.torch_flicker_2()
                else:
                    self.torch_flicker_3()

        if self.flicker:
            self.frame += 1
            if self.frame < 60:
                if random.randint(0, 7) < 1:
                    self.toggle()
            else:
                self.on = True
                self.flicker = False

        if self.battery > 0:
            if frame == 0:
                if self.on:
                    self.battery -= 1 * self.brightness
        else:
            self.battery = 0
            self.on = False


class Axe(Item):
    def __init__(self, pos_x, pos_y):
        self.factor = 3*resolution_factor()

        # Load all images of Axe
        self.axe_image = pygame.image.load("Images/Objects/Axe.png")
        self.axe_icon = pygame.image.load("Images/Icons/Axe.png")

        # Record width and height of all images
        w1, h1 = self.axe_image.get_size()
        w2, h2 = self.axe_icon.get_size()

        # Scale all images by factor
        self.axe_image = pygame.transform.scale(self.axe_image, (w1 * self.factor, h1 * self.factor))
        self.axe_icon = pygame.transform.scale(self.axe_icon, (w2 * self.factor, h2 * self.factor))

        # Call to the super class constructor Item
        super(Axe, self).__init__(pos_x, pos_y, self.axe_image, self.axe_icon)


class Key(Item):
    def __init__(self, pos_x, pos_y, door_code):
        self.factor = 3*resolution_factor()
        self.icon_factor = 5*resolution_factor()
        self.door_code = door_code

        # Load all images of Key
        self.key_image = pygame.image.load("Images/Objects/Key.png")
        self.key_icon = pygame.image.load("Images/Icons/Key.png")

        # Record width and height of all images
        w1, h1 = self.key_image.get_size()
        w2, h2 = self.key_icon.get_size()

        # Scale all images by factor
        self.key_image = pygame.transform.scale(self.key_image, (int(w1 * self.factor), int(h1 * self.factor)))
        self.key_icon = pygame.transform.scale(self.key_icon, (int(w2 * self.icon_factor), int(h2 * self.icon_factor)))

        # Call to the super class constructor Item
        super(Key, self).__init__(pos_x, pos_y, self.key_image, self.key_icon)

    def draw(self, main_surface, angle, sign):
        super(Key, self).item_draw(main_surface, angle, sign)

    def update(self, pos):
        super(Key, self).item_update(pos)
