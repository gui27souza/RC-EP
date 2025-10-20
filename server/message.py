from typing import List
from ..models import Player

from ..shared.receive_message import receive_message as shared_receive_message

def send_message(player: Player, message: str):
    """Função auxiliar para enviar uma mensagem a um jogador."""

    terminator = "\r\n"
    full_message = (message + terminator).encode('ascii')

    try: player.socket.sendall(full_message)
    except: print(f"Aviso: Não foi possível enviar mensagem para o jogador {player.name}")

def send_message_to_all(players: List[Player], message: str):
    """Função auxiliar para enviar uma mensagem a todos os jogadores."""

    terminator = "\r\n"
    full_message = (message + terminator).encode('ascii')
    
    for player in players:
        try: player.socket.sendall(full_message)
        except: print(f"Aviso: Não foi possível enviar mensagem para o jogador {player.name}")

def receive_message(player: Player) -> str:
    """Função auxiliar para receber uma mensagem de um jogador."""
    return shared_receive_message(player.socket)