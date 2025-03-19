import pygame

class DeathScreen:
    def __init__(self, screen, scene_manager):
        font = pygame.font.Font(None, 32)
        self.screen = screen
        self.scene_manager = scene_manager
        self.text = font.render("Ви померли на безкраїх просторах космосу. Яка прикрість", True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    
    def update_and_draw(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.scene_manager.exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.scene_manager.reset_game()
                    self.scene_manager.set_scene("game")
        self.screen.fill((0,0,0))
        self.screen.blit(self.text, self.text_rect)
        