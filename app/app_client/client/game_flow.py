import sys
from socket import socket
def end_game(socket: socket, gameover_message: str):
    message_parts = gameover_message.split()
    result = message_parts[1]
    player_name = message_parts[2]
    word = message_parts[3]

    print("O jogo terminou.")
    
    if result == "WIN":
        print(f"A palavra '{word}' foi adivinhada por {player_name}")
    elif result == "LOSE":
        print(f"O jogador {player_name} errou o último palpite para a palavra '{word}'!")
    else:
        print("Mensagem de gameover mal formatada.")

    print("Encerrando conexão com o servidor...")

    socket.close()

    sys.exit(0)