from wordle import Wordle, GuessResult
from strategies.random import BaseStrategy
from util.guess_manager import GuessManager
from util.probabilities import Probabilities


class SimilarWordsStrategy(BaseStrategy):
    def __init__(self, game: Wordle) -> None:
        super().__init__(game)
        self.guess_manager = GuessManager(game.words, game.word_len)
        self.probabilities = Probabilities(game.words, game.word_len)

    def get_guess(self) -> str:
        """Use highest-shared-letters strategy to makethe guess."""
        shared_letters_arr = self.probabilities.highest_shared_letters()
        index = 0
        return shared_letters_arr[index][0]

    def make_guess(self, guess_word: str) -> GuessResult:
        guess_result = self.game.guess(guess_word)
        remaining_words = self.guess_manager.update(guess_result)
        self.probabilities = Probabilities(
            remaining_words, self.game.word_len)
        return guess_result
