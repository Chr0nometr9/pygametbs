import pygame

def text(text, size=32, color=(255, 255, 255)):
        font = pygame.font.Font(None, size)
        return font.render(text, True, color)

class Menu:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.title_text = text("PyGameTDS", 72)
        self.title_rect = self.title_text.get_rect()
        self.title_rect.center = self.screen.get_width() // 2, 150

        self.new_game_text = text("Нова гра", 32)
        self.new_game_rect = self.new_game_text.get_rect()
        self.new_game_rect.center = self.screen.get_width() // 2, 300

    def update_and_draw(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.scene_manager.exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.new_game_rect.collidepoint(event.pos):
                    self.scene_manager.set_scene("game")
            if event.type == pygame.MOUSEMOTION:
                if self.new_game_rect.collidepoint(event.pos):
                    self.new_game_text = text("Нова гра", 32, color=(0, 150, 0))
                else:
                    self.new_game_text = text("Нова гра", 32)

        self.screen.fill((0, 0, 0))
        
        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.new_game_text, self.new_game_rect)
