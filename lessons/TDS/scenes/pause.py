import pygame

def text(text, size=32, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    return font.render(text, True, color)

class Pause:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.title_text = text("Пауза", 72)
        self.title_rect = self.title_text.get_rect()
        self.title_rect.center = self.screen.get_width() // 2, 150

        self.continue_text = text("Продовжити", 32)
        self.continue_rect = self.continue_text.get_rect()
        self.continue_rect.center = self.screen.get_width() // 2, 300

    def update_and_draw(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.scene_manager.exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.continue_rect.collidepoint(event.pos):
                    self.scene_manager.set_scene("game")
            if event.type == pygame.MOUSEMOTION:
                if self.continue_rect.collidepoint(event.pos):
                    self.continue_text = text("Продовжити", 32, color=(0, 150, 0))
                else:
                    self.continue_text = text("Продовжити", 32)

        self.screen.blit(self.scene_manager.background_surface, (0, 0))
        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.continue_text, self.continue_rect)