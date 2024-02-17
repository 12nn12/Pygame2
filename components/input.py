import pygame


class Input:
    def __init__(self, x, y, w, h, font_color=(255, 255, 255), active_color=(255, 0, 0), inactive_color=(150, 150, 150),
                 text='', changed=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = inactive_color
        self.text = text
        self.font_color = font_color
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.font_color)
        self.active = False
        self.changed = changed

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
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                else:
                    if len(self.text) < 12 and event.unicode.isdigit():
                        self.text += event.unicode
                if self.changed:
                    self.changed(self.text)
                self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.font_color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 3)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
