import copy

import pygame

from components.board import Board


class Life(Board):
    def __init__(self, width, height, left, top, cell_size, random_sells, choice_life):
        super().__init__(width, height, left, top, cell_size, random_sells, choice_life)

    def on_click(self, cell):
        self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x]:
                    pygame.draw.rect(screen, pygame.Color("green"),
                                     (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                      self.cell_size,
                                      self.cell_size))
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size,
                                  self.cell_size), 1)

    def next_move(self):
        tmp_board = copy.deepcopy(self.board)
        for y in range(self.height):
            for x in range(self.width):
                s = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if self.choice_life == 'Жизнь' or self.choice_life == 'Лабиринт':
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
        self.board = copy.deepcopy(tmp_board)
