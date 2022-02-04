# The amount of 'information' a guess gives is the average amount of words that it eliminates from the pool
# For each guess calculate the amount of infomation, choose the best
# May take an actual eternity

# estimate information based on sample pool?

# lmao ai?


from cmath import inf
from faulthandler import cancel_dump_traceback_later
from tkinter.tix import INTEGER
from util.guess_manager import GuessManager
from wordle import GuessResult, Result, Wordle
from strategies.base import BaseStrategy
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple


class MaximalInformationStrategy(BaseStrategy):
    # pool of valid words
    valid_word_pool: List[str]
    strategy_guess_manager: GuessManager

    def __init__(self, game: Wordle) -> None:
        super().__init__(game)
        self.valid_word_pool = game.words
        self.strategy_guess_manager = GuessManager(
            self.valid_word_pool, game.word_len)

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

        return best_word

    def make_guess(self, guess: str) -> GuessResult:
        print(self.strategy_guess_manager.remaining_words_tracker)
        guess_result: GuessResult = super().make_guess(guess)
        self.valid_word_pool = self.strategy_guess_manager.update(guess_result)
        return guess_result

    def calculate_information(self, guess):
        est_game = Wordle(self.valid_word_pool, 1, 5, None)
        word_count = len(est_game.words)
        info = 0
        for word in self.valid_word_pool:
            if len(est_game.words) != word_count:
                print("????", word_count)
            if word not in est_game.words:
                print(word)
                print(est_game.words)
            est_game.reset(word)
            guess_manager = GuessManager(
                self.valid_word_pool, self.game.word_len)
            guess_result: GuessResult = est_game.guess(guess)
            info -= len(guess_manager.update(guess_result))

        return info

    # def get_num_net_words(self, result: GuessResult):
    #     new_word_count: int = 0
    #     invalid_chars: List[str] = []
    #     required_chars: List[str] = []
    #     correct_chars: List[tuple(int, str)] = []
    #     guess = result.guess

    #     for i, result in enumerate(result.result):
    #         if result == Result.INVALID:
    #             invalid_chars.append(guess[i])
    #         if result == Result.CORRECT or result == Result.IN_WORD:
    #             required_chars.append(guess[i])
    #         if result == Result.CORRECT:
    #             correct_chars.append((i, guess[i]))

    #     for word in self.valid_word_pool:
    #         is_valid = True
    #         for char in required_chars:
    #             if char not in word:
    #                 is_valid = False

    #         for i, letter in enumerate(word):
    #             if letter in invalid_chars:
    #                 is_valid = False

    #         for i, letter in correct_chars:
    #             if word[i] != letter:
    #                 is_valid = False

    #         if is_valid:
    #             new_word_count += 1

    #     return new_word_count

    # def get_new_word_pool(self, result: GuessResult):
    #     print("Start get new word pool", self.valid_word_pool)
    #     new_word_pool: List[str] = []
    #     invalid_chars: List[str] = []
    #     required_chars: List[str] = []
    #     correct_chars: List[tuple(int, str)] = []
    #     guess = result.guess

    #     for i, result in enumerate(result.result):
    #         if result == Result.INVALID:
    #             invalid_chars.append(guess[i])
    #         if result == Result.CORRECT or result == Result.IN_WORD:
    #             required_chars.append(guess[i])
    #         if result == Result.CORRECT:
    #             correct_chars.append((i, guess[i]))

    #     print(invalid_chars)
    #     print(required_chars)
    #     print(correct_chars)

    #     for word in self.valid_word_pool:
    #         is_valid = True
    #         for char in required_chars:
    #             if char not in word:
    #                 is_valid = False

    #         for i, letter in enumerate(word):
    #             if letter in invalid_chars:
    #                 is_valid = False

    #         for i, letter in correct_chars:
    #             if word[i] != letter:
    #                 is_valid = False

    #         if is_valid:
    #             new_word_pool.append(word)

    #     return new_word_pool
