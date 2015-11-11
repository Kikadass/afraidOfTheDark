import pygame
pygame.init()

from Entity import*
from Item import*
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, arm, room_factor):
        self.factor = room_factor

        # image resize and flip for left/right
        self.image_right = image
        w, h = self.image_right.get_size()
        self.image_right = pygame.transform.scale(self.image_right, ((int(w * self.factor), int(h * self.factor))))
        self.image_left = pygame.transform.flip(self.image_right, True, False)

        # create rect from image and remove the sides
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-(self.factor*8), 0)

        # inventory list and hand
        self.inventory = [None, None, None]
        self.hand_number = 0
        self.in_hand = self.inventory[self.hand_number]

        # arm
        self.sign = -1
        self.start_arm_x = arm[0]
        self.start_arm_y = arm[1]
        self.arm_x = arm[0]
        self.arm_y = arm[1]
        self.arm_angle = 0

        # other stuff
        self.right = True
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.on_floor = False
        self.move_x = 0
        self.move_y = 0
        self.inv_temp = 0
        self.inv_on = True
        self.breath = 100
        self.interact = False

    def toggle_inventory(self):
        if self.inv_temp == 0:
            self.inv_on = not self.inv_on

    def set_hand(self, number):
        self.hand_number = number
        self.in_hand = self.inventory[self.hand_number]

    def drop_hand(self, world_list):
        # drop the equivalent item
        if self.right:
            drop_x, drop_y = self.rect.right*inv_resolution_factor() + 1, 22
        else:
            drop_x, drop_y = self.rect.left*inv_resolution_factor() - 40, 22

        if isinstance(self.inventory[self.hand_number], Torch):
            new_entity = TorchEntity(drop_x, self.rect.top*inv_resolution_factor() + drop_y, self.inventory[self.hand_number].battery)
            world_list.append(new_entity)
        else:
            if isinstance(self.inventory[self.hand_number], Key):
                door_code = self.inventory[self.hand_number].door_code
                new_entity = KeyEntity(drop_x, self.rect.top + drop_y, door_code)
                world_list.append(new_entity)

        # remove the dropped item from the inventory
        self.inventory[self.hand_number] = None

    def add_to_inventory(self, new_object):
        for x in range(0, len(self.inventory)):
            if self.inventory[x] is None:
                if isinstance(new_object, TorchEntity):
                    torch = Torch(0, 0, new_object.battery, True)
                    self.inventory[x] = torch
                if isinstance(new_object, Axe):
                    axe = Axe(0, 0)
                    self.inventory[x] = axe
                if isinstance(new_object, KeyEntity):
                    key = Key(0, 0, new_object.door_code)
                    self.inventory[x] = key
                break

    def display_inventory(self, main_surface):
        my_surface_un = pygame.Surface((85*resolution_factor(), 85*resolution_factor()))
        my_surface_sel = pygame.Surface((85*resolution_factor(), 85*resolution_factor()))
        my_surface_selBack = pygame.Surface((75*resolution_factor(), 75*resolution_factor()))

        my_surface_selBack.fill((50, 50, 50))
        my_surface_un.fill((50, 50, 50))
        my_surface_sel.fill((250, 250, 250))


        unselected = my_surface_un
        selected = my_surface_sel
        back = my_surface_selBack

        if self.hand_number == 0:
            main_surface.blit(selected, (960*resolution_factor(), 18*resolution_factor()))
            main_surface.blit(back, (965*resolution_factor(), 23*resolution_factor()))

        else:
            main_surface.blit(unselected, (960*resolution_factor(), 18*resolution_factor()))

        if self.hand_number == 1:
            main_surface.blit(selected, (1065*resolution_factor(), 18*resolution_factor()))
            main_surface.blit(back, (1070*resolution_factor(), 23*resolution_factor()))
        else:
            main_surface.blit(unselected, (1065*resolution_factor(), 18*resolution_factor()))

        if self.hand_number == 2:
            main_surface.blit(selected, (1170*resolution_factor(), 18*resolution_factor()))
            main_surface.blit(back, (1175*resolution_factor(), 23*resolution_factor()))
        else:
            main_surface.blit(unselected, (1170*resolution_factor(), 18*resolution_factor()))

        for x in range(0, len(self.inventory)):
            if self.inventory[x] is not None:
                main_surface.blit(self.inventory[x].icon, (960*resolution_factor() + (x * 105*resolution_factor()), 20*resolution_factor()))

    def jump(self):
        if self.on_floor:
            self.move_y -= 5 * self.factor

    def move_collide(self, dx, dy, world_objects):
        self.rect.x += dx
        self.rect.y += dy
        x = 0
        self.interact = False
        while x < len(world_objects):
            if isinstance(world_objects[x], Obstacle):
                world_objects[x].collision(self, dx, dy)
            else:
                if isinstance(world_objects[x], Entity):
                    if pygame.sprite.collide_rect(self, world_objects[x]):
                        if isinstance(world_objects[x], BatteryEntity):
                            for y in range(0, len(self.inventory)):
                                if isinstance(self.inventory[y], Torch):
                                    self.inventory[y].battery += 30
                                    if self.inventory[y].battery > 100:
                                        self.inventory[y].battery = 100
                            del world_objects[x]
                        else:
                            self.add_to_inventory(world_objects[x])
                            del world_objects[x]
                else:
                    if isinstance(world_objects[x], Door):
                        if pygame.sprite.collide_rect(self, world_objects[x]):
                            if isinstance(self.in_hand, Key):
                                if self.in_hand.door_code == world_objects[x].key_code:
                                    print("The right key is in hand")
                    else:
                        if isinstance(world_objects[x], Chest) or isinstance(world_objects[x], Light) or isinstance(world_objects[x], Switch):
                            if pygame.sprite.collide_rect(self, world_objects[x]):
                                world_objects[x].display_key = True
                                self.interact = True
                            else:
                                world_objects[x].display_key = False

            x += 1

        if self.move_y != 0:
            self.on_floor = False

    def walk_or_sprint(self, walk, direction, world_list):
        # walk is true or false, if not true then sprint, direction is 1(right) or -1(Left)
        if walk:
            self.move_collide(direction * 2*resolution_factor(), 0, world_list)
        else:  # (sprint)
            if self.breath > 1:  # only if he has breath
                self.move_collide(direction * 5*resolution_factor(), 0, world_list)
                self.breath -= 0.3
            else:
                self.breath = 0
                self.move_collide(direction * 2*resolution_factor(), 0, world_list)

    def solve_arm_angle(self):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        mouse_pos_x -= 16 * self.factor
        mouse_pos_y -= 20 * self.factor
        dy = mouse_pos_y - self.rect.y
        dx = mouse_pos_x - self.rect.x
        theta = math.atan2(dy, dx)
        theta *= 180/math.pi
        self.arm_angle = theta

    def draw_player_info(self, main_surface):
        if self.inv_on:
            self.display_inventory(main_surface)
        if self.in_hand is not None:
            if isinstance(self.in_hand, Torch):
                self.in_hand.draw_indicator(main_surface)

    def try_interact(self, world_list):
        if self.interact:
            for x in range(0, len(world_list)):
                if isinstance(world_list[x], Chest) or isinstance(world_list[x], Light) or isinstance(world_list[x], Switch) or isinstance(world_list[x], Door):
                    if pygame.sprite.collide_rect(self, world_list[x]):
                        world_list[x].interact()

    def draw(self, main_surface, darkness):
        main_surface.blit(self.image, (self.rect.x - (self.factor*4), self.rect.y))
        if self.in_hand is not None:
            if isinstance(self.in_hand, Torch):
                self.in_hand.draw(main_surface, self.arm_angle, self.sign, darkness)
            else:
                self.in_hand.draw(main_surface, self.arm_angle, self.sign)

    def update(self, frame):
        if self.in_hand is not None:
            if isinstance(self.in_hand, Torch):
                self.in_hand.update(frame, (self.arm_x, self.arm_y))
            else:
                self.in_hand.update((self.arm_x, self.arm_y))

        if self.breath > 100:
            self.breath = 100

        self.solve_arm_angle()

        if self.arm_angle < 60 and self.arm_angle > -60:
            self.right = True

        if self.arm_angle < -120 or self.arm_angle > 120:
            self.right = False

        if self.right:
            self.image = self.image_right
            self.arm_x = self.start_arm_x
            self.arm_y = self.start_arm_y
            self.sign = -1

        else:
            self.image = self.image_left
            self.arm_x = -self.start_arm_x
            self.arm_y = self.start_arm_y
            self.arm_angle = -self.arm_angle
            self.sign = 1

        self.arm_x, self.arm_y = self.rect.x + self.arm_x, self.rect.y + self.arm_y


class PlayerMarty(Player):
    def __init__(self, pos_x, pos_y, room_factor):
        image = pygame.image.load("Images/guy/Guy1.png")
        arm = (10*resolution_factor(), 30*resolution_factor())
        super(PlayerMarty, self).__init__(pos_x, pos_y, image, arm, room_factor)


class PlayerCrab(Player):
    def __init__(self, pos_x, pos_y, room_factor):
        image = pygame.image.load("BlueCrab.png")
        arm = (20*resolution_factor(), -5*resolution_factor())
        super(PlayerCrab, self).__init__(pos_x, pos_y, image, arm, room_factor)
