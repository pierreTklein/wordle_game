from absl import app
from absl import flags

from typing import List, Tuple

from numpy import array, histogram
from wordle import Wordle
from wordle_solver_random import WordleSolverRandom

flags.DEFINE_string('words_file', './bag_of_words.txt',
                    'The path to the bag of words.')

flags.DEFINE_integer(
    'num_evals', 50, 'Number of evals to test the AI against.')

flags.DEFINE_enum('play_type', 'ai', ['ai', 'human'], 'Whether you want to play yourself, or you want the AI to play.')

flags.DEFINE_string('secret_word_override', None, 'Set this flag to the word that you want to be the secret one.')

FLAGS = flags.FLAGS


def ai_evaluator(game: Wordle, num_runs: int) -> Tuple[array, array]:
    run_score = []
    for i in range(0, num_runs):
        game.reset()
        solver = WordleSolverRandom(game)
        result = solver.play_game()
        print('Run result:', result, '| Guessed:', game.get_guessed_words(), '| Secret:', game._secret_word)
        run_score.append(result)
    return histogram(run_score, bins=6, range=(0, game.num_tries_initial + 1))

def human_game(game: Wordle):
    while game.can_guess() and not game.has_won():
        guess = ''
        guess = input('Enter guess:')
        if not game.is_valid_guess(guess):
            print('Invalid word, please try again.')
            continue
        guess, result = game.guess(guess)
        pretty_result = ''
        for i,r in enumerate(result):
            pretty_result += f'{guess[i]}: {r.name} | '
        print(pretty_result)

def main(argv):
    if len(argv) > 1:
        raise Exception('Too many arguments')
    game = Wordle.from_file(FLAGS.words_file)
    if FLAGS.secret_word_override:
        game.rig_game(FLAGS.secret_word_override)
    if FLAGS.play_type == 'ai':
        print(ai_evaluator(game, FLAGS.num_evals))
    else:
        human_game(game)



if __name__ == '__main__':
    app.run(main)
