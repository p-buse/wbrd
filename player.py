import pygame
from pygame.locals import *

class PlayerInput(object):
    """ Default control mapping """
    def __init__(self, left=K_a, right=K_d, up=K_w, down=K_s):
        self.left = left
        self.right = right
        self.up = up
        self.down = down


class Player(object):
    def __init__(self, char, color):
        self.char = char
        self.pos = [0,0]
        self.color = color
        self.velocity = [0,0]
        self.inputmap = PlayerInput()

    def set_input_map(self, left, right, up, down):
        self.inputmap = PlayerInput(left, right, up, down)

    """ Set our velocity based on the currently pressed keys"""
    def process_input(self, pressed_keys):
        velocity = [0, 0]
        if pressed_keys[self.inputmap.left]:
            velocity[0] -= 1
        if pressed_keys[self.inputmap.right]:
            velocity[0] += 1
        if pressed_keys[self.inputmap.up]:
            velocity[1] -= 1
        if pressed_keys[self.inputmap.down]:
            velocity[1] += 1
        self.velocity = velocity

    """ Render the player to the screen at a given size"""
    def render(self, screen, pixel_size):
        x, y = self.pos
        pygame.draw.rect(screen, self.color, Rect(x, y, pixel_size, pixel_size))

    """ Update the player's position, given a new position"""
    def update(self, new_pos):
        self.pos = new_pos
