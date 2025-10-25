'''
Módulo que lida com operações do fluxo de jogo relacionada a configuração de Players
'''

from socket import socket
from typing import List
from ..models import Player

from ..models import Error
from ..models import Message, ServerMessage

def init(server_socket: socket, numero_jogadores: int) -> List[Player]:
    '''
    Busca o número de jogadores especificado, retornando uma lista de dicionários, onde cada um tem o socket, nome e endereço do cliente
    '''

    connected_players: List[Player] = []

    i = 1
    while i<=numero_jogadores:

        print(f"Aguardando jogador {i}")

        # Aceita a conexão TCP
        client_socket, client_address = server_socket.accept()

        # Recebe NEWPLAYER <nome>
        initial_message = Message.receive_message(client_socket)

        if initial_message and initial_message.startswith("NEWPLAYER "):
            
            # Recorta apenas o nome do jogador da mensagem
            player_name = initial_message.split(' ', 1)[1].strip()


            if not player_name or ' ' in player_name or not player_name.isalnum():
                ServerMessage.send_message(client_socket, Error.INVALID_PLAYER_NAME)
                client_socket.close()
                print(f"Erro: Jogador de {client_address} enviou nome inválido ('{player_name}'). Conexão encerrada.")
                continue

            # Cria e guarda um novo objeto Player
            new_player = Player(
                socket=client_socket,
                name=player_name,
                address=client_address
            )
            connected_players.append(new_player)

            # Avisa o Player que está tudo ok e pede para aguardar o início do jogo
            ServerMessage.send_message_to_player(new_player, ServerMessage.STANDBY)
            
            # Player se conectou com sucesso
            i+=1
            print(f"Jogador conectado: {new_player.name} ({new_player.address})")

        # Lida com mensagem inicial completamente inválida
        else:
            ServerMessage.send_message(client_socket, Error.UNEXPECTED_MESSAGE)
            client_socket.close()
            print(f"Erro: Jogador de {client_address} enviou mensagem inicial inesperada ('{initial_message}'). Conexão encerrada.")
            continue

    print(f"Todos os {numero_jogadores} jogadores conectados.\nLista de jogadores: {[player.name for player in connected_players]} Preparando o jogo.")
    return connected_players