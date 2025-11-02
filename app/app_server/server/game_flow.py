from typing import List
from app.models import Player, ServerMessage, ServerGameState, Error

def abort_game(players: List[Player], error_code:str):
    """Envia a mensagem de erro crítico para todos e fecha os sockets."""
    ServerMessage.send_message_to_all_players(players, error_code)
    for player in players: 
        try: player.socket.close()
        except: 
            print(f"Não foi possível encerrar conexão de forma segura com o jogador {player.name} ({player.socket}).")

def is_game_over(game_state: ServerGameState) -> str:
    """Verifica se o jogo deve seguir após cada rodada"""
    
    # Jogo acabou - Player perdeu
    if game_state.lives == 0:
        return "LOSE"

    # Jogo acabou - Player ganhou
    if not '_' in game_state.word_progress:
        return "WIN"
    
    # Jogo segue
    return None
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
