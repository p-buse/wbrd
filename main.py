import pygame
from player import Player, PlayerInput
from board import Board
from pygame.locals import *
def main():
    pygame.init()
    screen_size = w, h = (1024, 768)

    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("WBRD")

    # Initialize clock
    clock = pygame.time.Clock()

    # Set up our game objects
    p1 = Player('1', Color('red'), PlayerInput(K_a, K_d, K_w, K_s, K_f), 3)
    p2 = Player('2', Color('blue'), PlayerInput(K_j, K_l, K_i, K_k, K_h), 3)
    # Make a new board with our two players on it
    board = Board('test_board.brd', [p1, p2])
    pixel_x = w / board.width
    pixel_y = h / board.height
    pixel_size = min(pixel_x, pixel_y)
    print("pixel size: %s" % pixel_size)

    done = False
    while not done:
        clock.tick(60) # don't run faster than 60FPS
        pygame.event.pump() # refresh the event queue
        pressed_keys = pygame.key.get_pressed()
        events = pygame.event.get()
        # Process input
        board.process_input(pressed_keys, events)
        # Update
        board.update()
        # Render
        screen.fill(Color('black'))
        board.render(screen, pixel_size)
        pygame.display.flip()

    pygame.quit()

main()
