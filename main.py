import pygame
import os
import time
import random

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
BG = pygame.image.load(os.path.join("assets", "background-black.png"))

def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
