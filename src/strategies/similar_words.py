import re
from absl import logging
from typing import Dict, List, Pattern, Sequence

from wordle import Wordle, Result, GuessResult
from strategies.random import BaseStrategy
from util.probabilities import Probabilities


class LetterInfo:
    def __init__(self, letter: str, word_length: int) -> None:
        self.letter = letter
        self._word_len = word_length
        # Minimum number of times this letter must be in the word
        self._min_count = 0
        self._max_count = word_length
        self._cur_count = 0
        # Whether we know if this letter is in word
        self._in_word = None
        # Whether this letter was marked as 'black'
        self._hit_black = False
        # Locations that the letter must be in or not be in
        self._must_be_here = [False] * word_length
        self._must_be_not_here = [False] * word_length
        self._mask_arr = ['.'] * word_length
        self._letter_mask = self._regen_mask_str()

    def _regen_mask_str(self) -> str:
        """Returns a string representing the mask for the secret word.

        The mask contains all of the information we know about the existence
        and location of this letter in the secret word, such as the number
        of times it must appear in the word, where it must appear, and 
        where it must not appear.
        """
        negate_letter = f'[^{self.letter}]'
        for i in range(0, self._word_len):
            if self._must_be_here[i]:
                self._mask_arr[i] = self.letter
            elif self._must_be_not_here[i] or self._in_word == False:
                # We know that if we hit black, then we can't have other occurences.
                self._mask_arr[i] = negate_letter
        # The lower an upper bounds of the number of times this letter must be seen.
        counts = f'{{{self._min_count},{self._max_count}}}'
        # Count how often this letter must be seen in string
        frequency_str = f'(?=^({negate_letter}*{self.letter}{negate_letter}*){counts}$)' if self._min_count else ''
        # Where the letter must be in the word.
        location_str = ''.join(self._mask_arr)
        # Combination of both frequency and location
        mask_str = frequency_str + location_str
        logging.debug(
            f'{self.letter}: min: {self._min_count}, max: {self._max_count} | regex: {mask_str}')
        return mask_str

    def set_info(self, index: int, result: Result):
        if result == Result.CORRECT:
            self._must_be_here[index] = True
            self._cur_count += 1
            self._in_word = True
        elif result == Result.INVALID:
            self._must_be_not_here[index] = True
            self._hit_black = True
            if self._in_word == None:
                self._in_word = False
        elif result == Result.IN_WORD:
            self._must_be_not_here[index] = True
            self._cur_count += 1
            self._in_word = True

    def end_of_word_calculations(self) -> None:
        self._min_count = max(self._min_count, self._cur_count)
        if self._hit_black:
            self._max_count = self._min_count
        self._cur_count = 0
        self._letter_mask = re.compile(self._regen_mask_str())

    def letter_mask(self) -> Pattern[str]:
        return self._letter_mask


class GuessManager:
    def __init__(self, game: Wordle, letter_info: Dict[str, LetterInfo] = None) -> None:
        self.game = game
        self.remaining_words = game.words
        # Tracks how many remaining words are left based on the number of guesses.
        self.remaining_words_tracker = [len(self.remaining_words)]
        self.letter_info = letter_info if letter_info else {}

    def _update_letter_infos(self, guess_result: GuessResult) -> None:
        guess, result = guess_result
        logging.debug(f'{self.game._secret_word} | {guess}: {result}')
        for i, r in enumerate(result):
            c = guess[i]
            if c not in self.letter_info.keys():
                self.letter_info[c] = LetterInfo(c, self.game.word_len)
            self.letter_info[c].set_info(i, r)
        unique_letters = set(guess)
        for c in unique_letters:
            self.letter_info[c].end_of_word_calculations()

    def _update_remaining_words(self) -> None:
        """Eliminate words that are no longer candidates."""
        num_words = len(self.remaining_words)
        candidate_words = []
        for w in self.remaining_words:
            match_all = True
            for letter_info in self.letter_info.values():
                if not letter_info.letter_mask().match(w):
                    match_all = False
                    break
            if match_all:
                candidate_words.append(w)
        self.remaining_words = candidate_words
        self.remaining_words_tracker.append(len(self.remaining_words))
        logging.debug(
            f'{len(self.remaining_words)} words remain. (Removed {num_words - len(self.remaining_words)})')

    def update(self, guess_result: GuessResult) -> List[str]:
        self._update_letter_infos(guess_result)
        self._update_remaining_words()
        return self.remaining_words


class SimilarWordsStrategy(BaseStrategy):
    def __init__(self, game: Wordle) -> None:
        super().__init__(game)
        self.guess_manager = GuessManager(game)
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
