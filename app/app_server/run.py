import socket

from app.models import ServerGameState, ServerMessage

from . import server

def run_game():

    # Verificação de parâmetros
    total_players, porta = server.inputs.check()

    # Criação do objeto socket
    server_socket = socket.socket(
        socket.AF_INET,     # especifica que o endereço será IPv4
        socket.SOCK_STREAM  # especifica que o transporte será TCP
    )

    # Inicia o servidor no endereço especificado
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('0.0.0.0', porta) # O endereço 0.0.0.0 permite que o servidor escute em todas as interfaces
    server_socket.bind(server_address)
    print(f"Servidor inicializadodo na porta {porta}")

    # Abre X conexões, onde X é o número de jogadores
    server_socket.listen(total_players)

    # Aguarda e armazena todos os jogadores
    connected_players = server.players.init(server_socket, total_players)

    # Loop principal do Servidor
    while True:
        print("Iniciando novo jogo...")

        # Define o mestre e a palavra da rodada
        master, word = server.master.master_setup(connected_players)

        # Reinicia o jogo caso haja algum erro no setup do Mestre
        if not master or not word: 
            print("Reiniciando jogo devido a problemas no setup do jogador Mestre...")
            continue

        print("Jogo iniciado com sucesso!")

        # Inicia jogo
        game_state = ServerGameState(
            word=word,
            all_players=connected_players,
            master_player=master
        )
        # Anuncia o início do jogo
        ServerMessage.send_message_to_all_players(
            connected_players, 
            ServerMessage.NEWGAME(
                game_state.lives,
                len(game_state.word)
            )
        )

        # Loop principal do jogo
        current_player_index = 0
        total_common_players = len(game_state.common_players)
        while True:
            current_player = game_state.common_players[current_player_index]
            print(f"Vez do jogador {current_player.name}.")

            # Recebe e processa palpite
            ServerMessage.send_message_to_player(current_player, ServerMessage.YOURTURN)
            guess_str = server.guess.deal_guess(current_player, game_state)

            # Verifica se o jogo deve encerrar
            game_over_status = server.game_flow.is_game_over(game_state)
            if game_over_status:
                
                if game_over_status == "LOSE":
                    print("Jogadores perderam!")
                elif game_over_status == "WIN":
                    print(f"Jogador {current_player.name} advinhou a palavra!")
                
                print("Finalizando jogo...")
                ServerMessage.send_message_to_all_players(
                    connected_players, 
                    ServerMessage.GAMEOVER(
                        game_over_status, current_player.name, game_state.word
                    )
                )
                
                break

            print(f"Continuando jogo. Estado atual: {''.join(game_state.word_progress)}, vidas restantes: {game_state.lives}")
            
            # Manda o status do jogo para todos os jogadores
            ServerMessage.send_message_to_all_players(
                game_state.all_players, 
                ServerMessage.STATUS(
                    game_state.lives,
                    ''.join(game_state.word_progress),
                    current_player.name,
                    guess_str if guess_str else 'palpite-invalido'
                )
            )

            # Atualiza o player atual
            current_player_index += 1
            if current_player_index == total_common_players: 
                current_player_index = 0
