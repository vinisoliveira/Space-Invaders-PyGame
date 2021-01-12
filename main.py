import pygame
import os
import time
import random
pygame.font.init()

WIN_W, WIN_H = 650, 650
WIN = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption('Space Invaders PyGame')

# CARREGAR AS IMAGENS
RED_SPACE_player = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_player = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_player = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
# NAVE DO JOGADOR
YELLOW_SPACE_player = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
# LASERS
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
# BACKGROUND
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIN_W, WIN_H))

class player:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(player):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_player
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


def main():
    run = True
    FPS = 60
    level = 1
    lives = 3
    player_vel = 4
    main_font = pygame.font.SysFont("comicsans", 50)

    player = Player(325, 550)

    clock = pygame.time.Clock()
    
    def redraw_window():
        WIN.blit(BG, (0,0))
        # EXIBR TEXTO NA TELA
        lives_label = main_font.render(f'Vidas: {lives}', 1, (255,255,255))
        level_label = main_font.render(f'Nível: {level}', 1, (255,255,255))

        WIN.blit(lives_label, (20, 20))
        WIN.blit(level_label, (WIN_W - level_label.get_width() - 20, 20))

        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT] and player.x - player_vel > 0: #MOVER-SE PARA A ESQUERDA
            player.x -= player_vel
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIN_W: #MOVER-SE PARA DIREITA
            player.x += player_vel
        if keys[pygame.K_w] or keys[pygame.K_UP] and player.y - player_vel > 0: #MOVER-SE PARA CIMA
            player.y -= player_vel
        if keys[pygame.K_a] or keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < WIN_H: # MOVER-SE PARA BAIXO
            player.y += player_vel

main()