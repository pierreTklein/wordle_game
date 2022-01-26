import random
from wordle import Wordle
from wordle_solver_base import WordleSolverBase

class WordleSolverRandom(WordleSolverBase):
    def __init__(self, game: Wordle) -> None:
        super().__init__(game)
    
    def get_guess(self) -> str:
        return random.choice(self.game.words)