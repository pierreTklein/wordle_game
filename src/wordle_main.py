from absl import app
from absl import flags

from typing import List

from numpy import histogram
from wordle import Wordle
from wordle_solver_base import WordleSolverBase

flags.DEFINE_string('words_file', './bag_of_words.txt',
                    'The path to the bag of words.')
flags.DEFINE_integer(
    'num_evals', 50, 'Number of evals to test the AI against.')

FLAGS = flags.FLAGS


def ai_evaluator(game: Wordle, num_runs: int) -> List[int]:
    run_score = []
    for i in range(0, num_runs):
        game.reset()
        solver = WordleSolverBase(game)
        result = solver.play_game()
        print('Run result:', result, game.get_guess_words(), game._secret_word)
        run_score.append(result)
    return histogram(run_score, bins=6, range=(0, game.num_tries_initial + 1))


def main(argv):
    if len(argv) > 1:
        raise Exception('Too many arguments')
    game = Wordle.from_file(FLAGS.words_file)
    print(ai_evaluator(game, FLAGS.num_evals))


if __name__ == '__main__':
    app.run(main)
