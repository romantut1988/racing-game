import pygame

img_dir = "media/img/"
snd_dir = "media/snd/"

width = 1200  # ширина игрового окна
height = 600  # высота игрового окна


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_dir + "player.png")
        self.rect = self.image.get_rect()
        self.rect.x = width / 2
        self.rect.bottom = height - 50
        self.max_speed = 50
        self.min_speed = 0
        self.speed = 0
        self.score = 0
        self.snd_shoot = pygame.mixer.Sound(snd_dir + "shoot.mp3")
        self.snd_move = pygame.mixer.Sound(snd_dir + "motor.mp3")
        self.snd_explosion = pygame.mixer.Sound(snd_dir + "explosion_player.mp3")

    def update(self):  # Функция, действия которой выполнятся каждый тик
        keystate = pygame.key.get_pressed()  # Нажатие на кнопку
        if keystate[pygame.K_RIGHT]:  # Если нажата стрелка вправо
            self.rect.x += 15  # Изменяем координату Х на 5
        elif keystate[pygame.K_LEFT]:  # Если нажата стрелка влево
            self.rect.x -= 15  # Изменяем координату Х на -5
        elif keystate[pygame.K_UP] and self.speed < self.max_speed:
            self.speed += 1
        elif keystate[pygame.K_DOWN] and self.speed > self.min_speed:
            self.speed -= 1
        if self.speed > 0 and not pygame.mixer.get_busy():
            self.snd_move.play()
        if self.speed == 0:
            self.snd_move.stop()
