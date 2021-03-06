import pygame
import os
import time
import random
from pygame import mixer
from pygame.constants import QUIT
pygame.font.init()

WIN_W, WIN_H = 650, 650
WIN = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption('Space Invaders PyGame')

# CARREGAR AS IMAGENS
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
# NAVE DO JOGADOR
YELLOW_SPACE_player = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
# LASERS
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# BACKGROUND
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIN_W, WIN_H))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

class Ship:
    COOLDOWN = 30

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
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(WIN_H):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                mixer.music.load('assets/sounds/shock-impact.wav')
                mixer.music.play()
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            mixer.music.load('assets/sounds/laser-gun2.wav')
            mixer.music.play()

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_player
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(WIN_H):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        mixer.music.load('assets/sounds/explosion-hit.wav')
                        mixer.music.play()
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
            'red':(RED_SPACE_SHIP, RED_LASER),
            'green':(GREEN_SPACE_SHIP, GREEN_LASER),
            'blue':(BLUE_SPACE_SHIP, BLUE_LASER)
    }
    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 12, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def move(self, vel):
        self.y += vel


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    mixer.music.load('assets/sounds/Space-Invaders-Gameplay.wav')
    mixer.music.play(-1)

    run = True
    FPS = 60
    level = 0
    lives = 3
    player_vel = 4
    laser_vel = 3
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_lenght = 5
    enemy_vel = 1

    player = Player(325, 530)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0
    
    def redraw_window():
        WIN.blit(BG, (0,0))
        # EXIBR TEXTO NA TELA
        lives_label = main_font.render(f'Vidas: {lives}', 1, (255,255,255))
        level_label = main_font.render(f'Nível: {level}', 1, (255,255,255))

        WIN.blit(lives_label, (20, 20))
        WIN.blit(level_label, (WIN_W - level_label.get_width() - 20, 20))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render('Você Perdeu!', 1, (255,255,255))
            WIN.blit(lost_label, (WIN_W/2 - lost_label.get_width()/2, 300))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            mixer.music.load('assets/sounds/explosion-hit2.wav')
            mixer.music.play()
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_lenght += 5
            for i in range(wave_lenght):
                enemy = Enemy(random.randrange(50, WIN_W - 100), random.randrange(-1000, -100), random.choice(['red', 'green', 'blue']))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        #MOVER-SE PARA A ESQUERDA
        if keys[pygame.K_a] and player.x - player_vel > 0 or keys[pygame.K_LEFT] and player.x - player_vel > 0: 
            player.x -= player_vel
        #MOVER-SE PARA DIREITA
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIN_W or keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIN_W:
            player.x += player_vel
        #MOVER-SE PARA CIMA
        if keys[pygame.K_w]  and player.y - player_vel > 0 or keys[pygame.K_UP] and player.y - player_vel > 0: 
            player.y -= player_vel
        # MOVER-SE PARA BAIXO
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < WIN_H or keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < WIN_H:
            player.y += player_vel
        #ATIRAR
        if keys[pygame.K_SPACE] or keys[pygame.K_KP_ENTER]:
            player.shoot()            

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                mixer.music.load('assets/sounds/shock-impact.wav')
                mixer.music.play()
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > WIN_H:
                lives -= 1
                enemies.remove(enemy)
            
        player.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pygame.font.SysFont('comicsans', 70)
    run = True
    pygame.mixer.init()
    mixer.music.load('assets/sounds/Space_Invaders_theme.wav')
    mixer.music.play(-1)
    while run:

        WIN.blit(BG, (0,0))
        title_label = title_font.render('Clique para começar', 1, (255,255,255))
        WIN.blit(title_label, (WIN_W/2 - title_label.get_width()/2, 300))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mixer.music.stop()
                main()
    quit()

main_menu()