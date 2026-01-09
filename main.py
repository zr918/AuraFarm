import pygame
import sys
import csv

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
            'player': pygame.transform.scale(pygame.image.load("images/spritetest.png").convert_alpha(), (40, 60))
        }
        self.player = Player(self.screen, [100, 100], self.assets['player'].get_size())
        pygame.mixer.music.load('sounds/piano_sound.mp3')


    def run(self):
        pygame.mixer.music.play()
        pygame.mixer.music.play(-1)
        running = True
        font = pygame.font.SysFont("Adobe Heidi Std Normal", 16)
        ticks = 0;
        while running:
            self.screen.fill(self.assets['background'])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.jump()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.moveleftright(-4);
            if keys[pygame.K_RIGHT]:
                self.player.moveleftright(4);

            self.player.update()
            self.screen.blit(self.assets['player'], self.player.pos) # this is fine
            #health bar graphic
            pygame.draw.rect(self.screen, (255, 0, 0), (50, 150-self.player.health, 25, self.player.health))
            pygame.draw.rect(self.screen, (0, 0, 0), (50, 50, 25, 100), 3)
            #health bar text
            text_surface = font.render("HP: " + str(self.player.health), True, (0, 0, 0))
            self.screen.blit(text_surface, (45, 30))

            #update
            pygame.display.update()
            pygame.time.Clock().tick(60)

            #decrease health by 5 every 15 seconds
            ticks = ticks + 1;
            if ticks == 900:
                self.player.changehealth(-5)
                ticks = 0;



    # def read_map_from_csv("Aura Farm Map Draft - Sheet1"):
    # def load_map_colors_from_excel(filename):



Game().run()

