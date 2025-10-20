from dataclasses import dataclass, field

from typing import List
from .Player import Player

@dataclass
class GameState:

    word: str
    all_players: List[Player]
    master_player: Player

    lives: int = 7
    guesses: List[str] = []

    word_array: List[str] = field(init=False)
    word_progress: List[str] = field(init=False)
    common_players: List[Player] = field(init=False)

    def __post_init__(self):
        
        word_array = []
        empty_word_array = []

        for letter in self.word:
            word_array.append(letter.upper())
            empty_word_array.append('_')
        common_players = [player for player in self.all_players if player != self.master_player]

        self.word_array = word_array
        self.word_progress = empty_word_array
        self.common_players = common_players