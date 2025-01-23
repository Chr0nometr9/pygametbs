import pygame

class Button:
    def __init__(self,
                text : str,
                font : pygame.font.Font,
                size : tuple = None,
                position : tuple = (0, 0),
                color_text : tuple = (0, 0, 0),
                color_bg : tuple = (150, 150, 150),
                callback = None):

        self.text = text
        self.font = font

        if not size:
            w_text, h_text = font.size(text)
            self.size = (w_text * 1.3, h_text * 1.3)

        self.position = position
        self.rect = pygame.Rect(self.position, self.size)

        self.color_text = color_text
        self.current_color = self.color_text
        self.color_bg = color_bg

        self.callback = callback
        self.mouse_over = False

    def handle(self, event : pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_over = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONUP and self.mouse_over:
            if event.button == 1:
                if not self.callback is None:
                    self.callback()

    def render(self, screen):
        button_surface = pygame.Surface(self.size)
        button_surface_rect = button_surface.get_rect()

        if self.mouse_over:
            self.current_color = (255, 255, 255)
        else:
            self.current_color = self.color_text

        text_surface = self.font.render(self.text, True, self.current_color)
        text_rect = text_surface.get_rect()
        text_rect.center = button_surface_rect.center

        button_surface.fill(self.color_bg)
        button_surface.blit(text_surface, text_rect)

        screen.blit(button_surface, self.position)
