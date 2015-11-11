import pygame
pygame.init()

from Options_class import*
from World_Light import Light, Switch
from Controls_class import*

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, collide, collide_sides, width, height, pos_x, pos_y, image, trim_x, trim_y, move_by_trim, rotate, room_factor):
        self.factor = room_factor

        self.collide = collide
        self.collide_sides = collide_sides
        self.trim_x = trim_x
        self.trim_y = trim_y
        self.move_by_trim = move_by_trim
        self.rotate = rotate
        if self.trim_x is None:
            self.trim_x = 0
        if self.trim_y is None:
            self.trim_y = 0
        if self.move_by_trim is None:
            self.move_by_trim = False
        if self.rotate is None:
            self.rotate = 0

        if image is not None:
            width, height = image.get_size()
            self.image = pygame.transform.scale(image, (int(width * self.factor), int(height * self.factor)))
            self.image = pygame.transform.rotate(self.image, self.rotate)
            self.rect = self.image.get_rect()
            self.rect = self.rect.inflate((self.factor * self.trim_x), (self.factor * self.trim_y))
        else:
            self.image = pygame.Surface((width, height))
            self.rect = self.image.get_rect()

        self.rect.x = pos_x
        self.rect.y = pos_y

    def collision(self, marty, dx, dy):
        if self.collide:  # if the obstacle should collide at all
            if pygame.sprite.collide_rect(marty, self):
                if self.collide_sides:  # if the obstacle should collide on sides
                    if dx > 0:  # moving right
                        marty.rect.right = self.rect.left
                    if dx < 0:  # moving left
                        marty.rect.left = self.rect.right
                    if dy < 0:  # moving up
                        marty.rect.top = self.rect.bottom
                        marty.move_y = 1
                if marty.move_y > self.factor * 0.33 and dy > 0:  # moving down
                    marty.rect.bottom = self.rect.top
                    marty.on_floor = True
                    marty.move_y = 0

    def draw(self, main_surface):
        if self.move_by_trim:
            main_surface.blit(self.image, (self.rect.x + (self.trim_x * self.factor), self.rect.y + (self.trim_y * self.factor)))
        else:
            main_surface.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        # this only has an update so we can call an update on all world
        # objects, we could use this update to move the platforms?
        return None


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_pass):
        #original pos
        self.original_factor = 3
        self.original_pos_x = pos_x
        self.original_pos_y = pos_y
        self.original_image = image_pass

        self.factor = self.original_factor * resolution_factor()
        w, h = image_pass.get_size()
        self.image = pygame.transform.scale(self.original_image, (int(w * self.factor), int(h * self.factor)))
        w, h = self.image.get_size()
        self.rect = (w, h)
        self.my_surface = pygame.Surface(self.rect)
        self.rect = self.my_surface.get_rect()
        self.rect.x = self.original_pos_x * resolution_factor()
        self.rect.y = self.original_pos_y * resolution_factor()
        self.move_y = 0
        self.move_x = 0
        self.on_floor = False

    def draw(self, main_surface):
        main_surface.blit(self.image, self.rect)

    def check_collide(self, world_list):
        for x in range(0, len(world_list)):
            if isinstance(world_list[x], Obstacle):
                if world_list[x].collide:
                    if pygame.sprite.collide_rect(world_list[x], self):
                        self.rect.bottom = world_list[x].rect.top
                        self.on_floor = True
                        self.move_y = 0
                        break
                else:
                    self.on_floor = False
    def resize(self):
        self.factor = self.original_factor * resolution_factor()
        w, h = self.original_image.get_size()
        self.image = pygame.transform.scale(self.original_image, (int(w * self.factor), int(h * self.factor)))
        w, h = self.image.get_size()
        self.rect = (w, h)
        self.my_surface = pygame.Surface(self.rect)
        self.rect = self.my_surface.get_rect()
        self.rect.x = self.original_pos_x * resolution_factor()
        self.rect.y = self.original_pos_y * resolution_factor()


    def update(self, world_list):
        gravity(self)
        self.move_y -= 0.26 * self.factor
        self.check_collide(world_list)
        if self.on_floor:
            self.move_y -= 1 * self.factor

        self.rect.x += self.move_x
        self.rect.y += self.move_y


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, room_factor):
        #original values
        self.original_pos_x = pos_x
        self.original_pos_y = pos_y

        self.factor = room_factor

        self.items = [None, None]

        # load images
        self.original_chest_open = pygame.image.load("Images/world_design/chest/chest_open.png")
        self.original_chest_closed = pygame.image.load("Images/world_design/chest/chest_closed.png")

        # resize images
        ow, oh = self.original_chest_open.get_size()
        cw, ch = self.original_chest_closed.get_size()
        self.chest_open = pygame.transform.scale(self.original_chest_open, (int(ow * self.factor), int(oh * self.factor)))
        self.chest_closed = pygame.transform.scale(self.original_chest_closed, (int(cw * self.factor), int(ch * self.factor)))

        # create rect of images
        self.open_rect = self.chest_open.get_rect()
        self.closed_rect = self.chest_closed.get_rect()
        self.open_rect.x = pos_x *resolution_factor()
        self.open_rect.y = pos_y*resolution_factor() - (3 * self.factor)
        self.closed_rect.x = pos_x*resolution_factor()
        self.closed_rect.y = pos_y*resolution_factor()

        self.active_image = [self.chest_closed, self.closed_rect.x, self.closed_rect.y]
        self.rect = self.active_image[0].get_rect()
        self.rect.x = self.active_image[1]
        self.rect.y = self.active_image[2]
        self.closed = True
        self.display_key = False
        self.key = pygame.key.name(controls.interact)

    def throw_to_world(self, world_list):
        for x in range(0, len(self.items)):
            if self.items[x] is not None:
                if self.items[x] == "Battery":
                    battery = Entity(self.x + 50, self.y - 50, "Battery")
                    world_list.append(battery)

    def toggle(self):
        if self.closed:
            sound = pygame.mixer.Sound('Sounds/open_chest.wav')
            channel = sound.play(0, 0, 0)
            sound.set_volume(float(options.world_volume)/100)
            channel.set_volume(float(options.master_volume)/100)

            self.active_image = [self.chest_open, self.open_rect.x, self.open_rect.y]
            self.closed = False
        else:
            sound = pygame.mixer.Sound('Sounds/close_chest.wav')
            channel = sound.play(0, 0, 0)
            sound.set_volume(float(options.world_volume)/100)
            channel.set_volume(float(options.master_volume)/100)

            self.active_image = [self.chest_closed, self.closed_rect.x, self.closed_rect.y]
            self.closed = True

        self.rect = self.active_image[0].get_rect()
        self.rect.x = self.active_image[1]
        self.rect.y = self.active_image[2]

    def interact(self):
        self.toggle()

    def draw(self, main_surface):
        main_surface.blit(self.active_image[0], (self.active_image[1], self.active_image[2]))
        if self.display_key:
            font = pygame.font.SysFont("", int(30*resolution_factor()))
            letter = font.render("press {0}".format(self.key), True, (0, 0, 0))
            main_surface.blit(letter, (self.active_image[1] + -9*resolution_factor(), self.active_image[2] - 60*resolution_factor()))

    def resize(self, room_factor):
        self.factor = room_factor

        # resize images
        ow, oh = self.original_chest_open.get_size()
        cw, ch = self.original_chest_closed.get_size()
        self.chest_open = pygame.transform.scale(self.original_chest_open, (int(ow * self.factor), int(oh * self.factor)))
        self.chest_closed = pygame.transform.scale(self.original_chest_closed, (int(cw * self.factor), int(ch * self.factor)))

        # create rect of images
        self.open_rect = self.chest_open.get_rect()
        self.closed_rect = self.chest_closed.get_rect()
        self.open_rect.x = self.original_pos_x *resolution_factor()
        self.open_rect.y = self.original_pos_y *resolution_factor() - (3 * self.factor)
        self.closed_rect.x = self.original_pos_x *resolution_factor()
        self.closed_rect.y = self.original_pos_y *resolution_factor()

        if self.closed:
            self.active_image = [self.chest_closed, self.closed_rect.x, self.closed_rect.y]
        else:
            self.active_image = [self.chest_open, self.open_rect.x, self.open_rect.y]

        self.rect = self.active_image[0].get_rect()
        self.rect.x = self.active_image[1]
        self.rect.y = self.active_image[2]

    def update(self):
        return None


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, key_code):
        #original position
        self.original_pos_x = pos_x
        self.original_pos_y = pos_y
        self.original_factor = 3

        factor = self.original_factor * resolution_factor()
        self.door_closed = pygame.Surface((2 * factor, 60 * factor))
        self.door_closed.fill((255, 255, 255))
        self.rect_closed = self.door_closed.get_rect()
        self.rect_closed.x = self.original_pos_x*resolution_factor()
        self.rect_closed.y = self.original_pos_y*resolution_factor()

        self.door_open = pygame.Surface((20 * factor, 60 * factor))
        self.door_open.fill((255, 255, 255))
        self.rect_open = self.door_open.get_rect()

        self.rect_open.x = self.original_pos_x*resolution_factor()
        self.rect_open.y = self.original_pos_y*resolution_factor()

        self.closed = True
        self.active = [self.door_closed, self.rect_closed]
        self.rect = self.active[1]

        self.key_code = key_code

    def toggle(self):
        if self.closed:
            self.active = [self.door_open, self.rect_open]
            self.closed = False
        else:
            self.active = [self.door_closed, self.rect_closed]
            self.closed = True

        self.rect = self.active[1]

    def draw(self, main_surface):
        main_surface.blit(self.active[0], self.rect)
        door_font = pygame.font.SysFont("Bebas", int(20*resolution_factor()))
        Text = door_font.render("DOOR".format(), True, (255, 255, 255))
        main_surface.blit(Text, (self.rect.x, self.rect.y))

    def resize(self):
        factor = 3*resolution_factor()
        self.door_closed = pygame.Surface((2 * factor, 60 * factor))
        self.door_closed.fill((255, 255, 255))
        self.rect_closed = self.door_closed.get_rect()
        self.rect_closed.x = self.original_pos_x*resolution_factor()
        self.rect_closed.y = self.original_pos_y*resolution_factor()

        self.door_open = pygame.Surface((20 * factor, 60 * factor))
        self.door_open.fill((255, 255, 255))
        self.rect_open = self.door_open.get_rect()

        self.rect_open.x = self.original_pos_x*resolution_factor()
        self.rect_open.y = self.original_pos_y*resolution_factor()

        if self.closed:
            self.active = [self.door_closed, self.rect_closed]
        else:
            self.active = [self.door_open, self.rect_open]

        self.rect = self.active[1]

    def update(self):
        # another pointless update but again we could update the image for
        # the door to open/close in this update function
        return None


def gravity(sprite_object):
    sprite_object.move_y += 0.33 * 3 * resolution_factor()


def draw_world(main_surface, world_objects, world_decorations, dark):
    for x in range(0, len(world_decorations)):
        world_decorations[x].draw(main_surface)
    for x in range(0, len(world_objects)):
        if isinstance(world_objects[x], Light):
            world_objects[x].draw_image(main_surface)
            world_objects[x].draw_light(dark)
        else:
            world_objects[x].draw(main_surface)



def update_world(world_objects, world_decorations):
    for x in range (0, len(world_decorations)):
        world_decorations[x].update()
    for x in range(0, len(world_objects)):
        if isinstance(world_objects[x], Entity):
            world_objects[x].update(world_decorations)
        else:
            if not isinstance(world_objects[x], Light):
                world_objects[x].update()