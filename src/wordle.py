from absl import logging
from collections import Counter
from enum import Enum
import random
from typing import List, NamedTuple, Optional, Sequence, Tuple


class Result(Enum):
    CORRECT = 1
    IN_WORD = 2
    INVALID = 3


class GuessResult(NamedTuple):
    guess: str
    result: Tuple[Result]


class GameResult(NamedTuple):
    # The secret word for this game.
    secret_word: str
    # The score of the game
    score: int
    # Words that were guessed in the game
    guessed_words: Sequence[str]
    # Runtime, in seconds
    runtime: float


class GuessValidation(NamedTuple):
    is_valid: bool
    error: Optional[str]


class Wordle:
    def __init__(self, words: List[str], num_tries_initial: int, word_len: int, hard_mode=False, prev_guesses: Optional[List[GuessResult]] = None) -> None:
        self.hard_mode = hard_mode
        self.word_len = word_len
        self.words = words
        self.word_set = set(words)
        self._secret_word = random.choice(seq=words)
        self._secret_word_counts = Counter(self._secret_word)
        self.guesses = prev_guesses if prev_guesses else []
        self.num_tries_initial = num_tries_initial
        self.num_tries_remaining = num_tries_initial

    def _set_secret_word(self, secret_word: str) -> None:
        if len(secret_word) != self.word_len:
            raise Exception(
                f'{secret_word} is not the proper word length ({len(secret_word)} instead of {self.word_len}).')

        if secret_word not in self.word_set:
            raise Exception(f'{secret_word} is not in set of available words.')

        self._secret_word = secret_word
        self._secret_word_counts = Counter(secret_word)

    @classmethod
    def from_file(cls, path: str, num_tries_initial: int = 6, hard_mode=False) -> "Wordle":
        with open(path, "r") as file:
            words = list(map(lambda x: x.strip(), file.readlines()))
            if not len(words):
                # The word list must be non-empty
                raise Exception(f'{path} has zero words.')

            word_len = len(words[0])
            for w in words:
                # All words must be the same length
                if len(w) != word_len:
                    raise Exception(
                        f'Not all words in {path} are of the same length.')

            return cls(words, num_tries_initial=num_tries_initial, word_len=word_len, hard_mode=hard_mode)

    def can_guess(self) -> bool:
        return self.num_tries_remaining > 0

    def is_valid_guess(self, guess_word: str) -> GuessValidation:
        if len(guess_word) != self.word_len:
            return GuessValidation(False, f'{guess_word} is invalidd length.')

        if self.hard_mode:
            # Hard mode is where you need to use all letters that are IN_WORD or CORRECT.
            required_letters = set()
            required_positions = [None] * self.word_len
            for guess_result in self.guesses:
                for i, result in enumerate(guess_result.result):
                    if result == Result.CORRECT or result == Result.IN_WORD:
                        required_letters.add(guess_result.guess[i])
                    if result == Result.CORRECT:
                        required_positions[i] = guess_result.guess[i]
            # Guess word must have all required letters
            guess_word_set = set([*guess_word])
            missing_letters = required_letters.difference(guess_word_set)

            if missing_letters:
                return GuessValidation(False, f'[{", ".join(missing_letters)}] must be in the guess word.')

            for i, letter in enumerate(guess_word):
                if required_positions[i] and required_positions[i] != letter:
                    return GuessValidation(False, f'The letter {required_positions[i]} must be at position {i+1}.')

        if guess_word not in self.word_set:
            return GuessValidation(False, f'{guess_word} is not a valid guess.')

        return GuessValidation(True, None)

    def guess(self, guess_word: str) -> GuessResult:
        if self.num_tries_remaining <= 0:
            raise Exception('No more guesses available.')

        validation_check = self.is_valid_guess(guess_word)
        if not validation_check.is_valid:
            raise Exception(validation_check.error)

        self.num_tries_remaining -= 1
        results = []
        mapping = self._secret_word_counts.copy()
        for i, c in enumerate(guess_word):
            if self._secret_word[i] == c:
                results.append(Result.CORRECT)
                mapping[c] -= 1
            else:
                results.append(Result.INVALID)
        for i, c in enumerate(guess_word):
            # Make it known if there is an available match elsewhere
            if results[i] == Result.INVALID and mapping[c]:
                mapping[c] -= 1
                results[i] = Result.IN_WORD
        guess_result = GuessResult(guess_word, tuple(results))
        self.guesses.append(guess_result)
        return guess_result

    def get_guessed_words(self) -> List[str]:
        return list(map(lambda t: t[0], self.guesses))

    def has_won(self) -> bool:
        if self.guesses:
            return self.guesses[-1][0] == self._secret_word
        else:
            return False

    def get_score(self) -> int:
        return len(self.guesses) if self.has_won() else -1

    def rig_game(self, secret_word: str):
        self._set_secret_word(secret_word)

    def reset(self, secret_word: Optional[str] = None):
        if secret_word:
            self._set_secret_word(secret_word)
        else:
            self._set_secret_word(random.choice(self.words))
        self.guesses = []
        self.num_tries_remaining = self.num_tries_initial
