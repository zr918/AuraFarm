# player class for the main player
import pygame

from entities import PhysicalEntities

class Player(PhysicalEntities):
    def __init__(self, screen, pos, size): #position and size are both in form (a, b)
        super().__init__(screen, "player", pos, size)
        self.health = 100   # set initial health to 100
        self.inventory = []  # initialize empty array for player inventory
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.width, self.height = size
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.minheight = 0;

    def setpos(self, x, y):
        self.pos = (x, y)

    def pos(self): # returns position
        return self.pos

    def size(self):  # returns size
        return self.size

    def health(self):
        return self.health

    def width(self): return self.width
    def height(self): return self.height

    def changehealth(self, num):
        self.health = min(100, self.health + num)

    def update(self, movement = [0, 0]):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        if self.pos[1] > self.minheight:
            self.velocity[1] = -1
            self.velocity[1] = min(1000, self.velocity[1] + 0.05)
        elif movement[1]:
            self.velocity[1] = -9
        else:
            self.velocity[1] = min(1000, self.velocity[1] + 0.1)

        # if self.pos[0] > 800:
          #  self.pos[0] = 800
        if self.pos[0] < 0:
          self.pos[0] = 0

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]

        #entity_rect = self.rect()

        self.pos[1] += frame_movement[1]

    def jump(self):
        if self.velocity[1] >= -3:
            self.velocity[1] -= 2


    def moveleftright(self, amt):
        self.update([amt, 0]);





