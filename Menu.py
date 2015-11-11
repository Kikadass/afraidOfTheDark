import pygame
import os
import Tkinter
pygame.init()

from Options import*
from World_Light import Light
from GameLoop import game_loop
from Levels import *
from Controls import*
from Save_class import*

def create_player(egg, room_factor):
    if egg:
        marty = PlayerCrab(120*resolution_factor(), 400*resolution_factor(), room_factor)
    else:
        marty = PlayerMarty(120*resolution_factor(), 400*resolution_factor(), room_factor)
    marty.in_hand = None
    return marty

class ERROR():
    def __init__(self, master):
        self.master = master
        try:
            geometry  = '170x50'
            x = int(800*resolution_factor())
            y = int(500*resolution_factor())
            geometry = geometry + '+' + str(x) + '+' + str(y)
            self.master.geometry(geometry)
            self.master.title('ERROR')

            self.label = Tkinter.Label(self.master, text = 'That slot has already been used', fg = 'black').grid(row = 0, column = 2)
            self.button = Tkinter.Button(self.master, text = "OK", fg = 'blue', command = self.finish).grid(row = 1, column = 2)
        except StandardError:
            pass

    def finish(self):
        self.master.destroy()

def error_message():
    try:
        root = Tkinter.Tk()
        the_window = ERROR(root)
        root.mainloop()
    except StandardError:
        pass

def load_game_menu(main_surface, left_light, mid_light, right_light, dark, option_selected):
    #define list of options
    options_list = [None]*2
    address = 'Languages/Saves/'
    address += options.language
    options_file = open(address, 'r')
    options_list = read_file(options_file, options_list)

    #define list of sub_options
    sub_options_list = [None]*10
    options_count = len(sub_options_list) - 1
    sub_option_selected = 0


    clock = pygame.time.Clock()
    frame_count = 0
    click_time = -1
    double_click_speed = 20

    running = True
    while running:
        address = 'Saves/List.txt'
        options_file = open(address, 'r')
        sub_options_list = read_file(options_file, sub_options_list)

        clock.tick(60)
        frame_count += 1
        if frame_count == 600:
            frame_count = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_w] or key[pygame.K_UP]:
            sub_option_selected -= 1
            time.sleep(0.1)
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            sub_option_selected += 1
            time.sleep(0.1)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                    start(0)
                if e.key == K_KP_ENTER or e.key == K_RETURN:
                    running = False
                    #if continue game:
                    if option_selected:
                        address = 'Saves/'
                        address += str(sub_option_selected)
                        address += '/room'
                        if not os.path.isfile(address):
                            print "NO SE PUEE"
                            running = False
                            load_game_menu(main_surface, left_light, mid_light, right_light, dark, option_selected)

                        else:
                            room,marty = Load_Game(sub_option_selected)
                            game_loop(0, marty, room)

                    #if new game:
                    else:
                        address = 'Saves/'
                        address += str(sub_option_selected)
                        address += '/room'
                        if os.path.isfile(address):
                            print "NO SE PUEE"
                            running = False
                            #error_message()
                            load_game_menu(main_surface, left_light, mid_light, right_light, dark, option_selected)

                        else:
                            print "Si se puee"
                            room = MartyRoom()
                            marty = create_player(0, room.world_factor)
                            Save_Game(marty, room, sub_option_selected)
                            game_loop(0, marty, room)

            mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
            if mouse_pos_x > 730*resolution_factor() and mouse_pos_x < 900*resolution_factor():
                for x in range(0, len(sub_options_list), 1):
                    if mouse_pos_y > (250*resolution_factor()+50*x*resolution_factor()) and mouse_pos_y < (300*resolution_factor()+50*x*resolution_factor()):
                        sub_option_selected = x
                        if e.type == MOUSEBUTTONDOWN:
                            is_it, click_time = double_click(click_time, frame_count, double_click_speed)
                            if is_it:
                                running = False
                                #if continue game:
                                if option_selected:
                                    room,marty = Load_Game(sub_option_selected)
                                    game_loop(0, marty, room)

                                #if new game:
                                else:
                                    address = 'Saves/'
                                    address += str(sub_option_selected)
                                    address += '/room'
                                    if not os.path.isfile(address):
                                        print "NO SE PUEE"
                                        running = False
                                        #error_message()
                                        load_game_menu(main_surface, left_light, mid_light, right_light, dark, option_selected)

                                    else:
                                        print "Si se puee"
                                        room = MartyRoom()
                                        marty = create_player(0, room.world_factor)
                                        Save_Game(marty, room, sub_option_selected)
                                        game_loop(0, marty, room)

        # define fonts
        list_font = pygame.font.SysFont("Bebas", int(40*resolution_factor()))

        sub_option_selected = limit_options(options_count, sub_option_selected)
        update_menu(options, main_surface, left_light, mid_light, right_light, dark, 2, options_list, resolution_factor(), option_selected)

        display_small_menu(main_surface, list_font, sub_options_list, sub_option_selected)

        pygame.display.flip()


def start(egg):
    # define fonts
    options_font = pygame.font.SysFont("Bebas", int(60*resolution_factor()))

    # define surfaces
    main_surface = pygame.display.set_mode((int(options.resolution*16/9), options.resolution))
    dark = pygame.Surface((options.resolution*16/9, options.resolution)).convert_alpha()

    left_light = Light("Images/menu_lights/left.png", 300, 0, 45, 35, 135, 50, 12, 6, False)
    mid_light = Light("Images/menu_lights/mid.png", 700, 0, 70, 30, 110, 50, 12, 6, False)
    right_light = Light("Images/menu_lights/right.png", 1100, 0, 140, 20, 160, 50, 12, 6, False)

    #define list of options
    options_list = [None]*2

    options_count = len(options_list) - 1
    option_selected = 0

    clock = pygame.time.Clock()
    frame_count = 0
    click_time = -1
    double_click_speed = 20

    running = True
    while running:
        address = 'Languages/Saves/'
        address += options.language
        file = open(address, 'r')

        options_list = read_file(file, options_list)

        clock.tick(60)
        frame_count += 1
        if frame_count == 600:
            frame_count = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_w] or key[pygame.K_UP]:
            option_selected -= 1
            time.sleep(0.1)
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            option_selected += 1
            time.sleep(0.1)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                    menu()
                if e.key == K_KP_ENTER or e.key == K_RETURN:
                    if option_selected == 0:
                        running = False
                        #give the option of input a name for the save file
                        choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                        load_game_menu(main_surface, left_light, mid_light, right_light, dark, 0)
                    if option_selected == 1:
                        running = False
                        #open a save file and continue from there
                        choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                        load_game_menu(main_surface, left_light, mid_light, right_light, dark, 1)

            mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
            if mouse_pos_x > 30*resolution_factor() and mouse_pos_x < 280*resolution_factor():
                for x in range(0, len(options_list), 1):
                    if mouse_pos_y > (35*resolution_factor()+80*x*resolution_factor()) and mouse_pos_y < (90*resolution_factor()+80*x*resolution_factor()):
                        option_selected = x
                        if e.type == MOUSEBUTTONDOWN:
                            is_it, click_time = double_click(click_time, frame_count, double_click_speed)
                            if is_it:
                                if x == 0:
                                    running = False
                                    #give the option of input a name for the save file
                                    choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                                    load_game_menu(main_surface, left_light, mid_light, right_light, dark, 0)
                                if x == 1:
                                    running = False
                                    #open a save file and continue from there
                                    choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                                    load_game_menu(main_surface, left_light, mid_light, right_light, dark, 1)

        flicker_light(left_light)
        flicker_light(mid_light)
        flicker_light(right_light)

        option_selected = limit_options(options_count, option_selected)

        update_menu(options, main_surface, left_light, mid_light, right_light, dark, 0, options_list, resolution_factor(), option_selected)
        display_menu(main_surface, options_font, options_list, option_selected, resolution_factor())

        pygame.display.flip()


def menu():
    channel = pygame.mixer.Channel(0)
    sound = pygame.mixer.Sound('Sounds/videoplayback.wav')

    if not channel.get_busy():
        channel = sound.play(-1, 0, 0)
    sound.set_volume(float(options.music_volume)/100)
    channel.set_volume(float(options.master_volume)/100)

    room = Hallway()
    room = MartyRoom()

    # define fonts
    options_font = pygame.font.SysFont("Bebas", int(60*resolution_factor()))

    # define surfaces
    main_surface = pygame.display.set_mode((int(options.resolution*16/9), options.resolution))
    main_surface.fill((137, 139, 136))

    dark = pygame.Surface((options.resolution*16/9, options.resolution)).convert_alpha()

    # define lights
    #image_pass, x_pos, y_pos, angle, shift_x, shift_y, beam_start, scale, Switch
    left_light = Light("Images/menu_lights/left.png", 300, 0, 45, 35, 135, 50, 12, 6, False)
    mid_light = Light("Images/menu_lights/mid.png", 700, 0, 70, 30, 110, 50, 12, 6, False)
    right_light = Light("Images/menu_lights/right.png", 1100, 0, 140, 20, 160, 50, 12, 6, False)

    if options.resolution_changed:
        options_menu(0, None, None)

    options_list = [None]*6

    options_count = len(options_list) - 1
    option_selected = 0

    clock = pygame.time.Clock()
    frame_count = 0
    click_time = -1
    double_click_speed = 20

    running = True
    while running:
        address = 'Languages/Menu/'
        address += options.language
        file = open(address, 'r')

        options_list = read_file(file, options_list)

        clock.tick(60)
        frame_count += 1
        if frame_count == 600:
            frame_count = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_w] or key[pygame.K_UP]:
            option_selected -= 1
            time.sleep(0.1)
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            option_selected += 1
            time.sleep(0.1)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                if e.key == K_KP_ENTER or e.key == K_RETURN:
                    if option_selected == 0:
                        running = False
                        channel.fadeout(2000)
                        start(0)
                    if option_selected == 1:
                        options_menu(0, None, None)
                    if option_selected == 2:
                        controls_loop(main_surface, left_light, mid_light, right_light, dark)
                        running = False
                        menu()
                    if option_selected == 3:
                        credits()
                    if option_selected == 4:
                        youtube()
                    if option_selected == 5:
                        blog()

            mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
            if mouse_pos_x > 30*resolution_factor() and mouse_pos_x < 280*resolution_factor():
                for x in range(0, len(options_list), 1):
                    if mouse_pos_y > (35*resolution_factor()+80*x*resolution_factor()) and mouse_pos_y < (90*resolution_factor()+80*x*resolution_factor()):
                        option_selected = x
                        if e.type == MOUSEBUTTONDOWN:
                            is_it, click_time = double_click(click_time, frame_count, double_click_speed)
                            if is_it:
                                if x == 0:
                                    running = False
                                    channel.fadeout(2000)
                                    start(0)
                                if x == 1:
                                    options_menu(0, None, None)
                                if x == 2:
                                    controls_loop(main_surface, left_light, mid_light, right_light, dark)
                                    running = False
                                    menu()
                                if x == 3:
                                    credits()
                                if x == 4:
                                    youtube()
                                if x == 5:
                                    blog()
                if e.type == MOUSEBUTTONDOWN:
                    if mouse_pos_y > 575*resolution_factor() and mouse_pos_y < 675*resolution_factor():
                        is_it, click_time = double_click(click_time, frame_count, double_click_speed)
                        if is_it:
                            running = False
                            channel.fadeout(2000)
                            marty = create_player(1, room.world_factor)
                            game_loop(1, marty, room)
        if options.resolution_changed:
            running = False
            menu()

        flicker_light(left_light)
        flicker_light(mid_light)
        flicker_light(right_light)

        option_selected = limit_options(options_count, option_selected)

        update_menu(options, main_surface, left_light, mid_light, right_light, dark, 0, options_list, resolution_factor(), option_selected)
        display_menu(main_surface, options_font, options_list, option_selected, resolution_factor())

        pygame.display.flip()

menu()