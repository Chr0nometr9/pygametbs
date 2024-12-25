import pygame

class Button:
    def __init__(self,
                text : str,
                font : pygame.font.Font,
                size : tuple = None,
                color_text : tuple = (0, 0, 0),
                color_bg : tuple = (150, 150, 150)):
        self.text = text
        self.font = font
        
        if not size:
            w_text, h_text = font.size(text)
            self.size = (w_text * 1.3, h_text * 1.3)

        self.color_text = color_text
        self.color_bg = color_bg

    def render(self, mouse_x, mouse_y):
        button_surface = pygame.Surface(self.size)
        button_surface_rect = button_surface.get_rect()

        color = self.color_text
        if button_surface_rect.collidepoint(mouse_x, mouse_y):
            color = (255, 255, 255)

        text_surface = self.font.render(self.text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = button_surface_rect.center

        button_surface.fill(self.color_bg)
        button_surface.blit(text_surface, text_rect)

        return button_surface
        
        
        
