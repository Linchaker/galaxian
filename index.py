import sys

import pygame

from config import Config
from units.ship import Ship
from units.bullet import Bullet


class Galaxian:
    """Main class of game"""

    def __init__(self):
        pygame.init()

        self.config = Config()
        # self.screen = pygame.display.set_mode((self.config.screen_width, self.config.screen_height))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.config.screen_width = self.screen.get_rect().width
        self.config.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Galaxian")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Run game"""

        while True:
            self._check_events()
            self.ship.update()
            self._update_bullet()

            self._update_screen()

    def _check_events(self):
        """Events handler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # start move ship to right
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            # start move ship to left
            self.ship.moving_left = True
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            # stop move ship to right
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            # stop move ship to left
            self.ship.moving_left = False

    def _update_screen(self):
        """Update screen image and switch to new screen"""
        # fill screen / add objects
        self.screen.fill(self.config.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # update screen
        pygame.display.flip()

    def _fire_bullet(self):
        if len(self.bullets) < self.config.bullet_limit:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullet(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

if __name__ == '__main__':
    # Init game
    ai = Galaxian()
    ai.run_game()
