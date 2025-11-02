from socket import socket
from typing import NoReturn

from app.models import ClientMessage, ClientGameState, Error
from . import game_flow

def handle_yourturn(client_socket: socket, game_state: ClientGameState):
    """
    Lida com vez do jogador de dar o palpite de letra ou palavra, lidando com erros.
    """

    while True:

        # Recebe o palpite do usuário
        guess_input = input("Digite sua jogada (letra ou palavra), ou \q para sair: ")

        # Saída do jogo
        if guess_input == "\q":
            _game_quit(client_socket)

        # Validação inicial do palpite
        elif (
            not guess_input.isalpha() or
            ' ' in guess_input
        ):
            print("Palpite inválido!")
            continue

        # Definição do tipo do palpite
        guess_type: str
        if len(guess_input) == 1: guess_type = "LETTER"
        else: guess_type = "WORD"

        # =============== GUESS ===============
        # Envio do palpite ao servidor
        ClientMessage.send_message_to_server(
            client_socket,
            ClientMessage.GUESS(
                guess_type, guess_input.upper()
            )
        )

        # Aguarda a resposta do servidor sobre o palpite
        response = ClientMessage.receive_message_from_server(client_socket)

        # Sucesso
        if response == "OK": 
            return

        # Erros recuperáveis - Não encerram execução, porém jogador perde a vez
        if response == Error.INVALID_FORMAT or response == Error.INVALID_LETTER:
            print(f"Servidor não pode lidar com o palpite {guess_input}\nPerdeu a vez.")
            return
        elif response == Error.INVALID_WORD_LENGTH:
            print(f"Palpite de palavra com tamanho diferente da palavra a ser advinhada.\nPalpite -> {len(guess_input)} letras\nPalavra -> {game_state.word_length} letras\nPerdeu a vez.")
            return
        elif response == Error.ALREADY_GUESSED:
            print(f"Palpite '{guess_input}' já foi tentado!\nPerdeu a vez.")
            return

        # =============== Erros irrecuperáveis ===============
        abort_game_msg:str

        if response == None:
            abort_game_msg = "Conexão com o servidor encerrada de forma inesperada.\nEncerrando execução..."
        elif response.startswith("ERROR "):
            abort_game_msg = f"Servidor respondeu com uma mensagem de erro:\n{response}"
        else:
            abort_game_msg = f"Mensagem inesperada recebida:\n{response}"

        game_flow.abort_game(
            client_socket, 1,
            abort_game_msg
        )


def _game_quit(client_socket: socket) -> NoReturn:
    """
    Tenta sair do jogo de forma segura, se possível, ou não.
    """

    # Solicita saída do jogo
    ClientMessage.send_message_to_server(
        client_socket, Error.QUIT
    )

    # Aguarda o retorno do servidor
    response = ClientMessage.receive_message_from_server(client_socket)

    # Perda de conexão com o servidor ao tentar sair
    if response == None:
        game_flow.abort_game(
            client_socket, 1,
            "Conexão com servidor encerrada, porém sem resposta."
        )

    # Saída segura do jogo
    elif response == "OK":
        game_flow.abort_game(
            client_socket, 0,
            "Conexão com servidor de forma segura."
        )
