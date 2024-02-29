import sys
import pygame

from components.imagebutton import ImageButton
from components.input import Input
from components.life import Life

board_size = 26


def start_life(choice_life):
    global board_size
    if board_size <= 0:
        board_size = 26
    pygame.init()
    screen_width = 1050
    screen_height = 900
    size = 800
    cell_size = (size - 10) // board_size
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    if choice_life:
        pygame.display.set_caption(f'Игра «{choice_life}»')
    random_sells = False
    board = Life(board_size, board_size, 10, 10, cell_size, random_sells, choice_life)
    clear_button = ImageButton(30, 800, 180, 50, 'Очистить', './data/orange_button.jpg', './data/orange_button_1.png')
    random_button = ImageButton(240, 800, 180, 50, 'Рандом', './data/orange_button.jpg', './data/orange_button_1.png')
    start_button = ImageButton(450, 800, 180, 50, 'Старт', './data/green_button.png', './data/green_button1.png')
    speed_button = ImageButton(870, 140, 40, 40, '+', './data/orange_button.jpg', './data/orange_button_1.png')
    speed_button2 = ImageButton(870, 230, 40, 40, '-', './data/orange_button.jpg', './data/orange_button_1.png')
    exit_button = ImageButton(660, 800, 180, 50, 'Выйти', './data/red_button.jpg', './data/red_button_1.jpg')
    clear_button2 = ImageButton(30, 800, 180, 50, 'Очистить', './data/gray_button.png', './data/gray_button.png')
    random_button2 = ImageButton(240, 800, 180, 50, 'Рандом', './data/gray_button.png', './data/gray_button.png')
    start_button2 = ImageButton(450, 800, 180, 50, 'Пауза', './data/orange_button.jpg', './data/orange_button_1.png')
    random_button2.visible = False
    clear_button2.visible = False
    start_button2.visible = False
    time_on = False
    ticks = 0
    speed = 10
    speed_screen = 10
    button_clicked = False
    game_play = False
    running = True
    while running:
        screen.fill((0, 0, 0))
        board.render(screen)
        font = pygame.font.Font(None, 30)
        text_surfase = font.render(f'Скорость: {speed_screen}', True, (255, 255, 255))
        text_rect = text_surfase.get_rect(center=(865, 30))
        screen.blit(text_surfase, text_rect)
        text_surfase3 = font.render(f'Добавить скорость:', True, (255, 255, 255))
        text_rect3 = text_surfase.get_rect(center=(865, 120))
        screen.blit(text_surfase3, text_rect3)
        text_surfase4 = font.render(f'Уменьшить скорость:', True, (255, 255, 255))
        text_rect4 = text_surfase.get_rect(center=(865, 210))
        screen.blit(text_surfase4, text_rect4)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click(event.pos)
            if (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == 3) or (
                    event.type == pygame.USEREVENT and event.button == start_button) or (
                    event.type == pygame.USEREVENT and event.button == start_button2):
                time_on = not time_on
                game_play = not game_play
                if not random_button.active:
                    random_button.active = True
                    clear_button.active = True
                    random_button.visible = True
                    clear_button.visible = True
                    start_button.visible = True
                    random_button2.visible = False
                    clear_button2.visible = False
                    start_button2.visible = False
                else:
                    random_button.active = False
                    clear_button.active = False
                    random_button.visible = False
                    clear_button.visible = False
                    start_button.visible = False
                    random_button2.visible = True
                    clear_button2.visible = True
                    start_button2.visible = True
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 4) or (
                    event.type == pygame.USEREVENT and event.button == speed_button2):
                speed += 1
                speed_screen -= 1
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 5) or (
                    event.type == pygame.USEREVENT and event.button == speed_button):
                speed -= 1
                speed_screen += 1
            if event.type == pygame.USEREVENT:
                if event.button == random_button:
                    random_sells = True
                    board = Life(board_size, board_size, 10, 10, cell_size, random_sells, choice_life)
                    button_clicked = not button_clicked
                    random_button.active = True
                if event.button == clear_button:
                    random_sells = False
                    board = Life(board_size, board_size, 10, 10, cell_size, random_sells, choice_life)
                    button_clicked = not button_clicked
                    clear_button.active = True
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (
                    event.type == pygame.USEREVENT and event.button == exit_button):
                main_menu()
            for btn in [random_button, clear_button, start_button, speed_button, speed_button2, exit_button,
                        random_button2, clear_button2, start_button2]:
                btn.handle_event(event)
        for btn in [random_button, clear_button, start_button, speed_button, speed_button2, exit_button, random_button2,
                    clear_button2, start_button2]:
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


def main_menu():
    pygame.init()

    width, height = 600, 500

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Главное меню')
    main_background = pygame.image.load('./data/fon.jpg')
    connect_button = ImageButton(width / 2 - (252 / 2), 100, 252, 74, 'Выбрать игру', './data/orange_button.jpg',
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
    life_button = ImageButton(30, 100, 200, 70, 'Жизнь', './data/orange_button.jpg', './data/orange_button_1.png',
                              './data/Life.gif')
    life_on_thor = ImageButton(250, 100, 200, 70, 'Жизнь на торе', './data/orange_button.jpg',
                               './data/orange_button_1.png', './data/Life_on_thor.gif')
    labyrinth = ImageButton(470, 100, 200, 70, 'Лабиринт', './data/orange_button.jpg', './data/orange_button_1.png',
                            './data/labyrinth.gif')
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

            for btn in [back_button, life_button, life_on_thor, labyrinth]:
                btn.handle_event(event)
        for btn in [back_button, life_button, life_on_thor, labyrinth]:
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
    size_button = ImageButton(width / 2 - (275 / 2), 120, 275, 60, 'Изменить размер поля', './data/orange_button.jpg',
                              './data/orange_button_1.png')
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (-800, -100))
        font = pygame.font.Font(None, 72)
        text_surfase = font.render('Настройки', True, (255, 255, 255))
        text_rect = text_surfase.get_rect(center=(300, 50))
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
                if event.button == size_button:
                    running = False
                    settings_menu_size()
            for btn in [back_button, size_button]:
                btn.handle_event(event)
        for btn in [back_button, size_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()


def changed(x):
    global board_size
    board_size = int(x and x or 0)


def settings_menu_size():
    global board_size
    size = board_size
    pygame.init()

    width, height = 600, 500

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Настройка размера')
    main_background = pygame.image.load('./data/fon.jpg')
    back_button = ImageButton(width / 2 - (252 / 2), 300, 252, 74, 'Назад', './data/red_button.jpg',
                              './data/red_button_1.jpg')
    size_button = ImageButton(width / 2 - (165 / 2), 160, 165, 45, 'Подтвердить', './data/green_button.png',
                              './data/green_button1.png')
    size_input = Input(width / 2 - (180 / 2), 110, 180, 30, text=str(board_size), changed=changed)
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (-800, -100))
        font1 = pygame.font.Font(None, 72)
        text_sive = font1.render('Введите размер поля:', True, (255, 255, 255))
        text_rect1 = text_sive.get_rect(center=(300, 60))
        screen.blit(text_sive, text_rect1)
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
                    settings_menu()
            if event.type == pygame.USEREVENT:
                if event.button == back_button:
                    running = False
                    board_size = size
                    settings_menu()
                if event.button == size_button:
                    running = False
                    if board_size <= 4:
                        board_size = 26
                    settings_menu()
            for btn in [back_button, size_button]:
                btn.handle_event(event)
        for btn in [back_button, size_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main_menu()
