import socket

from .models import Player, GameState

from .shared import check_inputs
from . import server

# Verificação de parâmetros
numero_jogadores, porta = check_inputs.server()

# Criação do objeto socket
server_socket = socket.socket(
    socket.AF_INET,     # especifica que o endereço será IPv4
    socket.SOCK_STREAM  # especifica que o transporte será TCP
)

# O endereço 0.0.0.0 permite que o servidor escute em todas as interfaces
server_address = ('0.0.0.0', porta)

# Inicia o servidor no endereço especificado
server_socket.bind(server_address)
print(f"Servidor iniciado na porta {porta}")

# Abre X conexões, onde X é o número de jogadores
server_socket.listen(numero_jogadores)

while True:

    print("Iniciando novo jogo...")

    # Aguarda e armazena todos os jogadores
    connected_players = server.players.init(server_socket, numero_jogadores)

    # Define o mestre e a palavra da rodada
    master, word = server.master.master_setup(connected_players)
    
    if not master or not word:
        # TRATAR ERRO DE MASTER_SETUP
        continue

    # Inicia jogo

    game_state = GameState(
        word=word,
        all_players=connected_players,
        master_player=master
    )
    
    server.message.send_message_to_all(connected_players, f"NEWGAME {game_state.lives} {len(game_state.word)}")

    is_game_over = False
    while not is_game_over:
        
        for turn_player in game_state.common_players:

            server.message.send_message(turn_player, "YOURTURN")

            server.guess.deal_guess(turn_player)

            if game_over():
                server.message.send_message_to_all(connected_players, f"GAMEOVER {} {} {game_state.word}")
                is_game_over = True
                break


