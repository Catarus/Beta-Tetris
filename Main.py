from platform import system

import pygame
import random
import time

colors = [
    (0, 0, 0),       # Черный (фон)
    (0, 255, 255),   # I - Голубой
    (255, 0, 0),     # Z - Красный
    (0, 255, 0),     # S - Зелёный
    (0, 0, 255),     # J - Синий
    (255, 165, 0),   # L - Оранжевый
    (128, 0, 128),   # T - Фиолетовый
    (255, 255, 0)    # O - Жёлтый
]

class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # J
        [[4, 5, 9, 10], [2, 6, 5, 9]],   # S
        [[2, 3, 5, 6], [1, 5, 6, 10]],  # Z
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # T
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # I
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # O
        [[1, 2, 5, 6]]  # L
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)  # Выбираем случайный тип фигуры
        self.color = self.type + 1  # Цвет фигуры соответствует её типу
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

class Tetris:
    def __init__(self, height, width):
        self.next_figure = None  # Следующая фигура
        self.level = 1  # Начальный уровень
        self.score = 0
        self.lines_cleared = 0  # Количество уничтоженных линий
        self.state = "Начало"
        self.field = []
        self.height = height
        self.width = width
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figure = None
        self.fall_speed = 0.8  # Начальная скорость падения фигур

        self.height = height # поле
        self.width = width
        self.field = []
        self.score = 0
        self.state = "Начать"

        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        if self.next_figure is None:
            self.next_figure = Figure(3, 0)
        self.figure = self.next_figure
        self.next_figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2
        self.lines_cleared += lines  # Увеличиваем количество уничтоженных линий
        self.update_level()  # Проверяем, нужно ли повысить уровень

    def update_level(self):
        # Увеличиваем уровень каждые 10 уничтоженных линий
        if self.score >= self.level * 10:
            self.level += 1
            self.fall_speed = max(0.1, self.fall_speed - 0.05)  # Увеличиваем скорость падения

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()
    pass

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key != pygame.K_SPACE:
                    time.sleep(0.8)

        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color

        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "Конец игры"

    def go_side(self, dx):
        if self.figure is None:
            return
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation



pygame.init()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (600, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")


done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "Начать":
            game.go_down()

    keys = pygame.key.get_pressed()  # Получить текущее состояние всех клавиш
    if keys[pygame.K_DOWN]:
        pressing_down = True
    else:
        pressing_down = False  # Сбросить, когда клавиша не нажата

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
                pressing_down = False
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
                pressing_down = False
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
                pressing_down = False
            if event.key == pygame.K_SPACE:
                game.go_space()
                pressing_down = False
            if event.key == pygame.K_r:
                game.__init__(20, 10)
                pressing_down = False
            if event.key == pygame.K_ESCAPE:
                stopGame()

    def stopGame():
        pygame.quit()
        system().exit()

    def checkKeys():
        import sys
        sys.exit()

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pressing_down = False

    screen.fill(BLACK)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    next_figure_x = game.x + game.zoom * (game.width + 6) + 10  # Добавляем дополнительный отступ вправо
    next_figure_y = game.y  # Координата y остаётся прежней

    # Рисуем следующую фигуру в новом месте
    if game.next_figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.next_figure.image():
                    pygame.draw.rect(screen, colors[game.next_figure.color],
                                     [next_figure_x + game.zoom * j + 1,
                                      next_figure_y + game.zoom * i + 1,
                                      game.zoom - 2, game.zoom - 2])
    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    font2 = pygame.font.SysFont('Calibri', 100, True, False)
    text = font.render("Очки: " + str(game.score), True, WHITE)
    text_level = font.render(f"Уровень: {game.level}", True, (255, 255, 255))
    text_next_figure = font.render("Следующая фигура:", True, WHITE)

    text_game_over = font1.render("Конец игры", True, (255, 255, 255))
    text_game_over1 = font1.render("Повторить: R", True, (255, 255, 255))
    text_game_over2 = font1.render("Выйти:  Esc", True, (255, 255, 255))
    text_game_over3 = font1.render("Очки: " + str(game.score), True, (255, 255, 255))

    screen.blit(text_next_figure, [ 350, 10])
    screen.blit(text, [0, 0])
    screen.blit(text_level, [0, 30])

    if game.state == "Конец игры":
        screen.fill(BLACK)
        screen.blit(text_game_over, [20, 100])
        screen.blit(text_game_over1, [20, 165])
        screen.blit(text_game_over2, [20,230 ])
        screen.blit(text_game_over3, [20, 40])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
