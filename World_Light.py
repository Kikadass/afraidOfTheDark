import pygame
pygame.init()
from Options_class import*
from Rotation import rotate_polygon
from Controls_class import*
pygame.mixer.pre_init(22050, -16, 2, 512)

class Light(pygame.sprite.Sprite):
    def __init__(self, image_pass, x_pos, y_pos, angle, shift_x, shift_y, beam_start, beam_scale, scale, switch):
        #original values
        self.image_location = image_pass
        self.image_pass = pygame.image.load(self.image_location)
        self.original_scale = scale
        self.original_x = x_pos
        self.original_y = y_pos
        self.original_angle = angle
        self.original_shift_x = shift_x
        self.original_shift_y = shift_y
        self.original_beam_start = beam_start
        self.original_beam_scale = beam_scale
        self.switch = switch

        w, h = self.image_pass.get_size()
        self.image = pygame.transform.scale(self.image_pass, (int(w * scale*resolution_factor()), int(h * scale*resolution_factor())))

        self.x = x_pos*resolution_factor()
        self.y = y_pos*resolution_factor()
        self.beam = [
            (0 + self.x + shift_x*resolution_factor(), beam_start*resolution_factor() + self.y + shift_y*resolution_factor()),
            (0 + self.x + shift_x*resolution_factor(), 0 + self.y + shift_y*resolution_factor()),
            (1500*resolution_factor() + self.x + shift_x*resolution_factor(), -beam_scale*beam_start*resolution_factor() + self.y + shift_y*resolution_factor()),
            (1500*resolution_factor() + self.x + shift_x*resolution_factor(), beam_scale*beam_start*resolution_factor() + self.y + shift_y*resolution_factor())
        ]
        self.beam = rotate_polygon(self.beam, angle, self.beam[0])
        self.on = True
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.display_key = False
        self.key = pygame.key.name(controls.interact)

    def toggle(self):
        self.on = not self.on

    def interact(self):
        if not self.switch:
            self.toggle()
            sound = pygame.mixer.Sound('Sounds/switch.wav')
            channel = sound.play(0, 0, 0)
            sound.set_volume(float(options.world_volume)/100)
            channel.set_volume(float(options.master_volume)/100)

    def draw_image(self, main_surface):
        main_surface.blit(self.image, (self.x, self.y))
        if not self.switch:
            if self.display_key:
                font = pygame.font.SysFont("", int(30*resolution_factor()))
                letter = font.render("press {0}".format(self.key), True, (0, 0, 0))
                main_surface.blit(letter, (self.x + -9*resolution_factor(), self.y - 60*resolution_factor()))

    def draw_light(self, dark):
        if self.on:
            pygame.draw.polygon(dark, (0, 0, 0, 0), self.beam)

    def resize(self):
        w, h = self.image_pass.get_size()
        self.image = pygame.transform.scale(self.image_pass, (int(w * self.original_scale*resolution_factor()), int(h * self.original_scale*resolution_factor())))

        self.x = self.original_x*resolution_factor()
        self.y = self.original_y*resolution_factor()
        self.beam = [
            (0 + self.x + self.original_shift_x*resolution_factor(), self.original_beam_start*resolution_factor() + self.y + self.original_shift_y*resolution_factor()),
            (0 + self.x + self.original_shift_x*resolution_factor(), 0 + self.y + self.original_shift_y*resolution_factor()),
            (1500*resolution_factor() + self.x + self.original_shift_x*resolution_factor(), -self.original_beam_scale*self.original_beam_start*resolution_factor() + self.y + self.original_shift_y*resolution_factor()),
            (1500*resolution_factor() + self.x + self.original_shift_x*resolution_factor(), self.original_beam_scale*self.original_beam_start*resolution_factor() + self.y + self.original_shift_y*resolution_factor())
        ]
        self.beam = rotate_polygon(self.beam, self.original_angle, self.beam[0])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        return None


class Switch():
    def __init__(self, x_pos, y_pos, light, room_factor):
        #original values
        self.original_image = pygame.image.load("Images/world_design/decoration/LightSwitch.png")
        self.original_x_pos = x_pos
        self.original_y_pos = y_pos

        w, h = self.original_image.get_size()
        self.image = pygame.transform.scale(self.original_image, (int(w * room_factor), int(h * room_factor)))
        self.rect = self.image.get_rect()
        self.rect.x = x_pos*resolution_factor()
        self.rect.y = y_pos*resolution_factor()
        self.light_object = light
        self.display_key = False
        self.key = pygame.key.name(controls.interact)

    def interact(self):
        self.light_object.toggle()

    def draw(self, main_surface):
        main_surface.blit(self.image, (self.rect.x, self.rect.y))
        if self.display_key:
            font = pygame.font.SysFont("", int(30*resolution_factor()))
            letter = font.render("press {0}".format(self.key), True, (0, 0, 0))
            main_surface.blit(letter, (self.rect.x + -9*resolution_factor(), self.rect.y - 60*resolution_factor()))

    def resize(self, room_factor):
        w, h = self.original_image.get_size()
        self.image = pygame.transform.scale(self.original_image, (int(w * room_factor), int(h * room_factor)))
        self.rect = self.image.get_rect()
        self.rect.x = self.original_x_pos*resolution_factor()
        self.rect.y = self.original_y_pos*resolution_factor()

    def update(self):
        return None