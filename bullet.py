import pygame

width = 1200  # ширина игрового окна
height = 600  # высота игрового окна

img_dir = 'media/img/'  # папка с картинками
snd_dir = 'media/snd/'  # папка со звуками


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_dir + 'shell.png')
        self.image = pygame.transform.scale(self.image, (4, 15))
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center  # Пуля там же где и игрок
        self.speed = 50

    def update(self):
        self.rect.y -= self.speed  # Полет пули против оси Y
        if self.rect.bottom < 0:  # Если залетела за верхний край экрана
            self.kill()
