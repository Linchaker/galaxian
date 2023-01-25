class GameStats:
    """Statistics"""

    def __init__(self, ai_game):
        self.config = ai_game.config
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        """Init dymamic stats"""
        self.ships_left = self.config.ship_limit
        self.score = 0
        self.level = 1
