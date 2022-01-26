import re

from functools import reduce
from typing import Dict, List, Tuple


class Probabilities:
    def __init__(self, words: List[str], word_len: int = 5) -> None:
        self.words = words
        self.word_len = word_len
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                        'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.letter_freqs: Dict[int, Dict[str, int]] = {}
        for i in range(0, word_len):
            self.letter_freqs[i] = {}
            for l in self.letters:
                self.letter_freqs[i][l] = self.letter_freq(l, i)

    def letter_freq(self, letter: str, pos: int) -> int:
        """Returns number of occurences that a letter appears in a given position."""
        # Count the number of times a letter appears at a given position in a word
        letter_counts = map(lambda w: 1 if w[pos] == letter else 0, self.words)
        return reduce(lambda x, y: x+y, letter_counts)

    def p_letter(self, letter: str, pos: int) -> float:
        """Returns probability that a letter is in a given position."""
        return self.letter_freqs[pos][letter] * 1. / len(self.words)

    def word_freq(self, mask: str) -> int:
        """Returns count of words that matches string mask."""
        regex = re.compile(mask)
        match_counts = map(lambda w: 1 if regex.fullmatch(w)
                           else 0, self.words)
        return reduce(lambda x, y: x+y, match_counts)

    def p_word(self, mask: str) -> float:
        """Returns the probability that a word in the BoW matches the string mask."""
        return self.word_freq(mask) * 1. / len(self.words)

    def shared_letters(self, word: str) -> int:
        sl = 0
        for i, c in enumerate(word):
            sl += self.letter_freqs[i][c]
        return sl

    def highest_shared_letters(self) -> List[Tuple[str, int]]:
        """Returns an ordered list of words and it's shared-letter count.
        
        The shared-letter count is essentiallywith how many letters it shares
        with other words in the bag-of-words.
         """
        shared_letters = list(
            map(lambda x: (x, self.shared_letters(x)), self.words))
        return sorted(shared_letters, key=lambda x: x[1], reverse=True)
