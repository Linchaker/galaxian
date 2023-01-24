class Config:

    def __init__(self):
        # Screen settings
        self.screen_width = 1380
        self.screen_height = 768
        self.bg_color = "#A6A6AA"

        # Ship settings
        self.ship_speed = 3.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 2.0
        self.bullet_with = 10
        self.bullet_height = 20
        self.bullet_color = "darkred"
        self.bullet_limit = 10

        # Aliens
        self.alien_speed = 2.0
        self.fleet_drop_speed = 100
        # right 1, left -1
        self.fleet_direction = 1

