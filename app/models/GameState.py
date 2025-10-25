from dataclasses import dataclass, field

from typing import List
from .Player import Player

@dataclass
class GameState:

    word: str
    '''Palavra a ser advinhada pelos jogadores'''
    all_players: List[Player]
    '''Lista de todos os jogadores conectados'''
    master_player: Player
    '''Jogador Mestre'''
    lives: int = 7
    '''Vidas do jogo. Se chegar em 0, o jogo acaba'''
    guesses: List[str] = []
    '''Lista de palpites realizados pelos jogadores'''

    word_array: List[str] = field(init=False)
    '''Palavra a ser advinhada em forma de vetor'''
    word_progress: List[str] = field(init=False)
    '''Progresso dos palpites até a palavra a ser advinhada. Inicia apenas com "-"'''
    common_players: List[Player] = field(init=False)
    '''Lista de jogadores comuns (Não Mestre)'''


    # Construtor
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