import pygame
import time
pygame.init()

from Menu_things import*
from Options_class import*
from World_Light import Light

def choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected):
    left_light.on = False
    mid_light.on = True
    right_light.on = False

    update_menu(options, main_surface, left_light, mid_light, right_light, dark, 2, options_list, resolution_factor(), option_selected)
    pygame.display.flip()

def display_small_menu(main_surface, options_font, options_list, option_selected):
    for x in range(len(options_list)):
        if x == option_selected:
            option = options_font.render("{0}".format(options_list[x]), True, (255, 255, 255))
            main_surface.blit(option, (740*resolution_factor(), 250*resolution_factor() + (50 * x*resolution_factor())))
        else:
            option = options_font.render("{0}".format(options_list[x]), True, (20, 112, 162))
            main_surface.blit(option, (730*resolution_factor(), 250*resolution_factor() + (50 * x * resolution_factor())))

def small_menu_loop(main_surface, left_light, mid_light, right_light, dark, list_display, list_options, is_list, option_changed, option_selected, from_game):
    options.resolution_changed = 0
    change_options_file()

    options_count = len(list_display) - 1
    sub_option_selected = option_changed

    if from_game:
        options_list = [None]*7
    else:
        options_list = [None]*6

    clock = pygame.time.Clock()
    frame_count = 0
    click_time = -1
    double_click_speed = 20

    running = True
    while running:
        address = 'Languages/Options/'
        address += options.language
        options_file = open(address, 'r')
        options_list = read_file(options_file, options_list)

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
                if e.key == K_KP_ENTER or e.key == K_RETURN:
                    option_changed = sub_option_selected
                    if list_options[0] == 1080:
                        options.resolution_changed = 1
                        running = False

            if is_list:
                mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                if mouse_pos_x > 730*resolution_factor() and mouse_pos_x < 900*resolution_factor():
                    for x in range(0, len(list_display), 1):
                        if mouse_pos_y > (250*resolution_factor()+50*x*resolution_factor()) and mouse_pos_y < (300*resolution_factor()+50*x*resolution_factor()):
                            sub_option_selected = x
                            if e.type == MOUSEBUTTONDOWN:
                                is_it, click_time = double_click(click_time, frame_count, double_click_speed)
                                if is_it:
                                    option_changed = x

        # define fonts
        list_font = pygame.font.SysFont("Bebas", int(40*resolution_factor()))

        sub_option_selected = limit_options(options_count, sub_option_selected)
        update_menu(options, main_surface, left_light, mid_light, right_light, dark, 2, options_list, resolution_factor(), option_selected)

        if is_list:
            display_small_menu(main_surface, list_font, list_display, sub_option_selected)
        else:
            option = list_font.render("{0}".format(list_display[sub_option_selected]), True, (255, 255, 255))
            main_surface.blit(option, (740*resolution_factor(), 250*resolution_factor() + (50 * resolution_factor())))

        font = pygame.font.SysFont("Bebas", int(40*resolution_factor()))
        title = font.render("Press ENTER to save changes", True, (20, 112, 162))
        main_surface.blit(title, (700*resolution_factor(), 600*resolution_factor()))
        pygame.display.flip()
    return list_options[option_changed]

def change_options_file():
    address = 'Languages/Options.txt'
    file = open(address, 'w')
    file.write('language: ')
    file.write(options.language + '\n')
    file.write('resolution: ')
    file.write(str(options.resolution) + '\n')
    file.write('resolution changed: ')
    file.write(str(options.resolution_changed) + '\n')
    file.write('master volume: ')
    file.write(str(options.master_volume) + '\n')
    file.write('music volume: ')
    file.write(str(options.music_volume) + '\n')
    file.write('world volume: ')
    file.write(str(options.world_volume) + '\n')
    file.write('brightness: ')
    file.write(str(options.brightness) + '\n')

def change_language(main_surface, left_light, mid_light, right_light, dark, option_selected):
    language_display_list = [None]*2
    language_file = open('Languages/List.txt', 'r')
    language_display_list = read_file(language_file, language_display_list)
    language_options_list = ["en.txt", "es.txt"]

    for x in range(len(language_options_list)):
        if language_options_list[x] == options.language:
            option_passed = x

    options.language = small_menu_loop(main_surface, left_light, mid_light, right_light, dark, language_display_list, language_options_list, 1, option_passed, option_selected, 0)
    change_options_file()

def change_resolution(main_surface, left_light, mid_light, right_light, dark, option_selected, from_game):
    resolution_display_list = ["1920x1080", "1280x720", "853x480", "640x360"]
    resolution_options_list = [1080, 720, 480, 360]

    for x in range(len(resolution_options_list)):
        if resolution_options_list[x] == options.resolution:
            option_passed = x

    options.resolution = small_menu_loop(main_surface, left_light, mid_light, right_light, dark, resolution_display_list, resolution_options_list, 1, option_passed, option_selected, from_game)
    change_options_file()

def change_master_volume(main_surface, left_light, mid_light, right_light, dark, option_selected):
    master_volume_options_list = [None]*101
    for x in range(0, 101):
        master_volume_options_list[x] = x

    options.master_volume = small_menu_loop(main_surface, left_light, mid_light, right_light, dark, master_volume_options_list, master_volume_options_list, 0, options.master_volume, option_selected, 0)
    change_options_file()

def change_music_volume(main_surface, left_light, mid_light, right_light, dark, option_selected):
    music_volume_options_list = [None]*101
    for x in range(0, 101):
        music_volume_options_list[x] = x

    options.music_volume = small_menu_loop(main_surface, left_light, mid_light, right_light, dark, music_volume_options_list, music_volume_options_list, 0, options.music_volume, option_selected, 0)
    change_options_file()

def change_world_volume(main_surface, left_light, mid_light, right_light, dark, option_selected):
    world_volume_options_list = [None]*101
    for x in range(0, 101):
        world_volume_options_list[x] = x

    options.world_volume = small_menu_loop(main_surface, left_light, mid_light, right_light, dark, world_volume_options_list, world_volume_options_list, 0, options.world_volume, option_selected, 0)
    change_options_file()

def change_brightness(main_surface, left_light, mid_light, right_light, dark, option_selected):
    brightness_options_list = [None]*101
    for x in range(0, 101):
        brightness_options_list[x] = x

    options.brightness = small_menu_loop(main_surface, left_light, mid_light, right_light, dark, brightness_options_list, brightness_options_list, 0, options.brightness, option_selected, 0)
    change_options_file()

def options_menu(from_game, marty, world_factor):
    # define fonts
    options_font = pygame.font.SysFont("Bebas", int(60*resolution_factor()))

    # define surfaces
    main_surface = pygame.display.set_mode((int(options.resolution*16/9), options.resolution))
    main_surface.fill((0, 200, 255))

    dark = pygame.Surface((int(options.resolution*16/9), options.resolution)).convert_alpha()

    # define lights
    left_light = Light("Images/menu_lights/left.png", 300, 0, 45, 35, 135, 50, 12, 6, False)
    mid_light = Light("Images/menu_lights/mid.png", 700, 0, 70, 30, 110, 50, 12, 6, False)
    right_light = Light("Images/menu_lights/right.png", 1100, 0, 140, 20, 160, 50, 12, 6, False)

    if from_game:
        options_list = [None]*7
    else:
        options_list = [None]*6
    options_count = len(options_list) - 1


    if options.resolution_changed:
        address = 'Languages/Options/'
        address += options.language
        file = open(address, 'r')
        options_list = read_file(file, options_list)

        if from_game:
            player_x = marty.rect.x
            player_y = marty.rect.y
            old_factor = resolution_factor()
        choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, 1)
        change_resolution(main_surface, left_light, mid_light, right_light, dark, 1, from_game)
        if options.resolution_changed:
            if from_game:
                marty.rect.x = player_x * resolution_factor() / old_factor
                marty.rect.y = player_y * resolution_factor() / old_factor
            running = False
        else:
            running = True
    else:
        running = True

    option_selected = 0

    clock = pygame.time.Clock()
    frame_count = 0
    click_time = -1
    double_click_speed = 20

    while running:
        # options
        address = 'Languages/Options/'
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
                        choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                        change_language(main_surface, left_light, mid_light, right_light, dark, option_selected)
                    if option_selected == 1:
                        if from_game:
                            player_x = marty.rect.x
                            player_y = marty.rect.y
                            old_factor = resolution_factor()
                        choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                        change_resolution(main_surface, left_light, mid_light, right_light, dark, option_selected, from_game)
                        if options.resolution_changed:
                            if from_game:
                                marty.rect.x = player_x * resolution_factor() / old_factor
                                marty.rect.y = player_y * resolution_factor() / old_factor
                            running = False
                    if option_selected == 2:
                        choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                        change_master_volume(main_surface, left_light, mid_light, right_light, dark, option_selected)
                    if option_selected == 3:
                        choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                        change_music_volume(main_surface, left_light, mid_light, right_light, dark, option_selected)
                    if option_selected == 4:
                        choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                        change_world_volume(main_surface, left_light, mid_light, right_light, dark, option_selected)
                    if option_selected == 5:
                        choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                        change_brightness(main_surface, left_light, mid_light, right_light, dark, option_selected)
                    if option_selected == 6:
                        return 1

            mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
            if mouse_pos_x > 30*resolution_factor() and mouse_pos_x < 450*resolution_factor():
                for x in range(0, len(options_list), 1):
                    if mouse_pos_y > (120*resolution_factor()+80*x*resolution_factor()) and mouse_pos_y < (180*resolution_factor()+80*x*resolution_factor()):
                        option_selected = x
                        if e.type == MOUSEBUTTONDOWN:
                            is_it, click_time = double_click(click_time, frame_count, double_click_speed)
                            if is_it:
                                if x == 0:
                                    choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                                    change_language(main_surface, left_light, mid_light, right_light, dark, option_selected)
                                if x == 1:
                                    if from_game:
                                        player_x = marty.rect.x
                                        player_y = marty.rect.y
                                        old_factor = resolution_factor()
                                    choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                                    change_resolution(main_surface, left_light, mid_light, right_light, dark, option_selected, from_game)
                                    if options.resolution_changed:
                                        if from_game:
                                            marty.resize_player(world_factor)
                                            marty.rect.x = player_x * resolution_factor() / old_factor
                                            marty.rect.y = player_y * resolution_factor() / old_factor
                                        running = False
                                if x == 2:
                                    choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                                    change_master_volume(main_surface, left_light, mid_light, right_light, dark, option_selected)
                                if x == 3:
                                    choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                                    change_music_volume(main_surface, left_light, mid_light, right_light, dark, option_selected)
                                if x == 4:
                                    choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                                    change_world_volume(main_surface, left_light, mid_light, right_light, dark, option_selected)
                                if x == 5:
                                    choice_made(left_light, mid_light, right_light, dark, main_surface, options_list, option_selected)
                                    change_brightness(main_surface, left_light, mid_light, right_light, dark, option_selected)
                                if x == 6:
                                    return 1

        flicker_light(left_light)
        flicker_light(mid_light)
        flicker_light(right_light)

        option_selected = limit_options(options_count, option_selected)
        update_menu(options, main_surface, left_light, mid_light, right_light, dark, 1, options_list, resolution_factor(), option_selected)

        display_options(main_surface, options_font, options_list, option_selected, resolution_factor())
        pygame.display.flip()

