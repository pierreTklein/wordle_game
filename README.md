# Wordle Game

This is a python implementation of wordle, which uses the same set of available words as the hit game, Wordle.

## Play the game manually

```bash
python src/wordle_main.py
```

## Implement an algorithm to solve it

So you want to write an algorithm that can solve Wordle in as few turns as possible?

1. Create a new class that inherits from `WordleSolverBase`.
2. Change the implementation of the `get_guess()` function, as well as the `make_guess()` function.
3. Update `wordle_main` to import the new `WordleSolver` class that you created.
4. Run it: `python src/wordle_main.py`