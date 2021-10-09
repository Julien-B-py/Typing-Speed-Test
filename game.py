import random

from words import WORDS


class Game:
    def __init__(self):
        self.answer = None
        self.current_word = 0
        self.game_over = False
        self.started = False
        self.timer = 60
        # SCORE
        self.characters_count = 0
        self.correct_words = 0
        self.incorrect_words = 0
        # RANDOMIZE WORDS LIST
        self.randomize_words_order()

    def randomize_words_order(self):
        self.list_of_words = WORDS
        random.shuffle(self.list_of_words)
        self.game_text = ' '.join(self.list_of_words)
