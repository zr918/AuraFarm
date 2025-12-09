import pygame
import sys

from player import Player
from interactable import Interactable, Food, Water, Sign
from entities import PhysicalEntities

#intialization (game class)
class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('AuraFarm')
        self.clock = pygame.time.Clock()
        self.assets = { # (dictionary) all images for stuff on the screen e.g. background, player, interactable
            'background': (14, 219, 248), #RGB color tuple for background
            'player': pygame.transform.scale(pygame.image.load("images/sprite.webp").convert_alpha(), (200, 300))
        }
        self.player = Player(self.screen, (100, 100), self.assets['player'].get_size())

    def run(self):
        running = True
        while running:
            self.screen.fill(self.assets['background'])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.blit(self.assets['player'], self.player.pos) # this is fine
            pygame.display.update()
            pygame.time.Clock().tick(60)


Game().run()

