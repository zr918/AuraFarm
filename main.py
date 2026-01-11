import pygame
import sys
import csv
import pytmx

from player import Player
from interactable import Interactable, Food, Water, Sign
from entities import PhysicalEntities

#intialization (game class)
class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        #slightly stupid fix to a bug (temp setting the screen to an irrelevant size)
        self.screen = pygame.display.set_mode((800, 600))

        self.tmx_data = pytmx.load_pygame("maps/Start_Forest Scene.tmx")
        self.TILE_WIDTH = self.tmx_data.tilewidth * 2
        self.TILE_HEIGHT = self.tmx_data.tileheight * 2

        mapwidth = self.tmx_data.width * self.TILE_WIDTH
        mapheight = self.tmx_data.height * self.TILE_HEIGHT

        self.camerax = 0

        self.screen = pygame.display.set_mode((800, mapheight))
        pygame.display.set_caption('AuraFarm')
        self.clock = pygame.time.Clock()
        self.assets = { # (dictionary) all images for stuff on the screen e.g. background, player, interactable
            'background': (14, 219, 248), #RGB color tuple for background
            'player': pygame.transform.scale(pygame.image.load("images/spritetest.png").convert_alpha(), (40, 60)),
            'food': pygame.transform.scale(pygame.image.load("images/corn.png").convert_alpha(), (50, 60))
        }
        self.player = Player(self.screen, [100, 100], self.assets['player'].get_size())
        pygame.mixer.music.load('sounds/piano_sound.mp3')
        # def read_map_from_csv("Aura Farm Map Draft - Sheet1"):
        # def load_map_colors_from_excel(filename):

        #food
        self.interactable_food = []
        for obj in self.tmx_data.objects:
            if obj.type == 'Food':
                newfood = Food(obj.x * 2, obj.y * 2, obj.width * 2, obj.height * 2)
                self.interactable_food.append(newfood)


        #popups and interactable objects
        #storage of all the interactable objects
        self.interactables = []
        self.active_popup = None
        self.popup_image = pygame.image.load("images/oldPaper.jpg").convert_alpha()
        self.font_popup = pygame.font.SysFont("Adobe Heidi Std Normal", 16)
        self.load_interactables()

    def load_interactables(self):
        for obj in self.tmx_data.objects:
            obj_name = str(obj.name).lower()
            rect = pygame.Rect(2*obj.x - self.camerax, 2*obj.y, 2*obj. width, 2*obj. height)

            #it triggers the popup when soldier is interacted with
            if obj_name == "soldier":
                self.interactables.append({
                    "type": "soldier", "rect": rect, "text": obj.properties.get("txt")
                })
            #it triggers the map switch when the door is interacted with
            elif obj_name == "door":
                self.interactables.append({
                    "type": "door", "rect": rect, "target": obj.properties.get("Start_Forest Scene"), "spawn": (obj.properties.get("X"), obj.properties.get("Y"))
                })

    def intro(self):
        startscreen = pygame.image.load('images/startscreen.webp')
        self.screen.blit(startscreen, (0, 0))
        pygame.display.update()
        pygame.time.delay(5000)

    def draw_map(self):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, tile in layer.tiles():
                    tile = pygame.transform.scale(tile, (self.TILE_WIDTH, self.TILE_HEIGHT))
                    self.screen.blit(tile, (x * self.TILE_WIDTH - self.camerax, y * self.TILE_HEIGHT))

    def run(self):
        pygame.mixer.music.play()
        pygame.mixer.music.play(-1)
        running = True
        font = pygame.font.SysFont("Adobe Heidi Std Normal", 16)
        ticks = 0;
        player_rect = pygame.Rect(self.player.pos[0] - self.camerax, self.player.pos[1], self.player.width, self.player.height)
        while running:
            moved = 0
            self.draw_map()

            self.camerax = self.player.pos[0] - 400
            self.camerax = max(0, min(self.camerax, 18*64 - 800))

            colliding = False
            for obj in self.tmx_data.objects:
                obj.rect = pygame.Rect(2*obj.x - self.camerax, 2*obj.y, 2*obj.width, 2*obj.height)
                if obj.type != 'Food':
                    if player_rect.colliderect(obj.rect):
                        print(obj.rect)
                        colliding = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.jump()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    world_mouse_pos = (mouse_pos[0] + self.camerax, mouse_pos[1])

                    # checks for any clicks on the door
                    for obj in self.interactables:
                        if obj[:type:] == "door" and obj.colliderect(world_mouse_pos):
                            self.change_map(obj["target"], obj["spawn"])

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.moveleftright(-4);
                if (self.camerax != 0 and self.camerax != 18*64 - 800):
                    moved = -4
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.moveleftright(4);
                if (self.camerax != 0 and self.camerax != 18*64 - 800):
                    moved = 4

            if not colliding:
                self.player.update()

            self.draw_map()
            self.screen.blit(self.assets['player'], (self.player.pos[0] - self.camerax, self.player.pos[1])) # this is fine
            player_rect = pygame.Rect(self.player.pos[0] - self.camerax, self.player.pos[1], self.player.width, self.player.height)

            #health bar graphic
            pygame.draw.rect(self.screen, (255, 0, 0), (50, 150-self.player.health, 25, self.player.health))
            pygame.draw.rect(self.screen, (0, 0, 0), (50, 50, 25, 100), 3)
            #health bar text
            text_surface = font.render("HP: " + str(self.player.health), True, (255, 255, 255))
            self.screen.blit(text_surface, (45, 30))

            #food graphics
            for food in self.interactable_food:
                food.x = food.x - moved
                food.rect = pygame.Rect(food.x, food.y, food.width, food.height)
                if not food.iseaten() and player_rect.colliderect(food.rect):
                    food.eaten = True
                    self.player.changehealth(food.health)
                if not food.iseaten():
                    self.screen.blit(self.assets['food'], (food.x, food.y))


            # update
            pygame.display.update()
            pygame.time.Clock().tick(60)

            # decrease health by 5 every 15 seconds
            ticks = ticks + 1;
            if ticks == 900:
                self.player.changehealth(-5)
                ticks = 0;

            if self.active_popup:
                 self.draw_pop(self.active_popup)


    #This draws the popup box
    def draw_pop(self, text):
        box_rect= self.popup_image.get_rect(center = (self.player.pos[0] - self.camerax, self.player.pos[1]))
        self.screen.blit(self.popup_image, box_rect)

        lines = self.wrap_text(text, self.font_popup, box_rect.width - 40)
        y = box_rect.y +25
        for line in lines:
            surf = self.font_popup.render(line, True, (60, 40, 20))
            self.screen.blit(surf, (box_rect.x + 20, y))
            y += 26

    # This wraps the text so it fits inside the popup box
    def wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        return lines





#Game().intro()
Game().run()

