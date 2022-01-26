import re

from wordle import Wordle, Result, GuessResult
from strategies.random import BaseStrategy
from util.probabilities import Probabilities


class SimilarWordStrategy(BaseStrategy):
    def __init__(self, game: Wordle) -> None:
        super().__init__(game)
        self.remaining_words = game.words
        self.probabilities = Probabilities(game.words, game.word_len)

        # Letter Trackers
        self.bad_letters = set()
        self.good_letters = [None] * self.game.word_len
        self.not_here_letters = [set(), set(), set(), set(), set()]
        pass

    def _update_letter_trackers(self, guess_result: GuessResult) -> None:
        guess, result = guess_result
        for i, r in enumerate(result):
            if r == Result.CORRECT:
                self.good_letters[i] = guess[i]
            elif r == Result.INVALID:
                self.bad_letters.add(guess[i])
            else:
                self.not_here_letters[i].add(guess[i])

    def _gen_candidate_word_mask(self) -> str:
        """Generate a regex string that contains info we know about the secret word."""
        candidate_mask = ['.', '.', '.', '.', '.']
        for i in range(0, self.game.word_len):
            if self.good_letters[i]:
                # The letter in this position must be good_letters[i]
                candidate_mask[i] = self.good_letters[i]
            elif self.not_here_letters[i] or self.bad_letters:
                # The letter in this position should not be a bad letter or a not_here letter.
                candidate_mask[i] = ''.join(
                    ('[^', ''.join(self.bad_letters), ''.join(self.not_here_letters[i]), ']'))
        return ''.join(candidate_mask)

    def _update_remaining_words(self) -> None:
        """Eliminate words that are no longer candidates."""
        mask = self._gen_candidate_word_mask()
        regex = re.compile(mask)
        num_words = len(self.remaining_words)
        self.remaining_words = list(
            filter(lambda w: regex.fullmatch(w), self.remaining_words))
        print(f'{len(self.remaining_words)} words remain. (Removed {num_words - len(self.remaining_words)})')

    def get_guess(self) -> str:
        """Use highest-shared-letters strategy to makethe guess."""
        shared_letters_arr = self.probabilities.highest_shared_letters()
        index = 0
        return shared_letters_arr[index][0]

    def make_guess(self, guess_word: str) -> GuessResult:
        guess_result = self.game.guess(guess_word)
        self._update_letter_trackers(guess_result)
        self._update_remaining_words()
        self.probabilities = Probabilities(
            self.remaining_words, self.game.word_len)
        return guess_result
