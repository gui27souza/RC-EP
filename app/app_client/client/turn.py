from socket import socket

from app.models import ClientMessage, Error
from . import game_flow

def handle_yourturn(client_socket: socket):
    
    while True:
    
        guess_input = input("Digite sua jogada (letra ou palavra), ou \q para sair: ")

        if guess_input == "\q":
            _game_quit(client_socket)

        elif (
            not guess_input.isalpha() or
            ' ' in guess_input
        ):
            print("Palpite inválido!")
            continue

        guess_type: str
        if len(guess_input) == 1: guess_type = "LETTER"
        else: guess_type = "WORD"

        ClientMessage.send_message_to_server(
            client_socket,
            ClientMessage.GUESS(
                guess_type, guess_input.upper()
            )
        )

        response = ClientMessage.receive_message_from_server(client_socket)

        if response == None:
            game_flow.abort_game(
                client_socket,
                "Conexão com o servidor encerrada de forma inesperada.\nEncerrando execução...",
                1
            )

        elif response == "OK": 
            break

        #### LIDAR COM RESPOSTA DO SERVER

def _game_quit(client_socket: socket):

    ClientMessage.send_message_to_server(
        client_socket, Error.QUIT
    )

    response = ClientMessage.receive_message_from_server(client_socket)

    if response == None:
        game_flow.abort_game(
            client_socket,
            "Conexão com servidor encerrada, porém sem resposta.",
            1
        )
    elif response == "OK":
        game_flow.abort_game(
            client_socket,
            "Conexão com servidor de forma segura.",
            0
        )