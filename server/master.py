import random, socket

from typing import List, Tuple
from ..models import Player

from ..shared.receive_message import receive_message
from .message import send_message_to_all

def master_setup(connected_players: List[Player]) -> Tuple[Player, str]:
    
    master_player = random.choice(connected_players)
    master_socket = master_player.socket

    print(f"Jogador mestre: {master_player.name}")

    try:
        master_socket.sendall("MASTER\r\n".encode('ascii'))
        response = receive_message(master_socket)

        if response and response.startswith("WORD"):
            try:

                chosen_word = response.split(' ', 1)[1].strip()
                if _is_word_valid(chosen_word):
                    master_socket.sendall("OK\r\n".encode('ascii'))
                    print(f"Jogador mestre forneceu a palavra: {chosen_word}")
                    return master_player, chosen_word.upper()
                
                else: raise ValueError("Palavra inválida")

            except (IndexError, ValueError):
                raise ValueError("Mensagem WORD mal-formatada ou palavra inválida")

    except Exception as e:
        
        print(f"Erro CRÍTICO no setup do mestre ({master_player['name']}): {e}")
        send_message_to_all(connected_players, "ERROR INVALID_MASTER_MESSAGE")

        for player in connected_players: 
            try: player.socket.close()
            except: pass
        
        return None, None

def _is_word_valid(word: str) -> bool:
    return (
        not '-' in word   and\
        len(word) > 0     and\
        word.isalpha()
    )
