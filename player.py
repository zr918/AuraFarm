# player class for the main player
import pygame

from entities import PhysicalEntities

class Player(PhysicalEntities):
    def __init__(self, screen, pos, size): #position and size are both in form (a, b)
        super().__init__(screen, "player", pos, size)
        self.health = 100   # set initial health to 100
        self.inventory = []  # initialize empty array for player inventory

    def pos(self): # returns position
        return self.pos

    def size(self):  # returns size
        return self.size

