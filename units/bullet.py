import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """ Class for control Ship Weapon"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.config = ai_game.config
        self.color = self.config.bullet_color

        # create bullet
        if ai_game.stats.level == 2:
            bullet_width = 10
        else:
            bullet_width = self.config.bullet_with
        self.rect = pygame.Rect(0, 0, bullet_width, self.config.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        """Bullet fly to top | Change bullet position"""

        self.y -= self.config.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
