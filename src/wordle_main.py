from absl import app
from absl import flags


from numpy import average, histogram
from wordle import Result, Wordle
from strategies.similar_words import SimilarWordsStrategy
from strategies.base import BaseStrategy
from strategies.random import RandomStrategy
##############################################
# (1) Import your strategy here              #
##############################################


flags.DEFINE_string('words_file', './bag_of_words.txt',
                    'The path to the bag of words.')

flags.DEFINE_integer(
    'num_evals', 50, 'Number of evals to test the AI against.')

flags.DEFINE_enum('play_type', 'ai', ['ai', 'human'], 'Whether you want to play yourself, or you want the AI to play.')

##############################################
# (2) Add a flag value for your strat        #
##############################################
flags.DEFINE_enum('strategy', 'similar_words', ['random', 'similar_words'], 'What type of strategy you want the AI to use.')

flags.DEFINE_string('secret_word_override', None, 'Set this flag to the word that you want to be the secret one.')

FLAGS = flags.FLAGS

def pick_ai(game: Wordle, strategy: str) -> BaseStrategy:
    """Add your strategy in here."""
    if strategy == 'random':
        return RandomStrategy(game)
    elif strategy == 'similar_words':
        return SimilarWordsStrategy(game)
    ##############################################
    # (3) Construct your strategy here           #
    ##############################################
    else:
        return BaseStrategy(game)


def ai_evaluator(game: Wordle, num_runs: int, strategy: str) -> None:
    run_score = []
    num_failures = 0
    for i in range(0, num_runs):
        game.reset()
        ai = pick_ai(game, strategy)
        result = ai.play_game()
        print('Run result:', result, '| Guessed:', game.get_guessed_words(), '| Secret:', game._secret_word)
        if result > 0:
            run_score.append(result)
        else:
            num_failures += 1
    print('Total rounds:', num_runs)
    print('Num failed rounds:', num_failures)
    print('Average win score:', average(run_score) if run_score else -1)
    print('histogram: ', histogram(run_score, bins=5, range=(1, game.num_tries_initial + 1))[0])

def human_game(game: Wordle):
    letters = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
    while game.can_guess() and not game.has_won():
        guess = ''
        print('Available letters:', ','.join(sorted(list(letters))))
        guess = input(f'[{len(game.guesses)+1}/{game.num_tries_initial}] Enter guess:')
        if not game.is_valid_guess(guess):
            print('Invalid word, please try again.')
            continue
        guess, result = game.guess(guess)
        pretty_result = ''
        for i,r in enumerate(result):
            if r == Result.INVALID and guess[i] in letters:
                letters.remove(guess[i])
            pretty_result += f'{guess[i]}: {r.name} | '
        print(pretty_result)
    print(game.get_score())
    if not game.has_won():
        print('You ran out of moves. The secret was:', game._secret_word)

def main(argv):
    if len(argv) > 1:
        raise Exception('Too many arguments')
    game = Wordle.from_file(FLAGS.words_file)
    if FLAGS.secret_word_override:
        game.rig_game(FLAGS.secret_word_override)
    if FLAGS.play_type == 'ai':
        ai_evaluator(game, FLAGS.num_evals, FLAGS.strategy)
    else:
        human_game(game)



if __name__ == '__main__':
    app.run(main)
