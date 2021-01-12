import pygame
import os
import time
import random
pygame.font.init()

WIN_W, WIN_H = 650, 650
WIN = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption('Space Invaders PyGame')

# CARREGAR AS IMAGENS
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
# NAVE DO JOGADOR
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
# LASERS
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
# BACKGROUND
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIN_W, WIN_H))

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.lasers = []
        self.cool_down_counter = 0

def main():
    run = True
    FPS = 60
    level = 1
    lives = 3
    main_font = pygame.font.SysFont("comicsans", 50)

    clock = pygame.time.Clock()
    
    def redraw_window():
        WIN.blit(BG, (0,0))
        # EXIBR TEXTO NA TELA
        lives_label = main_font.render(f'Vidas: {lives}', 1, (255,255,255))
        level_label = main_font.render(f'Nível: {level}', 1, (255,255,255))

        WIN.blit(lives_label, (20, 20))
        WIN.blit(level_label, (WIN_W - level_label.get_width() - 20, 20))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

main()