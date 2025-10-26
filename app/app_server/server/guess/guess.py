from app.models import Player, GameState, ServerMessage

from .validate_guess import validate_guess
from .process_guess import process_guess


def deal_guess(turn_player: Player, game_state: GameState) -> str:

    guess = ServerMessage.receive_message_from_player(turn_player)
    guess_type, guess_str, guess_error = validate_guess(guess, game_state)
    
    if guess_error: 
        ServerMessage.send_message_to_player(turn_player, guess_error)
        return guess_str
    
    if guess_type == "WORD": guess_type_msg = "palavra"
    if guess_type == "LETTER": guess_type_msg = "letra"

    print(f"Processando palpite de {guess_type_msg}: '{guess_str}'")
    process_guess(guess_type, guess_str, game_state)
    ServerMessage.send_message_to_player(turn_player, "OK")
    return guess_str
