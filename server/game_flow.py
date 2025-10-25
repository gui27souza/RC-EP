from typing import List
from ..models import Player, ServerMessage, GameState

def abort_game(players: List[Player], error_code:str):
    """Envia a mensagem de erro crítico para todos e fecha os sockets."""
    ServerMessage.send_message_to_all_players(players, error_code)
    for player in players: 
        try: player.socket.close()
        except: 
            print(f"Não foi possível encerrar conexão de forma segura com o jogador {player.name} ({player.socket}).")

def is_game_over(game_state: GameState) -> str:
    """Verifica se o jogo deve seguir após cada rodada"""
    
    if game_state.lives == 0:
        #### PERDEU
        return "LOSE"

    if not '_' in game_state.word_progress:
        #### GANHOU
        return "WIN"
    
    return None
