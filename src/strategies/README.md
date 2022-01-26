# strategies directory

1. `base.py`: The module that contains the base python class that your AI should inherit from.
2. `random.py`: The module that applies the 'random' strategy to solve wordle. It's very bad. I think it has never beaten the game.
3. `similar_words.py`: Guesses the word that shares the most letters with the other words in the bag-of-words. Pretty bad (fails half of the time).