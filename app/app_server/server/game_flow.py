import time
from socket import socket

from typing import List
from app.models import Player, ServerMessage, ServerGameState, Error

def abort_game(players: List[Player], error_code:str):
    """Envia a mensagem de erro crítico para todos e fecha os sockets."""
    ServerMessage.send_message_to_all_players(players, error_code)
    for player in players: 
        try: player.socket.close()
        except: 
            print(f"Não foi possível encerrar conexão de forma segura com o jogador {player.name} ({player.socket}).")

def is_game_over(current_player:Player, server_socket: socket,game_state: ServerGameState) -> bool:
    """Verifica se o jogo deve seguir após cada rodada"""

    # Jogo acabou - Player perdeu
    if game_state.lives == 0:
        end_game(
            "LOSE", current_player,
            server_socket, game_state
        )
        return True

    # Jogo acabou - Player ganhou
    if not '_' in game_state.word_progress:
        end_game(
            "WIN", current_player,
            server_socket, game_state
        )
        return True

    # Jogo segue
    return False

def end_game(game_over_status:str, current_player:Player, server_socket: socket, game_state:ServerGameState):

    if game_over_status == "LOSE":
        print("Jogadores perderam!")
    elif game_over_status == "WIN":
        print(f"Jogador {current_player.name} advinhou a palavra!")

    print("Finalizando jogo...")
    ServerMessage.send_message_to_all_players(
        game_state.all_players, 
        ServerMessage.GAMEOVER(
            game_over_status, current_player.name, game_state.word
        )
    )

    time.sleep(1)

    for player in game_state.all_players:
        try: player.socket.close()
        except: pass

    server_socket.close()

def deal_not_enough_players(master_player: Player):

    print("Não há mais jogadores comuns.\nFim de jogo.")

    # =============== NOT ENOUGH PLAYERS ===============
    try:
        ServerMessage.send_message_to_player(
            master_player,
            Error.NOT_ENOUGH_PLAYERS
        )
    except: pass

    time.sleep(1)

def deal_player_left(response: str, current_player: Player, total_common_players: int, current_player_index: int, game_state: ServerGameState):

    if response == Error.QUIT:
        ServerMessage.send_message_to_player(
            current_player, ServerMessage.OK
        )

    game_state.common_players.remove(current_player)
    total_common_players = len(game_state.common_players)

    if total_common_players > 0:
        current_player_index -= 1

    return total_common_players, current_player_index, game_state
