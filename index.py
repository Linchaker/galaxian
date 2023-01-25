import sys
from time import sleep

import pygame

from config import Config
from units.ship import Ship
from units.bullet import Bullet
from units.alien import Alien
from game_stats import GameStats
from units.button import Button
from units.scoreboard import Scoreboard


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

        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # create Buttons
        self.button_play = Button(self, "Play")


    def run_game(self):
        """Run game"""

        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Events handler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
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

    def _check_play_button(self, mouse_pos):
        """Start game by Play button"""
        button_clicked = self.button_play.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.config.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            # hidden mouse
            pygame.mouse.set_visible(False)

    def _update_screen(self):
        """Update screen image and switch to new screen"""
        # fill screen / add objects
        self.screen.fill(self.config.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        self.scoreboard.show_score()

        if not self.stats.game_active:
            self.button_play.draw_button()

        # update screen
        pygame.display.flip()

    def _fire_bullet(self):
        if len(self.bullets) < self.config.bullet_limit:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Make aliens fleet"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.config.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.config.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # make rows
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_bullet_alien_collisions(self):
        # check hits
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.config.alien_points * len(aliens)
        self.scoreboard.prep_score()
        self.scoreboard.check_high_score()

        if not self.aliens:
            # new level
            self.bullets.empty()
            self._create_fleet()
            self.config.increase_speed()
            # level up
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _check_aliens_bottom(self):
        """Check if alien is on bottom of screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # is like ship hit
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Change fleet row to another (below)"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.config.fleet_drop_speed
        self.config.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()
            # clear
            self.aliens.empty()
            self.bullets.empty()
            # reset
            self._create_fleet()
            self.ship.center_ship()
            # pause game
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


if __name__ == '__main__':
    # Init game
    ai = Galaxian()
    ai.run_game()
