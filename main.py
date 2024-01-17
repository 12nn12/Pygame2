import sys
import pygame
import random
import copy


class Input:
    def __init__(self, x, y, w, h, font_color=(255, 255, 255), active_color=(255, 0, 0), inactive_color=(150, 150, 150),
                 text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = inactive_color
        self.text = text
        self.font_color = font_color
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.font_color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.active_color if self.active else self.inactive_color
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 10 and event.unicode.isdigit():
                        self.text += event.unicode
                self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.font_color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 3)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))


class Board:
    def __init__(self, width, height, left, top, cell_size, random_sells, choice_life):
        self.width = width
        self.height = height
        self.board = board_sells(width, height, random_sells)
        self.left = 20
        self.top = 20
        self.cell_size = 30
        self.set_view(left, top, cell_size)
        self.choice_life = choice_life

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size,
                                  self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def on_click(self, cell):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


def board_sells(width, height, random_sells):
    if random_sells:
        return [[random.randint(0, 1) for i in range(width)] for _ in range(height)]
    else:
        return [[0] * width for i in range(height)]


class Life(Board):
    def __init__(self, width, height, left, top, cell_size, random_sells, choice_life):
        super().__init__(width, height, left, top, cell_size, random_sells, choice_life)

    def on_click(self, cell):
        self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x]:
                    # живые клетки рисуем зелеными
                    pygame.draw.rect(screen, pygame.Color("green"),
                                     (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                      self.cell_size,
                                      self.cell_size))
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size,
                                  self.cell_size), 1)

    def next_move(self):
        # сохраняем поле
        tmp_board = copy.deepcopy(self.board)
        # пересчитываем
        for y in range(self.height):
            for x in range(self.width):
                # сумма окружающих клеток
                s = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if self.choice_life == 'Жизнь' or self.choice_life == 'Лабиринт' or self.choice_life == 'Тест':
                            if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                                continue
                            s += self.board[y + dy][x + dx]
                        elif self.choice_life == 'Жизнь на торе':
                            new_x = (x + dx) % self.width
                            new_y = (y + dy) % self.height
                            s += self.board[new_y][new_x]

                s -= self.board[y][x]
                if self.choice_life == 'Жизнь' or self.choice_life == 'Жизнь на торе':
                    if s == 3:
                        tmp_board[y][x] = 1
                    elif s < 2 or s > 3:
                        tmp_board[y][x] = 0
                elif self.choice_life == 'Лабиринт':
                    if s == 3 and self.board[y][x] == 0:
                        tmp_board[y][x] = 1
                    elif (s < 1 or s > 4) and self.board[y][x] == 1:
                        tmp_board[y][x] = 0
                elif self.choice_life == 'Тест':
                    if s == 3 and self.board[y][x] == 0:
                        tmp_board[y][x] = 1
                    elif (s < 2 or s > 5) and self.board[y][x] == 1:
                        tmp_board[y][x] = 0
        # обновляем поле
        self.board = copy.deepcopy(tmp_board)


def start_life(choice_life):
    pygame.init()
    size = 800, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    if choice_life == 'Жизнь':
        pygame.display.set_caption('Игра «Жизнь»')
    elif choice_life == 'Жизнь на торе':
        pygame.display.set_caption('Игра «Жизнь на торе»')
    elif choice_life == 'Лабиринт':
        pygame.display.set_caption('Игра «Лабиринт»')
    elif choice_life == 'Тест':
        pygame.display.set_caption('Игра «Тест»')
    random_sells = False
    board = Life(26, 26, 10, 10, 30, random_sells, choice_life)
    random_button = ImageButton(400, 700, 252, 74, 'Рандом', './data/orange_button.jpg', './data/orange_button_1.png')
    clear_button = ImageButton(100, 700, 252, 74, 'Очистить', './data/orange_button.jpg', './data/orange_button_1.png')
    # Включено ли обновление поля
    time_on = False
    ticks = 0
    speed = 10
    button_clicked = False
    game_play = False
    running = True
    while running:
        screen.fill((0, 0, 0))
        board.render(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click(event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                time_on = not time_on
                game_play = not game_play
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                speed += 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                speed -= 1
            if event.type == pygame.USEREVENT:
                if event.button == random_button:
                    random_sells = True
                    board = Life(26, 26, 10, 10, 30, random_sells, choice_life)
                    button_clicked = not button_clicked  # Инвертируем флаг после нажатия
                    # Восстанавливаем видимость и активность кнопки
                    random_button.visible = True
                    random_button.active = True
                if event.button == clear_button:
                    random_sells = False
                    board = Life(26, 26, 10, 10, 30, random_sells, choice_life)
                    button_clicked = not button_clicked  # Инвертируем флаг после нажатия
                    # Восстанавливаем видимость и активность кнопки
                    clear_button.visible = True
                    clear_button.active = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v or event.key == pygame.K_SPACE:
                    # Если кнопка была скрыта, восстанавливаем её видимость и активность
                    if not random_button.visible:
                        random_button.visible = True
                        random_button.active = True
                        clear_button.visible = True
                        clear_button.active = True
                    else:
                        # Иначе скрываем и делаем неактивной
                        random_button.visible = False
                        random_button.active = False
                        clear_button.visible = False
                        clear_button.active = False
                if game_play:
                    # Иначе скрываем и делаем неактивной
                    random_button.visible = False
                    random_button.active = False
                    clear_button.visible = False
                    clear_button.active = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu()
            for btn in [random_button, clear_button]:
                btn.handle_event(event)
        for btn in [random_button, clear_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
        if ticks >= speed:
            if time_on:
                board.next_move()
            ticks = 0
        pygame.display.flip()
        clock.tick(100)
        ticks += 1
    pygame.quit()


class ImageButton:

    def __init__(self, x, y, width, height, text, image_path, hover_image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = pygame.image.load(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        self.visible = True  # Добавлен флаг видимости
        self.active = True  # Добавлен флаг активности

    def draw(self, screen):
        if self.visible:
            current_image = self.hover_image if self.is_hovered else self.image
            screen.blit(current_image, self.rect.topleft)

            font = pygame.font.Font(None, 36)
            text_surfase = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surfase.get_rect(center=self.rect.center)
            screen.blit(text_surfase, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.visible and self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if self.active and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


def main_menu():
    pygame.init()

    width, height = 600, 500

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Главное меню')
    main_background = pygame.image.load('./data/fon.jpg')
    connect_button = ImageButton(width / 2 - (252 / 2), 100, 252, 74, 'Подключиться', './data/orange_button.jpg',
                                 './data/orange_button_1.png')
    settings_button = ImageButton(width / 2 - (252 / 2), 200, 252, 74, 'Настройки', './data/orange_button.jpg',
                                  './data/orange_button_1.png')
    exit_button = ImageButton(width / 2 - (252 / 2), 300, 252, 74, 'Выйти', './data/red_button.jpg',
                              './data/red_button_1.jpg')
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (-600, - 700))

        font = pygame.font.Font(None, 72)
        text_surfase = font.render('Главное меню', True, (255, 255, 255))
        text_rect = text_surfase.get_rect(center=(300, 50))
        screen.blit(text_surfase, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.button == settings_button:
                    settings_menu()
                if event.button == connect_button:
                    choice_game()
                if event.button == exit_button:
                    running = False
                    pygame.quit()
                    sys.exit()

            for btn in [connect_button, settings_button, exit_button]:
                btn.handle_event(event)
        for btn in [connect_button, settings_button, exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()


def choice_game():
    pygame.init()

    width, height = 700, 500

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Выбор игры')
    main_background = pygame.image.load('./data/fon.jpg')
    life_button = ImageButton(30, 100, 200, 70, 'Жизнь', './data/orange_button.jpg', './data/orange_button_1.png')
    life_on_thor = ImageButton(250, 100, 200, 70, 'Жизнь на торе', './data/orange_button.jpg',
                               './data/orange_button_1.png')
    labyrinth = ImageButton(470, 100, 200, 70, 'Лабиринт', './data/orange_button.jpg', './data/orange_button_1.png')
    test = ImageButton(30, 200, 200, 70, 'Тест', './data/orange_button.jpg', './data/orange_button_1.png')
    back_button = ImageButton(width / 2 - (252 / 2), 350, 252, 74, 'Назад', './data/red_button.jpg',
                              './data/red_button_1.jpg')
    running = True
    while running:
        screen.fill((0, 0, 0))

        screen.blit(main_background, (-800, -100))
        font = pygame.font.Font(None, 72)
        text_surfase = font.render('Выбор игры', True, (255, 255, 255))
        text_rect = text_surfase.get_rect(center=(350, 50))
        screen.blit(text_surfase, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    main_menu()
            if event.type == pygame.USEREVENT:
                if event.button == back_button:
                    running = False
                    main_menu()
                if event.button == life_button:
                    start_life('Жизнь')
                if event.button == life_on_thor:
                    start_life('Жизнь на торе')
                if event.button == labyrinth:
                    start_life('Лабиринт')
                if event.button == test:
                    start_life('Тест')

            for btn in [back_button, life_button, life_on_thor, labyrinth, test]:
                btn.handle_event(event)
        for btn in [back_button, life_button, life_on_thor, labyrinth, test]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()


def settings_menu():
    pygame.init()

    width, height = 600, 500

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Настроки')
    main_background = pygame.image.load('./data/fon.jpg')
    back_button = ImageButton(width / 2 - (252 / 2), 300, 252, 74, 'Назад', './data/red_button.jpg',
                              './data/red_button_1.jpg')
    size_input = Input(220, 140, 150, 30)
    running = True
    while running:
        screen.fill((0, 0, 0))

        screen.blit(main_background, (-800, -100))
        font = pygame.font.Font(None, 72)
        font1 = pygame.font.Font(None, 40)
        text_surfase = font.render('Настройки', True, (255, 255, 255))
        text_description = font1.render('Введите количество клеток на поле:', True, (255, 255, 255))
        text_rect = text_surfase.get_rect(center=(300, 50))
        screen.blit(text_surfase, text_rect)
        text_rect = text_description.get_rect(center=(300, 100))
        screen.blit(text_description, text_rect)
        size_input.draw(screen)

        for event in pygame.event.get():
            size_input.handle_event(event)
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    main_menu()
            if event.type == pygame.USEREVENT:
                if event.button == back_button:
                    running = False
                    main_menu()
            for btn in [back_button]:
                btn.handle_event(event)
        for btn in [back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main_menu()
