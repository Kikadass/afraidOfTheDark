import pygame
import time
import Tkinter
pygame.init()

from Menu_things import*
from Options_class import*
from Controls_class import*

class ERROR():
    def __init__(self, master):
        self.master = master

        geometry  = '170x50'
        x = int(800*resolution_factor())
        y = int(500*resolution_factor())
        geometry = geometry + '+' + str(x) + '+' + str(y)
        self.master.geometry(geometry)
        self.master.title('ERROR')

        self.label = Tkinter.Label(self.master, text = 'That key has already been used', fg = 'black').grid(row = 0, column = 2)
        self.button = Tkinter.Button(self.master, text = "OK", fg = 'blue', command = self.finish).grid(row = 1, column = 2)

    def finish(self):
        self.master.destroy()

def error_message():
    root = Tkinter.Tk()
    the_window = ERROR(root)
    root.mainloop()

def change_controls_file(controls):
    address = 'Languages/Controls.txt'
    file = open(address, 'w')
    file.write('jump: ')
    file.write(str(controls.jump) + '\n')
    file.write('up: ')
    file.write(str(controls.up) + '\n')
    file.write('down: ')
    file.write(str(controls.down) + '\n')
    file.write('left: ')
    file.write(str(controls.left) + '\n')
    file.write('right: ')
    file.write(str(controls.right) + '\n')
    file.write('sprint: ')
    file.write(str(controls.sprint) + '\n')
    file.write('invetory: ')
    file.write(str(controls.inventory) + '\n')
    file.write('torch: ')
    file.write(str(controls.torch) + '\n')
    file.write('drop: ')
    file.write(str(controls.drop) + '\n')
    file.write('interact: ')
    file.write(str(controls.interact) + '\n')
    file.closed

def change_control(option_selected):
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                else:
                    key = e.key
                    if e.key == controls.jump or e.key == controls.up or e.key == controls.down or e.key == controls.left or e.key == controls.right or e.key == controls.sprint or e.key == controls.inventory or e.key == controls.torch or e.key == controls.drop or e.key == controls.interact:
                        error_message()
                        running = False
                    else:
                        if option_selected == 0:
                            controls.jump = key
                            running = False
                        if option_selected == 1:
                            controls.up = key
                            running = False
                        if option_selected == 2:
                            controls.down = key
                            running = False
                        if option_selected == 3:
                            controls.left = key
                            running = False
                        if option_selected == 4:
                            controls.right = key
                            running = False
                        if option_selected == 5:
                            controls.sprint = key
                            running = False
                        if option_selected == 6:
                            controls.inventory = key
                            running = False
                        if option_selected == 7:
                            controls.torch = key
                            running = False
                        if option_selected == 8:
                            controls.drop = key
                            running = False
                        if option_selected == 9:
                            controls.interact = key
                            running = False

def display_small_menu_controls(main_surface, options_font, options_list, option_selected):
    list = [None]*10
    address = 'Languages/Controls.txt'
    file = open(address, 'r')
    list = read_file(file, list)

    for x in range(len(options_list)):
        if x == option_selected:
            option = options_font.render("{0}".format(options_list[x]), True, (255, 255, 255))
            main_surface.blit(option, (540*resolution_factor(), 250*resolution_factor() + (40 * x*resolution_factor())))
            option = options_font.render("{0}".format(pygame.key.name(int(list[x]))), True, (255, 255, 255))
            main_surface.blit(option, (780*resolution_factor(), 250*resolution_factor() + (40 * x*resolution_factor())))
        else:
            option = options_font.render("{0}".format(options_list[x]), True, (20, 112, 162))
            main_surface.blit(option, (530*resolution_factor(), 250*resolution_factor() + (40 * x * resolution_factor())))
            option = options_font.render("{0}".format(pygame.key.name(int(list[x]))), True, (20, 112, 162))
            main_surface.blit(option, (770*resolution_factor(), 250*resolution_factor() + (40 * x*resolution_factor())))

def controls_loop(main_surface, left_light, mid_light, right_light, dark):
    #reading the Menu list from a file
    menu_list = [None]*6
    address = 'Languages/Menu/'
    address += options.language
    menu_file = open(address, 'r')
    menu_list = read_file(menu_file, menu_list)

    #reading the Controls list from a file
    controls_list = [None]*10
    address = 'Languages/Controls/'
    address += options.language
    controls_file = open(address, 'r')
    controls_list = read_file(controls_file, controls_list)

    options_count = len(controls_list)-1
    option_selected = 0

    clock = pygame.time.Clock()
    frame_count = 0
    click_time = -1
    double_click_speed = 20

    running = True
    while running:
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
                    change_control(option_selected)
                    change_controls_file(controls)
                    controls.update_controls()


            mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
            if mouse_pos_x > 530*resolution_factor() and mouse_pos_x < 900*resolution_factor():
                for x in range(0, len(controls_list), 1):
                    if mouse_pos_y > (250*resolution_factor()+40*x*resolution_factor()) and mouse_pos_y < (300*resolution_factor()+40*x*resolution_factor()):
                        option_selected = x
                        if e.type == MOUSEBUTTONDOWN:
                            is_it, click_time = double_click(click_time, frame_count, double_click_speed)
                            if is_it:
                                change_control(x)
                                change_controls_file(controls)
                                controls.update_controls()


        # define fonts
        list_font = pygame.font.SysFont("Bebas", int(30*resolution_factor()))
        font = pygame.font.SysFont("Bebas", int(40*resolution_factor()))


        sub_option_selected = limit_options(options_count, option_selected)

        left_light.on = True
        mid_light.on = True
        right_light.on = True
        update_menu(options, main_surface, left_light, mid_light, right_light, dark, 2, menu_list, resolution_factor(), 2)

        display_small_menu_controls(main_surface, list_font, controls_list, sub_option_selected)

        title = font.render("Press ENTER to change", True, (20, 112, 162))
        main_surface.blit(title, (700*resolution_factor(), 650*resolution_factor()))
        pygame.display.flip()
