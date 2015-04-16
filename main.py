import pygame
from pygame.locals import *
def main():
    pygame.init()
    screen_size = (960, 600)
    player_size = 25

    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("WBRD")

    # Initialise clock
    clock = pygame.time.Clock()
    done = False
    x = y = 0
    while not done:
        clock.tick(60) # don't run faster than 60FPS
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            done = True
        if pressed_keys[K_a]:
            x += 1
        if pressed_keys[K_d]:
            x -= 1
        if pressed_keys[K_w]:
            y -= 1
        if pressed_keys[K_s]:
            y += 1

        """Update below here"""


        """Render below here"""
        screen.fill(Color('black'))
        pygame.draw.rect(screen, Color('white'), Rect(x, y, player_size, player_size))
        pygame.display.flip()

    pygame.quit()

main()
