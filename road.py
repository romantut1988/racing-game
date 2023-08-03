import pygame

width = 1200  # ширина игрового окна
height = 600  # высота игрового окна
img_dir = 'media/img/'  # папка с картинками
snd_dir = 'media/snd/'  # папка со звуками


class Road(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.max_speed = 50
        self.min_speed = 0
        self.speed = 0

        self.image = pygame.image.load(img_dir + 'road.jpg')
        self.rect = self.image.get_rect()
        self.rect.center = [width / 2, height / 2]

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP] and self.speed < self.max_speed:  # вверх
            self.speed += 1
        elif keystate[pygame.K_DOWN] and self.speed > self.min_speed:
            self.speed -= 1
        self.rect.y += self.speed  # Изменяем положение по вертикали
        if self.rect.top >= 0:  # Если верх достиг верхнего края
            self.rect.bottom = height  # Переносим вверх
