import random

import pygame


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
