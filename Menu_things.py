import pygame
from pygame.locals import *
pygame.init()

import webbrowser
import random


def flicker_light(light_object):
    if random.randint(0, 100) < 1:
        light_object.toggle()


def limit_options(options_count, option_selected):
    if option_selected > options_count:
        return 0

    if option_selected < 0:
        return options_count

    return option_selected


def display_menu(main_surface, options_font, options_list, option_selected, resolution_factor):
    for x in range(len(options_list)):
        if x == option_selected:
            option = options_font.render("{0}".format(options_list[x]), True, (255, 255, 255))
            main_surface.blit(option, (60*resolution_factor, 20*resolution_factor + (80 * x*resolution_factor)))
        else:
            option = options_font.render("{0}".format(options_list[x]), True, (20, 112, 162))
            main_surface.blit(option, (30*resolution_factor, 20*resolution_factor + (80 * x*resolution_factor)))


def display_title_logo(main_surface, font, logo, resolution_factor):
    title = font.render("AFRAID OF THE DARK", True, (255, 255, 255))
    main_surface.blit(title, (450*resolution_factor, 500*resolution_factor))
    main_surface.blit(logo, (30*resolution_factor, 575*resolution_factor))

def credits():
    print("CREDITS")


def youtube():
    new = 2 # open in a new tab, if possible
    url = "https://www.youtube.com/channel/UCmoPoyh-bRjmdOpplEYZEDg"
    webbrowser.open(url,new=new)


def blog():
    new = 2 # open in a new tab, if possible
    url = "http://aaronnebbs.com/"
    webbrowser.open(url,new=new)


def display_wall(options, main_surface):
    factor = 5
    wall = pygame.image.load("Images/Wall.png")
    w, h = wall.get_size()
    w *= factor
    h *= factor
    wall = pygame.transform.scale(wall, (w, h))
    for x in range(0, int(options.resolution*16/9), w):
        for y in range(0, options.resolution, h):
            main_surface.blit(wall, (x, y))


def display_options(main_surface, options_font, options_list, option_selected, resolution_factor):
    for x in range(len(options_list)):
        if x == option_selected:
            option = options_font.render("{0}".format(options_list[x]), True, (255, 255, 255))
            main_surface.blit(option, (60*resolution_factor, 100*resolution_factor + (80 * x*resolution_factor)))
        else:
            option = options_font.render("{0}".format(options_list[x]), True, (20, 112, 162))
            main_surface.blit(option, (30*resolution_factor, 100*resolution_factor + (80 * x*resolution_factor)))


def update_menu(options, main_surface, left_light, mid_light, right_light, dark, menu, options_list, resolution_factor, option_selected):

    main_surface.fill((0, 200, 255))

    display_wall(options, main_surface)

    left_light.draw_image(main_surface)
    mid_light.draw_image(main_surface)
    right_light.draw_image(main_surface)

    if menu == 0:
        title_font = pygame.font.SysFont("Bebas", int(80*resolution_factor))
        blue_crab = pygame.image.load("BlueCrab.png")
        w, h = blue_crab.get_size()
        blue_crab = pygame.transform.scale(blue_crab, (int(w * 10*resolution_factor), int(h * 10*resolution_factor)))
        display_title_logo(main_surface, title_font, blue_crab, resolution_factor)

    if menu == 2:
        options_font = pygame.font.SysFont("Bebas", int(60*resolution_factor))
        display_options(main_surface, options_font, options_list, option_selected, resolution_factor)

    dark.fill((0, 0, 0, 200))

    left_light.draw_light(dark)
    mid_light.draw_light(dark)
    right_light.draw_light(dark)

    main_surface.blit(dark, (0, 0))


def double_click(click_time, frame_count, double_click_speed):
    if click_time == -1:
        if frame_count > 600-double_click_speed:
            click_time = frame_count - 600
        else:
            click_time = frame_count
    else:
        click_time = frame_count - click_time
    if click_time >= double_click_speed:
        if frame_count > 600-double_click_speed:
            click_time = frame_count - 600
        else:
            click_time = frame_count
    if click_time < double_click_speed and click_time > -1:
        click_time = -1
        return 1, click_time
    else:
        return 0, click_time


def read_file(file, list):
    for x in range(0, len(list)):
        s = ''
        character = file.read(1)

        while character != ':':
            character = file.read(1)
        character = file.read(1)
        character = file.read(1)

        while character != '\n':
            s = str(s) + character
            character = file.read(1)
        s = s.strip('\r').strip('\n')
        list[x] = s
    file.closed

    return list