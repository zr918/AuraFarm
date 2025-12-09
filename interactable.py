# interactable - objects that the player can interact with or view on their journey
# includes objects that give the character information
# and objects that the character can add to their inventory
import pygame


class Interactable:
    def __init__(self):
        self.screen = pygame.display.get_surface()

class Food(Interactable):  # food class
    def __init__(self, screen):
        super().__init__()

class Water(Interactable):   # water class
    def __init__(self, screen):
        super().__init__()

class Sign(Interactable):   # sign class
    def __init__(self, screen):
        super().__init__()

