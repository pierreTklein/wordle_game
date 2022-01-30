from collections import Counter
from enum import Enum
import random
from typing import Dict, List, Optional, Tuple


class Result(Enum):
    CORRECT = 1
    IN_WORD = 2
    INVALID = 3


GuessResult = Tuple[str, Tuple[Result]]


class Wordle:
    def __init__(self, words: List[str], word_len: int = 5, num_tries_initial: int = 5, prev_guesses: Optional[List[GuessResult]] = None) -> None:
        self.word_len = word_len
        self.words = words
        self._secret_word = random.choice(seq=words)
        self._secret_word_counts = Counter(self._secret_word)
        self.guesses = prev_guesses if prev_guesses else []
        self.num_tries_initial = num_tries_initial
        self.num_tries_remaining = num_tries_initial

    def _set_secret_word(self, secret_word: str) -> None:
        self._secret_word = secret_word
        self._secret_word_counts = Counter(secret_word)

    @classmethod
    def from_file(cls, path: str, num_tries_initial: int = 5) -> "Wordle":
        with open(path, "r") as file:
            return cls(list(map(lambda x: x.strip(), file.readlines())), num_tries_initial=num_tries_initial)

    def can_guess(self) -> bool:
        return self.num_tries_remaining > 0

    def is_valid_guess(self, guess_word: str) -> bool:
        return guess_word in self.words

    def guess(self, guess_word: str) -> GuessResult:
        if self.num_tries_remaining <= 0:
            raise Exception('No more guesses available.')

        if not self.is_valid_guess(guess_word):
            raise Exception(f'{guess_word} is not a valid word.')

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
        guess_result = (guess_word, tuple(results))
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

    def reset(self):
        self._set_secret_word(random.choice(self.words))
        self.guesses = []
        self.num_tries_remaining = self.num_tries_initial
