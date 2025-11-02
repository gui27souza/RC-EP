from . import client
from app.models import ClientMessage, ClientGameState, Error

def run_game():

    # Verificação de parâmetros
    nome_jogador, ip, porta = client.inputs.check()

    # Cria e conecta o socket com o servidor
    print("Conectando ao servidor...")
    client_socket = client.server_conn.setup(ip, porta)

    # Envia mensagem de anuncio de novo player, com o nome do jogador
    ClientMessage.send_message_to_server(client_socket, ClientMessage.NEWPLAYER(nome_jogador))

    response = ClientMessage.receive_message_from_server(client_socket)
    client.game_flow.wait_game(client_socket, response)

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
                )

            else:
                client.game_flow.abort_game(
                    client_socket, 1,
                    f"Mensagem de erro inesperado recebida:\n{response}\nEncerrando execução..."
                )

        ### MASTER

        elif response.startswith("MASTER"):
            is_master = client.master.master_setup(client_socket)


        ### NEWGAME
        elif response.startswith("NEWGAME "):
            game_state = client.game_flow.start_game(client_socket, is_master, response)

        ### YOURTURN
        elif response.startswith("YOURTURN"):
            client.turn.handle_yourturn(client_socket, game_state)

        ### STATUS
        elif response.startswith("STATUS "):
            game_state = client.status.update(client_socket, game_state, response)


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
