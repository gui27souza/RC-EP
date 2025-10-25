from typing import List
from ..models import Player, ServerMessage

def abort_game(players: List[Player], error_code:str):
    """Envia a mensagem de erro crítico para todos e fecha os sockets."""
    ServerMessage.send_message_to_all_players(players, error_code)
    for player in players: 
        try: player.socket.close()
        except: 
            print(f"Não foi possível encerrar conexão de forma segura com o jogador {player.name} ({player.socket}).")