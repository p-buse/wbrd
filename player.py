import pygame
from vector2 import Vector2
from pygame.locals import *

class PlayerInput(object):
    def __init__(self, left, right, up, down, attack):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.attack = attack


class Player(object):
    def __init__(self, char, color, inputmap, num_attacks):
        self.char = char
        self.pos = Vector2(0,0)
        self.intended_pos = Vector2(0,0)
        self.color = color
        self.inputmap = inputmap
        self.attacking = False
        self.attacks_left = num_attacks

    """ Set our velocity based on the currently pressed keys"""
    def process_input(self, pressed_keys, events):
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
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.inputmap.attack:
                    self.attacking = True

    """ Render the player to the screen at a given size"""
    def render(self, screen, pixel_size):
        x, y = self.pos
        screen.fill(self.color, Rect(x, y, pixel_size, pixel_size))

    """Returns a dictionary of which actions this player performed this tick or not"""
    def update(self):
        if self.attacking and self.attacks_left > 0:
            self.attacking = False
            self.attacks_left -= 1
            return {'attacking': True}
        else:
            return {'attacking': False}
