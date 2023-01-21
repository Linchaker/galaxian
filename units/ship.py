import pygame


class Ship:

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.config = ai_game.config
        self.screen_rect = ai_game.screen.get_rect()

        # set img
        self.image = pygame.image.load('images/xwing.png')
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
