from enum import Enum
import random
from typing import List, Optional, Tuple


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
        self.guesses = prev_guesses if prev_guesses else []
        self.num_tries_initial = num_tries_initial
        self.num_tries_remaining = num_tries_initial

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
        for i, c in enumerate(guess_word):
            if self._secret_word[i] == c:
                results.append(Result.CORRECT)
            elif c in self._secret_word:
                results.append(Result.IN_WORD)
            else:
                results.append(Result.INVALID)
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

    def rig_game(self, secret_word: str):
        self._secret_word = secret_word

    def reset(self):
        self._secret_word = random.choice(self.words)
        self.guesses = []
        self.num_tries_remaining = self.num_tries_initial
