import socket

from . import client
from app.models import ClientMessage, ClientGameState

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

    response = ClientMessage.receive_message_from_server(client_socket)
    if response.startswith("STANDBY"):
        print("Aguardando início do jogo...")

    game_state: ClientGameState
    is_master = False
    while True:
        
        response = ClientMessage.receive_message_from_server(client_socket)

        ### ERROR
        if response.startswith("ERROR"):

            pass

        ### MASTER
        elif response.startswith("MASTER"):
            is_master_setup = client.master.master_setup(client_socket)

            if not is_master_setup: 
                pass

            is_master = True


        ### NEWGAME
        elif response.startswith("NEWGAME "):
            
            response_parts = response.split(' ')
            
            try:
                lives = int(response_parts[1])
                word_length = int(response_parts[2])
            
                game_state = ClientGameState(
                    lives, word_length, is_master
                )
            except (ValueError, IndexError):
                print(f"Mensagem de NEWGAME mal formatada: {response}")


        ### YOURTURN
        elif response.startswith("YOURTURN"):

            client.turn.handle_yourturn(client_socket)

        ### STATUS
        elif response.startswith("STATUS"):

            pass

        ### GAMEOVER
        elif response.startswith("GAMEOVER"):

            pass

        ### MENSAGEM INESPERADA
        else:

            pass
