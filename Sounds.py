from Player import *
window = pygame.display.set_mode((640, 400))
pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)

try:
    pygame.mixer.music.load('Sounds/bowhit2.ogg.wav')
    pygame.mixer.music.play(-1)

except:
    print("NO00")

    
