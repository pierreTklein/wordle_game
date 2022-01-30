from wordle import Result, Wordle, GuessResult
from strategies.base import BaseStrategy
from util.probabilities import alphabet


class HumanStrategy(BaseStrategy):
    def __init__(self, game: Wordle) -> None:
        self.letters = set(alphabet())
        super().__init__(game)

    def get_guess(self) -> str:
        guess = ''
        print('Available letters:', ','.join(sorted(list(self.letters))))
        while True:
            guess = input(
                f'[{len(self.game.guesses)+1}/{self.game.num_tries_initial}] Enter guess:')
            if self.game.is_valid_guess(guess):
                break
            print('Invalid word, please try again.')
        return guess

    def make_guess(self, guess: str) -> GuessResult:
        guess_result = super().make_guess(guess)
        guess, result = guess_result
        pretty_result = ''
        for i, r in enumerate(result):
            if r == Result.INVALID and guess[i] in self.letters:
                self.letters.remove(guess[i])
            pretty_result += f'{guess[i]}: {r.name} | '
        print(pretty_result)
        if not self.game.has_won() and not self.game.can_guess():
            print('You ran out of moves. The secret was:', self.game._secret_word)
