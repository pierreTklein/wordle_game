from absl import logging
from wordle import Wordle, GuessResult

class BaseStrategy:
    def __init__(self, game: Wordle) -> None:
        self.game = game

    def get_guess(self) -> str:
        """Returns the next guess to try."""
        raise NotImplementedError('Not yet implemented.')

    def make_guess(self, guess: str) -> GuessResult:
        """Makes the guess."""
        result = self.game.guess(guess)
        # Consider overriding this function to store state.
        return result

    def can_guess(self) -> bool:
        """Returns whether we can make another guess in the game."""
        return self.game.can_guess()

    def has_won(self) -> bool:
        """Returns whether solver has completed the game."""
        return self.game.has_won()

    def play_game(self) -> int:
        """Plays out the entire game. 

        Returns the game score."""
        while self.can_guess() and not self.has_won():
            guess_result = self.make_guess(self.get_guess())
            logging.debug(f'{self.game._secret_word} | {guess_result}')
        return self.game.get_score()
