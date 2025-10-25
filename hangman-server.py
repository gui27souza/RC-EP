import socket

from .models import Player, GameState
from .models import Message, ServerMessage, ClientMessage

from .shared import check_inputs
from . import server

def run_game():

    # Verificação de parâmetros
    total_players, porta = check_inputs.server()

    # Criação do objeto socket
    server_socket = socket.socket(
        socket.AF_INET,     # especifica que o endereço será IPv4
        socket.SOCK_STREAM  # especifica que o transporte será TCP
    )

    # Inicia o servidor no endereço especificado
    server_address = ('0.0.0.0', porta) # O endereço 0.0.0.0 permite que o servidor escute em todas as interfaces
    server_socket.bind(server_address)
    print(f"Servidor iniciado na porta {porta}")

    # Abre X conexões, onde X é o número de jogadores
    server_socket.listen(total_players)

    while True:

        print("Iniciando novo jogo...")

        # Aguarda e armazena todos os jogadores
        connected_players = server.players.init(server_socket, total_players)

        # Define o mestre e a palavra da rodada
        master, word = server.master.master_setup(connected_players)

        # Reinicia o jogo caso haja algum erro no setup do Mestre
        if not master or not word: continue

        # Inicia jogo
        game_state = GameState(
            word=word,
            all_players=connected_players,
            master_player=master
        )
        
        ServerMessage.send_message_to_all_players(connected_players, f"NEWGAME {game_state.lives} {len(game_state.word)}")

        current_player_index = 0
        total_common_players = len(game_state.common_players)
        while True:
            
            current_player = game_state.common_players[current_player_index]

            ServerMessage.send_message_to_player(current_player, "YOURTURN")
            server.guess.deal_guess(current_player)

            if game_over():
                ServerMessage.send_message_to_all_players(connected_players, ServerMessage.GAMEOVER(x, y, z))
                break

            current_player_index += 1
            if current_player_index == total_common_players: current_player_index = 0