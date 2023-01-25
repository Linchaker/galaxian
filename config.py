class Config:

    def __init__(self):
        # Screen settings
        self.screen_width = 1380
        self.screen_height = 768
        self.bg_color = "#A6A6AA"

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_with = 5
        self.bullet_height = 20
        self.bullet_color = "darkred"
        self.bullet_limit = 5

        # Aliens
        self.fleet_drop_speed = 40

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 2.0
        self.bullet_speed = 1.5
        self.alien_speed = 0.5
        self.alien_points = 50

        # right 1, left -1
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points *= int(self.score_scale * self.score_scale)
