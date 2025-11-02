from socket import socket
from app.models import ClientGameState, ClientMessage, Error

from . import game_flow

def update(client_socket: socket, game_state: ClientGameState, status_message: str):

    # STATUS <vidas> <estado> <jogador> <palpite>
    status_parts = status_message.split(' ')

    # Valida a mensagem
    try:

        if len(status_parts) < 5:
            raise ValueError

        status = status_parts[0]
        lives = int(status_parts[1])
        word_progress_str = status_parts[2]
        last_player = status_parts[3]
        last_guess = status_parts[4]

        if lives < 0 or lives > 7:
            raise ValueError

    except (ValueError, IndexError, TypeError) as e:
        ClientMessage.send_message_to_server(
            client_socket, Error.INVALID_FORMAT
        )
        game_flow.abort_game(
            client_socket, 1,
            f"Mensagem de STATUS mal formatada:\n{status_message}"
        )
    except Exception as e:
        game_flow.abort_game(
            client_socket, 1,
            f"Falha ao lida com mensagem de STATUS:\n{status_message}\n{e}"
        )

    # Aloca os dados para o objeto de controle de jogo
    game_state.lives = lives
    game_state.word_progress = list(word_progress_str)
    if (
        last_guess not in game_state.word_progress and
        last_guess != ''.join(game_state.word_progress) and
        last_guess != "palpite-invalido" and
        last_guess not in game_state.guesses
    ):
        game_state.guesses.append(last_guess)

    # Faz os prints necessários para o jogador
    print(f"jogador {last_player} fez uma jogada: {last_guess}. Restam {lives} vidas.")
    print(
        _forca_by_lives(int(lives), word_progress_str)
    )
    print(f"Palpites errados: {' '.join(game_state.guesses)}")

    return game_state



def _forca_by_lives(lives: int, word_progress: str):

    if lives == 7:
        return """
        _____
        |   |
        |   
        |   
        |   
        |
        ------
        """ + word_progress + "\n"

    elif lives == 6:
        return """
        _____
        |   |
        |   o
        |   
        |   
        |
        ------
        """ + word_progress + "\n"

    elif lives == 5:
        return """

        _____
        |   |
        |   o
        |   l
        |   
        |
        ------
        """ + word_progress + "\n"

    elif lives == 4:
        return """
        _____
        |   |
        |   o
        | --l
        |   
        |
        ------
        """ + word_progress + "\n"

    elif lives == 3:
        return """
        _____
        |   |
        |   o
        | --l--
        |   
        |
        ------
        """ + word_progress + "\n"

    elif lives == 2:
        return """
        _____
        |   |
        |   o
        | --l--
        |  / 
        |
        ------
        """ + word_progress + "\n"

    elif lives == 1 or lives == 0:
        return """
        _____
        |   |
        |   o
        | --l--
        |  / \\
        |
        ------
        """ + word_progress + "\n"

    else:
        return "Valor de vidas inválido.\n"
