import pygame
from vector2 import Vector2
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
        self.pos = Vector2(0,0)
        self.intended_pos = Vector2(0,0)
        self.color = color
        self.inputmap = PlayerInput()

    def set_input_map(self, left, right, up, down):
        self.inputmap = PlayerInput(left, right, up, down)

    """ Set our velocity based on the currently pressed keys"""
    def process_input(self, pressed_keys):
        x_velocity, y_velocity = 0, 0
        if pressed_keys[self.inputmap.left]:
            x_velocity -= 1
        if pressed_keys[self.inputmap.right]:
            x_velocity += 1
        if pressed_keys[self.inputmap.up]:
            y_velocity -= 1
        if pressed_keys[self.inputmap.down]:
            y_velocity += 1
        self.intended_pos = Vector2(self.pos.x + x_velocity, self.pos.y + y_velocity)

    """ Render the player to the screen at a given size"""
    def render(self, screen, pixel_size):
        x, y = self.pos
        screen.fill(self.color, Rect(x, y, pixel_size, pixel_size))

    """ Update the player's position, given a Vector2 of new position"""
    def update(self, new_pos):
        self.pos = new_pos
