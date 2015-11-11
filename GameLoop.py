import pygame
from pygame.locals import *
pygame.init()
from Save_class import*
from Player import*
from Options import*
from Levels import *
from Controls_class import*

def update(main_surface, marty, world_objects, world_decorations, my_font, frame_count, darkness):

    # update / reset
    darkness.fill((0, 0, 0, 100))
    main_surface.fill((137, 169, 186))
    marty.set_hand(marty.hand_number)
    marty.update(frame_count)
    update_world(world_objects, world_decorations)

    # draw
    draw_world(main_surface, world_objects, world_decorations, darkness)
    marty.draw(main_surface, darkness)
    marty.draw_player_info(main_surface)
    main_surface.blit(darkness, (0, 0))

    if marty.inv_on:
        marty.display_inventory(main_surface)

    marty_stats = my_font.render("{0}".format(marty.breath), True, (255, 255, 255))
    main_surface.blit(marty_stats, (5, 5))
    pygame.display.flip()

def resize_player(egg, marty, room_factor):
        if egg:
            player = PlayerCrab(marty.rect.x, marty.rect.y, room_factor)
        else:
            player = PlayerMarty(marty.rect.x, marty.rect.y, room_factor)

        # inventory list and hand

        player.inventory = [None]*3
        for x in range(0, len(marty.inventory)):
            if isinstance(marty.inventory[x], Torch):
                player.inventory[x] = Torch(0, 0, marty.inventory[x].battery, marty.inventory[x].on)
            if isinstance(marty.inventory[x], Axe):
                player.inventory[x] = Axe(0, 0)
            if isinstance(marty.inventory[x], Key):
                player.inventory[x] = Key(0, 0, marty.inventory[x].door_code)

        player.hand_number = marty.hand_number
        player.in_hand = player.inventory[player.hand_number]

        # other stuff
        player.right = marty.right
        player.on_floor = marty.on_floor
        player.move_x = marty.move_x
        player.move_y = marty.move_y
        player.inv_temp = marty.inv_temp
        player.inv_on = marty.inv_on
        player.breath = marty.breath
        player.interact = marty.interact
        return player

def game_loop(egg, marty, room):
    world_objects = room.world_objects

    if options.resolution_changed:
        if isinstance(room, MartyRoom):
            room1 = MartyRoom()
        if isinstance(room, Hallway):
            room1 = Hallway()

        room1.world_objects = room.world_objects
        for x in range(0, len(world_objects)):
            if isinstance(world_objects[x], Switch) or isinstance(world_objects[x], Chest):
                room1.world_objects[x].resize(room1.world_factor)
                world_objects = room1.world_objects
            else:
                room1.world_objects[x].resize()
                world_objects = room1.world_objects



        room = room1


        marty = resize_player(egg, marty, room.world_factor)
        options_menu(1, marty, room.world_factor)



    height = options.resolution
    width = int(options.resolution*16/9)

    # define video mode and alpha for lighting
    main_surface = pygame.display.set_mode((width, height))
    darkness = pygame.Surface((width, height)).convert_alpha()
    darkness.fill((0, 0, 0, 200))

    my_font = pygame.font.SysFont("Courier", int(16*resolution_factor()))
    clock = pygame.time.Clock()
    frame_count = 0

    running = True
    while running:
        clock.tick(60)
        frame_count += 1
        if frame_count == 50:
            frame_count = 0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                Save_Game(marty, room, None)
                quit_game = options_menu(1, marty, room.world_factor)
                if not quit_game:
                    game_loop(egg, marty, room)
                running = False

            if e.type == KEYDOWN:
                if e.key == controls.torch:
                    if marty.in_hand is not None:
                        if isinstance(marty.in_hand, Torch):
                            marty.in_hand.toggle()
                            marty.in_hand.batTemp = 1
                if e.key == controls.inventory:
                    marty.toggle_inventory()
                    marty.inv_temp = 1
                if e.key == controls.drop:
                    marty.drop_hand(world_objects)
                if e.key == K_1:
                    marty.hand_number = 0
                if e.key == K_2:
                    marty.hand_number = 1
                if e.key == K_3:
                    marty.hand_number = 2
                if e.key == K_F5:
                    marty.in_hand.battery -= 10
                if e.key == K_F6:
                    marty.in_hand.battery += 10

            if e.type == KEYUP:
                if e.key == controls.torch:
                    if isinstance(marty.in_hand, Torch):
                        marty.in_hand.batTemp = 0
                if e.key == controls.inventory:
                    marty.inv_temp = 0
                if e.key == controls.interact:
                    marty.try_interact(world_objects)

            if e.type == MOUSEBUTTONDOWN:
                if e.button == 4:
                    if marty.hand_number == 2:
                        marty.hand_number = 0
                    else:
                        marty.hand_number += 1
                if e.button == 5:
                    if marty.hand_number == 0:
                        marty.hand_number = 2
                    else:
                        marty.hand_number -= 1
        gravity(marty)

        marty.move_collide(0, marty.move_y, room.world_decorations)
        marty.move_collide(0, marty.move_y, world_objects)
        key = pygame.key.get_pressed()

        if key[controls.left]:
            if key[controls.sprint]:
                marty.walk_or_sprint(False, -1, room.world_decorations)
                marty.walk_or_sprint(False, -1, world_objects)
            else:
                marty.walk_or_sprint(True, -1, room.world_decorations)
                marty.walk_or_sprint(True, -1, world_objects)
            marty.right = False
        if key[controls.right]:
            if key[controls.sprint]:
                marty.walk_or_sprint(False, 1, room.world_decorations)
                marty.walk_or_sprint(False, 1, world_objects)
            else:
                marty.walk_or_sprint(True, 1, room.world_decorations)
                marty.walk_or_sprint(True, 1, world_objects)
            marty.right = True
        if key[controls.jump]:
            marty.jump()

        if options.resolution_changed:
            running = False
            game_loop(egg, marty, room)

        marty.breath += 0.05

        update(main_surface, marty, world_objects, room.world_decorations, my_font, frame_count, darkness)

