import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.config = ai_game.config

        # set img
        self.image = pygame.image.load('images/tie.png')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)


    def update(self):
        """ Update current position"""
        self.x += (self.config.alien_speed * self.config.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """True if alien position is on end of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
