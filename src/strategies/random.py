import random
from wordle import Wordle
from strategies.base import BaseStrategy

class RandomStrategy(BaseStrategy):
    def __init__(self, game: Wordle) -> None:
        super().__init__(game)
    
    def get_guess(self) -> str:
        return random.choice(self.game.words)