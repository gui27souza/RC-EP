from dataclasses import dataclass, field

from typing import List

@dataclass
class GameState:

    word: str
    word_array: List[str]
    word_progress: List[str]
    lives: 7
    guesses: List[str]
