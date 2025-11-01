import socket

from app.models import ServerGameState, ServerMessage

from . import server

def run_game():

    # Verificação de parâmetros
    total_players, porta = server.inputs.check()

    print(f"Servidor inicializado na porta {porta}")
    server_socket: socket.socket = None

    # Loop principal do Servidor
    while True:

        server_socket = server.socket.setup(
            total_players, 
            porta,
            server_socket if server_socket else None
        )

        print("Iniciando novo jogo...")

        # Aguarda e armazena todos os jogadores
        connected_players = server.players.init(server_socket, total_players)


        # Define o mestre e a palavra da rodada
        master, word = server.master.master_setup(connected_players)

        # Reinicia o jogo caso haja algum erro no setup do Mestre
        if not master or not word: 
            print("Reiniciando jogo devido a problemas no setup do jogador Mestre...")
            continue

        # Inicia jogo
        print("Jogo iniciado com sucesso!")
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

            response = ServerMessage.receive_message_from_player(current_player)

            if response == None or response == Error.QUIT:
            elif response.startswith("GUESS "):
                guess_str = server.guess.deal_guess(current_player, game_state, response)

            elif response.startswith("ERROR "):
                
                break

            else:
                ServerMessage.send_message_to_player(
                    current_player, Error.UNEXPECTED_MESSAGE
                )
                break

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
