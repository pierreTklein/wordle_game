# The amount of 'information' a guess gives is the average amount of words that it eliminates from the pool
# For each guess calculate the amount of infomation, choose the best
# May take an actual eternity

# estimate information based on sample pool?

# lmao ai?


from cmath import inf
from faulthandler import cancel_dump_traceback_later
from tkinter.tix import INTEGER

from sklearn.metrics import pairwise_distances
from util.guess_manager import GuessManager
from wordle import GuessResult, Result, Wordle
from strategies.base import BaseStrategy
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple


class MaximalInformationStrategy(BaseStrategy):
    # pool of valid words
    valid_word_pool: List[str]

    def __init__(self, game: Wordle) -> None:
        super().__init__(game)
        self.valid_word_pool = game.words

    def get_guess(self) -> str:
        if len(self.valid_word_pool) == 1:
            return self.valid_word_pool[0]

        best_word = "hello"
        best_info = -inf
        for word in self.valid_word_pool:
            info = self.calculate_information(word)
            if info > best_info:
                best_info = info
                best_word = word

        # print("get_guess", best_word, best_info)
        # print("get_guess", self.valid_word_pool)
        return best_word

    def make_guess(self, guess: str) -> GuessResult:
        guess_result: GuessResult = super().make_guess(guess)
        self.valid_word_pool = self.update_word_pool(
            self.valid_word_pool, guess_result)
        # print("make_guess", guess_result)
        return guess_result

    def calculate_information(self, guess: str):
        est_game = Wordle(self.valid_word_pool, 1, 5, None)
        info = 0
        for word in self.valid_word_pool:
            est_game.reset(word)
            guess_result: GuessResult = est_game.guess(guess)
            info += self.get_information(self.valid_word_pool, guess_result)
        # print(info, guess)
        return info

    def update_word_pool(self, word_pool: List[str], guess_result: GuessResult):
        new_word_pool: List[str] = []
        for word in word_pool:
            if self.is_valid_word(word, guess_result):
                new_word_pool.append(word)
        return new_word_pool

    def get_information(self, word_pool: List[str], guess_result: GuessResult):
        removed_count = 0
        for word in word_pool:
            if not self.is_valid_word(word, guess_result):
                removed_count += 1
        return removed_count

    def is_valid_word(self, word: str, guess_result: GuessResult):
        # step 1 - check for correct letter counts
        word_map = self.construct_word_map(word)
        guess_map = self.construct_guess_map(guess_result)
        if (not self.check_word_maps(word_map, guess_map)):
            return False

        # step 2 - check for correct letter placements
        for i, result in enumerate(guess_result.result):
            if result == Result.CORRECT and word[i] != guess_result.guess[i]:
                return False
        return True

    def construct_guess_map(self, guess_result: GuessResult):
        letterCounts = dict()
        guess_word = guess_result.guess
        for i, result in enumerate(guess_result.result):
            letter = guess_word[i]
            if result == Result.CORRECT or result == Result.IN_WORD:
                letterCounts[letter] = letterCounts.get(letter, 0) + 1
            if result == Result.INVALID:
                letterCounts[letter] = letterCounts.get(letter, 0)
        return letterCounts

    # Input - word
    # Output - map from letters in word to count of those letters
    def construct_word_map(self, word: str):
        letterCounts = dict()
        for letter in word:
            letterCounts[letter] = letterCounts.get(letter, 0) + 1
        return letterCounts

    # Input - map of letters in word to count of those letters
    # Input - map of letters in guess
    # Output - boolaen of whether the counts of letters from word is possible from guess map
    def check_word_maps(self, word_map, guess_map):
        for key, value in guess_map.items():
            # check for letters that definitively don't exist from guess
            if value == 0:
                if word_map.get(key, 0) > 0:
                    return False
            # the letters that are in the guess must exist in the word
            else:
                if word_map.get(key, 0) < guess_map.get(key, 0):
                    return False
        return True
