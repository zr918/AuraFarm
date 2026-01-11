# enemy class for enemies
import pygame

from entities import PhysicalEntities

class Enemy(PhysicalEntities):
    def __init__(self, screen, pos, size): #position and size are both in form (a, b)
        super().__init__(screen, "player", pos, size)
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

    def pos(self): # returns position
        return self.pos

    def size(self):  # returns size
        return self.size

    def health(self):
        return self.health

    def changehealth(self, num):
        self.health = self.health + num

    def update(self, movement = [0, 0]):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        if self.pos[1] > 320:
            self.velocity[1] = -1
            self.velocity[1] = min(1000, self.velocity[1] + 0.05)
        elif movement[1]:
            self.velocity[1] = -9
        else:
            self.velocity[1] = min(1000, self.velocity[1] + 0.1)

        if self.pos[0] > 800:
            self.velocity[0] = -1
        else:
            self.velocity[0] = 1

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]

        #entity_rect = self.rect()

        self.pos[1] += frame_movement[1]

    def jump(self):
        if self.velocity[1] >= -3:
            self.velocity[1] -= 2


    def moveleftright(self, amt):
        self.update([amt, 0]);





