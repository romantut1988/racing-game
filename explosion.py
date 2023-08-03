import pygamesnd_dir = 'media/snd/'  # Путь до папки со звукамиimg_dir = 'media/img/'  # Путь до папки со спрайтамиwidth = 1200  # ширина игрового окнаheight = 600  # высота игрового окнаclass Explosion(pygame.sprite.Sprite):    def __init__(self, center):        pygame.sprite.Sprite.__init__(self)        self.anim_speed = 2        self.frame = 0        self.anim = [pygame.transform.scale(            pygame.image.load(img_dir + f"./explosion/{i}.png"),            (100, 100)) for i in range(9)]        self.image = self.anim[0]        self.rect = self.image.get_rect()        self.rect.center = center        self.max_speed = 50        self.min_speed = 0        self.speed = 0    def update(self):        keystate = pygame.key.get_pressed()        if keystate[pygame.K_UP] and self.speed < self.max_speed:  # вверх            self.speed += 1        elif keystate[pygame.K_DOWN] and self.speed > self.min_speed:  # вниз            self.speed -= 1        self.rect.y += self.speed  # Изменяем положение по вертикали        self.image = self.anim[self.frame // self.anim_speed]        self.frame += 1        if self.frame >= self.anim_speed * len(self.anim):            self.kill()