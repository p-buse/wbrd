import pygame
from pygame.locals import *

class PlayerInput(object):
    """ Default control mapping """
    def __init__(self):
        self.left = K_a
        self.right = K_d
        self.up = K_w
        self.down = K_s

    def __init__(self, left, right, up, down):
        self.left = left
        self.right = right
        self.up = up
        self.down = down


class Player(object):
    def __init__(self, number):
        self.number = number
        self.x = 0
        self.y = 0
        self.color = pygame.Color()
        self.velocity = (0,0)
        self.inputmap = PlayerInput() 

    """ Set our velocity based on the currently pressed keys"""
    def processInput(self, pressed_keys):
        velocity = (0, 0)
        if pressed_keys[self.inputmap.left]: 
            velocity[0] -= 1
        if pressed_keys[self.inputmap.right]:
            velocity[0] += 1
        if pressed_keys[self.inputmap.up]:
            velocity[1] -= 1
        if pressed_keys[self.inputmap.down]:
            velocity[1] += 1
        self.velocity = velocity
