# With omniscience the strategy is to know the secret word first, and then to guess it

from wordle import Wordle
from strategies.base import BaseStrategy


class OmniscienceStrategy(BaseStrategy):
    def __init__(self, game: Wordle) -> None:
        super().__init__(game)

    def get_guess(self) -> str:
        return self.game._secret_word
