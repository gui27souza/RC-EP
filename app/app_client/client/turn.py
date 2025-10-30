from socket import socket

from app.models import ClientMessage

def handle_yourturn(client_socket: socket):
    
    while True:
    
        guess_input = input("Digite sua jogada (letra ou palavra), ou \q para sair: ")

        if (
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
        if response == "OK": break

        #### LIDAR COM RESPOSTA DO SERVER
