from socket import socket
from typing import List
from ..models import Player

from ..models import Error
from . import message

def init(server_socket: socket, numero_jogadores: int) -> List[Player]:
    '''
    Busca o número de jogadores especificado, retornando uma lista de dicionários, onde cada um tem o socket, nome e endereço do cliente
    '''

    connected_players = []

    i = 1

    while i<=numero_jogadores:

        print(f"Aguardando jogador {i}")

        # Aceita a conexão TCP
        client_socket, client_address = server_socket.accept()

        # Recebe NEWPLAYER <nome>
        initial_message = message.receive_message(client_socket)

        if initial_message and initial_message.startswith("NEWPLAYER "):
            
            # Recorta apenas o nome do jogador da mensagem
            player_name = initial_message.split(' ', 1)[1]

            if not player_name or ' ' in player_name or not player_name.isalnum():
                message.send_message(client_socket, Error.INVALID_PLAYER_NAME})
                client_socket.close()
                print(f"Erro: Jogador de {client_address} enviou nome inválido ('{player_name}'). Conexão encerrada.")
                continue


            connected_players.append(Player(
                socket=client_socket,
                name=player_name,
                address=client_address
            ))

            # Envia resposta de STANDBY ao cliente
            standby_msg = "STANDBY\r\n"
            client_socket.sendall(standby_msg.encode('ascii'))
            
            # Player se conectou com sucesso
            i+=1
            print(f"Jogador conectado: {player_name}")

        else:
            # LIDAR COM MENSAGEM INICIAL INVÁLIDA
            pass

    print(f"Todos os {numero_jogadores} jogadores conectados. Preparando o jogo.")
    return connected_players