from typing import Optional
from absl import app
from absl import flags


from numpy import average, histogram
from wordle import GameResult, Wordle

##############################################
# (1) Import your strategy here              #
##############################################
from strategies.base import BaseStrategy
from strategies.human import HumanStrategy
from strategies.random import RandomStrategy
from strategies.similar_words import SimilarWordsStrategy


flags.DEFINE_string('words_file', './bag_of_words.txt',
                    'The path to the bag of words.')

flags.DEFINE_integer(
    'num_evals', 50, 'Number of evals to test the AI against.')

##############################################
# (2) Add a flag value for your strat        #
##############################################
flags.DEFINE_enum('strategy', 'similar_words', [
                  'human', 'random', 'similar_words'], 'What type of strategy you want the AI to use.')

flags.DEFINE_string('secret_word', None,
                    'Set this flag to the word that you want to be the secret one.')

FLAGS = flags.FLAGS


def pick_ai(game: Wordle, strategy: str) -> BaseStrategy:
    """Add your strategy in here."""
    if strategy == 'random':
        return RandomStrategy(game)
    elif strategy == 'similar_words':
        return SimilarWordsStrategy(game)
    elif strategy == 'human':
        return HumanStrategy(game)
    ##############################################
    # (3) Construct your strategy here           #
    ##############################################
    else:
        return BaseStrategy(game)


def play_one_round(game: Wordle, strategy: str, secret_word: Optional[str] = None) -> GameResult:
    game.reset()
    if secret_word:
        game.rig_game(secret_word)
    ai = pick_ai(game, strategy)
    result = ai.play_game()
    return GameResult(secret_word=game._secret_word, score=result, guessed_words=game.get_guessed_words())


def ai_evaluator(game: Wordle, num_runs: int, strategy: str, secret_word: Optional[str]) -> None:
    run_score = []
    num_failures = 0
    failed_words = []
    for i in range(0, num_runs):
        game_result = play_one_round(game, strategy, secret_word)
        print(game_result)
        if game_result.score > 0:
            run_score.append(game_result.score)
        else:
            num_failures += 1
            failed_words.append(game._secret_word)
    print('Total rounds:', num_runs)
    print('Num failed rounds:', num_failures, '| Words:', failed_words)
    print('Average win score:', average(run_score) if run_score else -1)
    print('histogram: ', histogram(run_score, bins=game.num_tries_initial,
                                   range=(1, game.num_tries_initial + 1))[0])


def main(argv):
    if len(argv) > 1:
        raise Exception('Too many arguments')
    game = Wordle.from_file(FLAGS.words_file)
    if FLAGS.secret_word:
        game.rig_game(FLAGS.secret_word)
    if FLAGS.strategy == 'human':
        play_one_round(game, 'human', FLAGS.secret_word)
    else:
        ai_evaluator(game, FLAGS.num_evals, FLAGS.strategy, FLAGS.secret_word)


if __name__ == '__main__':
    app.run(main)
