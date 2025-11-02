import sys
from socket import socket

from app.models import ClientGameState, ClientMessage, Error

def abort_game(client_socket: socket, exit_value: int,  message:str = None):
    
    if message: print(message)
    
    try:client_socket.close()
    except: pass
    
    sys.exit(exit_value)


def wait_game(client_socket:socket, standby_response: str):

    if standby_response.startswith("STANDBY"):
        print("Aguardando o jogo começar...\n")
    else:
        ClientMessage.send_message_to_server(
            client_socket,
            Error.UNEXPECTED_MESSAGE
        )
        abort_game(
            client_socket, 1,
            f"Mensagem inesperada recebida:\n{standby_response}\nEncerrando execução..."
        )

def start_game(client_socket: socket, is_master:bool, newgame_response:str):

    response_parts = newgame_response.split(' ')
            
    try:
        lives = int(response_parts[1])
        word_length = int(response_parts[2])
    
        game_state = ClientGameState(
            lives, word_length, is_master
        )

        print(f"Jogo iniciado!\nVidas para advinhar: {game_state.lives}\nTamanho da palavra: {game_state.word_length} letras.")

        return game_state

    except (ValueError, IndexError):
        ClientMessage.send_message_to_server(client_socket, Error.INVALID_FORMAT)
        abort_game(
            client_socket, 1,
            f"Mensagem de NEWGAME mal formatada: {newgame_response}"
        )
    
    except Exception as e:
        abort_game(
            client_socket, 1,
            f"Erro inesperado ao iniciar novo jogo: {e}"
        )

def end_game(client_socket: socket, gameover_message: str):
    
    try:
        message_parts = gameover_message.split()
        
        result = message_parts[1]
        if result not in ["WIN", "LOSE"]: raise ValueError

        player_name = message_parts[2]
        
        word = message_parts[3]

    except (ValueError, IndexError):
        ClientMessage.send_message_to_server(
            client_socket,Error.INVALID_FORMAT
        )
        abort_game(client_socket, 1, f"Mensagem de GAMEOVER mal formatada:\n{gameover_message}\n")

    except Exception as e:
        abort_game(
            client_socket, 1,
            f"Erro inesperado ao lida com mensagem de GAMEOVER: {e}\n"
        )

    print("O jogo terminou.")
    if result == "WIN":
        print(f"A palavra '{word}' foi adivinhada por {player_name}")
    elif result == "LOSE":
        print(f"O jogador {player_name} errou o último palpite para a palavra '{word}'!")

    abort_game(
        client_socket, 0,
        "Encerrando conexão com o servidor..."
    )