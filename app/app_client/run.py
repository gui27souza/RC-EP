import socket

from . import client
from app.models import ClientMessage, ClientGameState, Error

def run_game():

    # Verificação de parâmetros
    nome_jogador, ip, porta = client.inputs.check()

    print("Conectando ao servidor...")
    client_socket = client.socket.setup(ip, porta)

    # Envia mensagem de anuncio de novo player, com o nome do jogador
    ClientMessage.send_message_to_server(client_socket, ClientMessage.NEWPLAYER(nome_jogador))

    response = ClientMessage.receive_message_from_server(client_socket)
    if response.startswith("STANDBY"):
        print("Aguardando o jogo começar...")

    game_state: ClientGameState
    is_master = False
    while True:
        
        response = ClientMessage.receive_message_from_server(client_socket)

        if response == None:
            client.game_flow.abort_game(
                client_socket, 1,
                "Conexão com o servidor encerrada de forma inesperada.\nEncerrando execução..."
            )

        ### ERROR
        elif response.startswith("ERROR"):
            
            if response == Error.NOT_ENOUGH_PLAYERS:
                client.game_flow.abort_game(
                    client_socket, 1,
                    "Partida finalizada por falta de jogadores.\nEncerrando programa...",
                    1
                )

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

                print(f"Jogo iniciado!\nVidas para advinhar: {game_state.lives}\nTamanho da palavra: {game_state.word_length} letras.")

            except (ValueError, IndexError):
                print(f"Mensagem de NEWGAME mal formatada: {response}")

        ### YOURTURN
        elif response.startswith("YOURTURN"):
            client.turn.handle_yourturn(client_socket)

        ### STATUS
        elif response.startswith("STATUS "):
            game_state = client.status.update(game_state, response)

        ### GAMEOVER
        elif response.startswith("GAMEOVER"):
            client.game_flow.end_game(client_socket, response)

        ### MENSAGEM INESPERADA
        else:
            ClientMessage.send_message_to_server(
                client_socket, Error.UNEXPECTED_MESSAGE
            )
            client.game_flow.abort_game(
                client_socket, 1,
                f"Mensagem de erro inesperado recebida:\n{response}\nEncerrando execução..."
            )
