from ...models import Player, GameState

from .. import message

from .validate_guess import validate_guess
from .process_guess import process_guess


def deal_guess(turn_player: Player, game_state: GameState):

    guess = message.receive_message(turn_player)
    guess_type, guess_str, is_invalid = validate_guess(guess)    

    if not is_invalid: message.send_message(turn_player, "OK")

    process_guess(guess_type, guess_str, game_state)

