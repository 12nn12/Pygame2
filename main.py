import sys
import pygame

from components.imagebutton import ImageButton
from components.life import Life

board_size = 26


def start_life(choice_life):
    global board_size
    pygame.init()
    size = (30 * board_size) + 20
    screen = pygame.display.set_mode((size, size))
    clock = pygame.time.Clock()
    if choice_life == 'Жизнь':
        pygame.display.set_caption('Игра «Жизнь»')
    elif choice_life == 'Жизнь на торе':
        pygame.display.set_caption('Игра «Жизнь на торе»')
    elif choice_life == 'Лабиринт':
        pygame.display.set_caption('Игра «Лабиринт»')
    random_sells = False
    board = Life(board_size, board_size, 10, 10, 30, random_sells, choice_life)
    random_button = ImageButton(400, 700, 252, 74, 'Рандом', './data/orange_button.jpg', './data/orange_button_1.png')
    clear_button = ImageButton(100, 700, 252, 74, 'Очистить', './data/orange_button.jpg', './data/orange_button_1.png')
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
                    button_clicked = not button_clicked
                    random_button.visible = True
                    random_button.active = True
                if event.button == clear_button:
                    random_sells = False
                    board = Life(26, 26, 10, 10, 30, random_sells, choice_life)
                    button_clicked = not button_clicked
                    clear_button.visible = True
                    clear_button.active = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v or event.key == pygame.K_SPACE:
                    if not random_button.visible:
                        random_button.visible = True
                        random_button.active = True
                        clear_button.visible = True
                        clear_button.active = True
                    else:
                        random_button.visible = False
                        random_button.active = False
                        clear_button.visible = False
                        clear_button.active = False
                if game_play:
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
    pygame.init()

    width, height = 600, 500

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Настройка размера')
    main_background = pygame.image.load('./data/fon.jpg')
    back_button = ImageButton(width / 2 - (252 / 2), 300, 252, 74, 'Назад', './data/red_button.jpg',
                              './data/red_button_1.jpg')
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
                    settings_menu()
            for btn in [back_button]:
                btn.handle_event(event)
        for btn in [back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main_menu()
