import socket

from . import client
from app.models import ClientMessage, ServerGameState

def run_game():

    nome_jogador, ip, porta = client.inputs.check()

    # Criação do objeto socket
    client_socket = socket.socket(
        socket.AF_INET,     # especifica que o endereço será IPv4
        socket.SOCK_STREAM  # especifica que o transporte será TCP
    )

    # Conecta com o servidor pelo socket
    client.server_conn.connect_to_server(client_socket, ip, porta)

    # Envia mensagem de anuncio de novo player, com o nome do jogador
    ClientMessage.send_message_to_server(client_socket, ClientMessage.NEWPLAYER(nome_jogador))

    while True:
        
        response = ClientMessage.receive_message_from_server(client_socket)

        ### ERROR
        if response.startswith("ERROR"):

            pass

        ### STANDBY
        elif response.startswith("STANDBY"):
            
            pass

        ### MASTER ###
        elif response.startswith("MASTER"):
            
            pass

        ### NEWGAME
        elif response.startswith("NEWGAME"):
            
            pass

        ### YOURTURN
        elif response.startswith("YOURTURN"):

            pass

        ### STATUS
        elif response.startswith("STATUS"):

            pass

        ### GAMEOVER
        elif response.startswith("GAMEOVER"):

            pass

        ### MENSAGEM INESPERADA
        else:

            pass
