class Game:
    def __init__(self):
        self.answer = None
        self.game_over = False
        self.started = False
        self.timer = 60
        # SCORE
        self.characters_count = 0
        self.correct_words = 0
        self.incorrect_words = 0
