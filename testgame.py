import pygame
import random
from pygame.locals import *


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('Fly (1).png').convert()
        self.image = pygame.transform.scale(self.image, (70, 60))
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom >= 600:
            self.rect.bottom = 600


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('Bullet (1).png').convert()
        self.image = pygame.transform.scale(self.image, (30, 20))
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(center=(random.randint(1200, 1300), random.randint(0, 800)))
        self.speed = random.randint(1, 2)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


pygame.init()
screen = pygame.display.set_mode((1200, 800))

ADDENEMY = pygame.USEREVENT + 1

pygame.time.set_timer(ADDENEMY, 250)

player = Player()

background = pygame.image.load('BG.png').convert()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# Variable to keep our main loop running
running = True

# Our main loop!!!
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event; KEYDOWN is a constant defiend in pygame.locals
        if event.type == KEYDOWN:
            # If the Esc key has been pressed set running to false to exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event; if QUIT, set running to False
        elif event.type == QUIT:
            running = False
        elif (event.type == ADDENEMY):
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    screen.blit(background, (0, 0))
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()

    for enity in all_sprites:
        screen.blit(enity.image, enity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    pygame.display.flip()
