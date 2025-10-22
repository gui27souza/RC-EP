from typing import List
from socket import socket
from ..models import Player

from ..shared.receive_message import receive_message as shared_receive_message

def send_message(socket_end: socket, message: str):
    terminator = "\r\n"
    full_message = (message + terminator).encode('ascii')
    socket_end.sendall(full_message)


def send_message_to_player(player: Player, message: str):
    """Função auxiliar para enviar uma mensagem a um jogador."""
    try: send_message(player.socket, message)
    except:
        print(f"Aviso: Não foi possível enviar mensagem para o jogador {player.name}")

def send_message_to_all_players(players: List[Player], message: str):
    """Função auxiliar para enviar uma mensagem a todos os jogadores."""
    for player in players: send_message_to_player(player, message)

def receive_message(player: Player) -> str:
    """Função auxiliar para receber uma mensagem de um jogador."""
    return shared_receive_message(player.socket)