import pygame
import time
from player import Player
from speedometer import Speedometr
from arrow import Arrow
from bullet import Bullet
from road import Road
from board import Board
from tree import Tree
from explosion import Explosion
from auto_forward import Auto_forward
from auto_backward import Auto_backward


def draw_text(screen, text, size, x, y, color):
    font_name = "media/font.ttf"
    font = pygame.font.Font(font_name, size)
    text_image = font.render(text, True, color)
    text_rect = text_image.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_image, text_rect)


def get_hit_sprite(hits_dict):
    for hit in hits_dict.values():
        return hit[0]


pygame.init()  # Инициализируем модуль pygame

width = 1200  # ширина игрового окна
height = 600  # высота игрового окна
fps = 30  # частота кадров в секунду
game_name = "Racing"  # название нашей игры

img_dir = "media/img/"
snd_dir = "media/snd/"

# Цвета
BLACK = "#4B0082"
WHITE = "#FFFFFF"
RED = "#FF0000"
GREEN = "#008000"
BLUE = "#0000FF"
CYAN = "#00FFFF"
GOLD = '#FFD700'

# Создаем игровой экран
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(game_name)  # Заголовок окна
icon = pygame.image.load(img_dir + 'icon.png')  # иконка
pygame.display.set_icon(icon)  # устанавливаем иконку в окно

player = Player()
speedometr = Speedometr()
arrow = Arrow()

all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
bullets = pygame.sprite.Group()
cars = pygame.sprite.Group()
boards = pygame.sprite.Group()

road = Road()
board_left = Board("left")
board_right = Board("right")

all_sprites.add(road)
all_sprites.add(board_left)
all_sprites.add(board_right)
boards.add(board_left)
boards.add(board_right)

all_sprites.add(player)
all_sprites.add(speedometr)
all_sprites.add(arrow)
players.add(player)  # добавляем игрока в группу

for i in range(20):
    tree = Tree()
    all_sprites.add(tree)

for i in range(4):
    auto_forward = Auto_forward()
    auto_backward = Auto_backward()

    all_sprites.add(auto_forward)
    all_sprites.add(auto_backward)

    cars.add(auto_forward)
    cars.add(auto_backward)

timer = pygame.time.Clock()  # Создаем таймер pygame

pygame.mixer.music.load(snd_dir + "music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

end_time = time.time()
run = True
while run:  # Начинаем бесконечный цикл
    timer.tick(fps)  # Контроль времени (обновление игры)
    all_sprites.update()  # Выполняем действия всех спрайтов в группе
    for event in pygame.event.get():  # Обработка ввода (события)
        if event.type == pygame.QUIT:  # Проверить закрытие окна
            run = False  # Завершаем игровой цикл
        if event.type == pygame.KEYDOWN and len(players) > 0:  # Если клавиша нажата
            if event.key == pygame.K_SPACE:
                player.snd_shoot.play()
                bullet = Bullet(player)  # Создаем пулю
                all_sprites.add(bullet)  # Добавляем пулю к спрайтам
                bullets.add(bullet)  # Добавляем пулю к пулям

    player.score += player.speed // 10

    hit_bullets = pygame.sprite.groupcollide(bullets, cars, True, False)
    if hit_bullets:
        car = get_hit_sprite(hit_bullets)
        car.sound.play()
        expl = Explosion(car.rect.center)  # Создаем взрыв на месте авто
        all_sprites.add(expl)
        if car.type == 'forward':
            auto_forward = Auto_forward()
            all_sprites.add(auto_forward)
            cars.add(auto_forward)
            player.score += 10
        else:
            auto_backward = Auto_backward()
            all_sprites.add(auto_backward)
            cars.add(auto_backward)
            player.score += 50
        car.kill()
    for car in cars:
        cars.remove(car)
        hit_another_car = pygame.sprite.spritecollide(car, cars, False)
        if hit_another_car:
            car.sound.play()
            car.sound.set_volume(0.1)
            expl = Explosion(car.rect.center)  # Создаем взрыв на месте авто
            all_sprites.add(expl)
            if car.type == 'forward':
                auto_forward = Auto_forward()
                all_sprites.add(auto_forward)
                cars.add(auto_forward)
            else:
                auto_backward = Auto_backward()
                all_sprites.add(auto_backward)
                cars.add(auto_backward)
            car.kill()
        else:
            cars.add(car)

    # Событие столкновения игрока и бортиков
    hit_boards = pygame.sprite.groupcollide(players, boards, False, False)

    # Событие столкновения игрока и авто
    hit_cars = pygame.sprite.groupcollide(players, cars, False, False)

    if hit_boards or hit_cars:  # Если произошло какое-то из событий
        player.speed = 0
        player.kill()
        end_time = time.time()
        for sprite in all_sprites:  # Обходим все спрайты в группе
            try:  # Пытаемся, так как не все спрайты имеют параметр скорости
                sprite.speed = 0
                sprite.max_speed = 0
                sprite.min_speed = 0
            except:  # Если получили ошибку в командах блока try
                continue  # То ничего не делаем
        player.snd_move.stop()
        player.snd_explosion.play()
        expl = Explosion(player.rect.center)  # Создаем взрыв на месте игрока
        all_sprites.add(expl)

    screen.fill(GREEN)  # Заливка заднего фона
    all_sprites.draw(screen)  # Отрисовываем все спрайты
    draw_text(screen, f'Score = {player.score}', 50, 120, 20, GOLD)

    if len(players) == 0:
        draw_text(screen, 'Game Over', 100, width / 2, height / 2 - 50, WHITE)
        draw_text(screen, f'Score = {player.score}', 100, width / 2, height / 2 + 50, WHITE)

    if time.time() - end_time > 5 and len(players) == 0:
        run = False

    pygame.display.update()  # Переворачиваем экран
pygame.quit()  # Корректно завершаем игру
