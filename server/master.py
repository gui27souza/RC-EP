import random

from typing import List, Tuple
from ..models import Player, Error, ServerMessage

from . import game_flow

def master_setup(connected_players: List[Player]) -> Tuple[Player, str]:
    
    # Escolhe um player aleatório para ser o Mestre
    master_player = random.choice(connected_players)
    print(f"Jogador mestre: {master_player.name}")

    # Avisa o player que ele é o Mestre
    try:
        ServerMessage.send_message_to_player(master_player, ServerMessage.MASTER)
    except Exception:
        game_flow.abort_game(connected_players, Error.INVALID_MASTER_MESSAGE)
        return None, None
    
    # Loop que aguarda uma palavra válida do Mestre
    while True:

        try:
            # Recebe a mensagem
            response = ServerMessage.receive_message_from_player(master_player)

            # Perda de conexão com o Mestre - Sem resposta
            if response is None: 
                game_flow.abort_game(connected_players, Error.INVALID_MASTER_MESSAGE)
                return None, None

            # Erro de mensagem
            if not response.startswith("WORD"): 
                raise ValueError

            # Valida a palavra
            chosen_word = response.split(' ', 1)[1].strip()
            if not (not '-' in chosen_word and len(chosen_word) > 0 and chosen_word.isalpha()): 
                raise ValueError

            ServerMessage.send_message_to_player(master_player, ServerMessage.OK)
            print(f"Jogador mestre forneceu a palavra: {chosen_word}")
            return master_player, chosen_word.upper()

        # Erro recuperável
        except ValueError:
            ServerMessage.send_message_to_player(master_player, Error.INVALID_FORMAT)
            ServerMessage.send_message_to_all_players(connected_players, Error.INVALID_MASTER_MESSAGE)
            continue
        
        # Erro irrecuperável
        except Exception:
            game_flow.abort_game(connected_players, Error.INVALID_MASTER_MESSAGE)
            return None, None

