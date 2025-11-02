import socket, time

from . import server
from app.models import ServerGameState, ServerMessage, Error

def run_game():

    # Verificação de parâmetros
    total_players, porta = server.inputs.check()

    print(f"Servidor inicializado na porta {porta}")
    server_socket: socket.socket = None

    # =============== Loop principal do Servidor ===============
    while True:

        # Faz o setup do socket
        server_socket = server.socket_util.setup(
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

        # =============== NEWGAME ===============
        # Anuncia o início do jogo
        ServerMessage.send_message_to_all_players(
            connected_players, 
            ServerMessage.NEWGAME(
                game_state.lives,
                len(game_state.word)
            )
        )

        time.sleep(1)

        # =============== Loop principal do jogo ===============
        current_player_index = 0
        total_common_players = len(game_state.common_players)
        while True:

            # =============== NOT ENOUGH PLAYERS ===============
            # Encerra a partida caso não tenha jogadores comuns o suficiente
            if total_common_players == 0:
                server.game_flow.deal_not_enough_players(game_state.master_player)
                break

            # =============== YOURTURN ===============
            # Notifica o jogador atual que é sua vez
            current_player = game_state.common_players[current_player_index]
            print(f"Vez do jogador {current_player.name}.")
            ServerMessage.send_message_to_player(current_player, ServerMessage.YOURTURN)


            # Aguarda resposta do jogador
            response = ServerMessage.receive_message_from_player(current_player)


            # =============== Conection Loss / QUIT ===============
            if response == None or response == Error.QUIT:
                total_common_players, current_player_index, game_state = server.game_flow.deal_player_left(
                    response, current_player,
                    total_common_players, current_player_index,
                    game_state
                )
                continue


            # =============== GUESS ===============
            elif response.startswith("GUESS "):
                guess_str = server.guess.deal_guess(current_player, game_state, response)


            # =============== ERROR / Unexpected Message ===============
            else:

                if response.startswith("ERROR"):
                    print(f"Mensagem de erro recebida de {current_player.name}: {response}\nEncerrando partida...")
                else:
                    print(f"Mensagem de não esperada recebida de {current_player.name}: {response}\nEncerrando partida...")

                server.game_flow.abort_game(game_state.all_players, Error.UNEXPECTED_MESSAGE)
                break


            # =============== GAMEOVER ===============
            # Verifica se o jogo deve encerrar após lidar com turno do jogador
            is_game_over = server.game_flow.is_game_over(current_player, server_socket, game_state)
            if is_game_over: break


            # =============== STATUS ===============
            # Manda o status do jogo para todos os jogadores
            print(f"Continuando jogo. Estado atual: {''.join(game_state.word_progress)}, vidas restantes: {game_state.lives}")
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
            current_player_index = (current_player_index + 1) % total_common_players
            time.sleep(1)
