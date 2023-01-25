import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_game, isMain = True):
        super().__init__()
        self.screen = ai_game.screen
        self.config = ai_game.config
        self.screen_rect = ai_game.screen.get_rect()

        # set img
        self.image = pygame.image.load('images/xwing.png')
        if not isMain:
            self.image = pygame.transform.scale(self.image, (50, 56))
        self.rect = self.image.get_rect()
        # image default position
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        # move indicator
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ Update current position by move indicator"""

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.config.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.config.ship_speed

        self.rect.x = self.x

    def blitme(self):
        """Draw ship in default position"""

        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
