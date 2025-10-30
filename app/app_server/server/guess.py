from typing import Tuple
from app.models import Player, ServerGameState, ServerMessage, Error

def deal_guess(turn_player: Player, game_state: ServerGameState) -> str:

    guess = ServerMessage.receive_message_from_player(turn_player)
    guess_type, guess_str, guess_error = _validate_guess(guess, game_state)
    
    if guess_error: 
        ServerMessage.send_message_to_player(turn_player, guess_error)
        return guess_str
    
    if guess_type == "WORD": guess_type_msg = "palavra"
    if guess_type == "LETTER": guess_type_msg = "letra"

    print(f"Processando palpite de {guess_type_msg}: '{guess_str}'")
    _process_guess(guess_type, guess_str, game_state)
    ServerMessage.send_message_to_player(turn_player, "OK")
    return guess_str


# --------------- Funções Auxiliares ---------------


def _validate_guess(guess: str, game_state: ServerGameState) -> Tuple[str, str, str|None]:
    """
    Valida o palpite, retornando o tipo do palpite (LETTER ou WORD), o palpite em upper, e o erro se for o caso.
    """

    if guess.startswith("GUESS "):
        guess = guess[6:]

        if guess.startswith("LETTER "):
            guess = guess[7:].strip().upper()
            guess_type = "LETTER"

            validated_guess, guess_error = _validate_guess_letter(guess, game_state)
        
        elif guess.startswith("WORD "):
            guess = guess[5:].strip().upper()
            guess_type = "WORD"
            
            validated_guess, guess_error = _validate_guess_word(guess, game_state)

        else: return None, None, Error.INVALID_FORMAT

        return guess_type, validated_guess, guess_error 
    
    return None, None, Error.UNEXPECTED_MESSAGE

def _validate_guess_letter(guess: str, game_state: ServerGameState) -> Tuple[str, str|None]:
    """
    Valida palpilte de palavra. 
    Retorna o palpite e o erro caso não seja válido
    """

    if len(guess) != 1 or not guess.isalpha():
        return guess, Error.INVALID_LETTER
    
    if guess in game_state.guesses: return guess, Error.ALREADY_GUESSED
        
    return guess, None

def _validate_guess_word(guess: str, game_state: ServerGameState) -> Tuple[str, str|None]:
    """
    Valida palpilte de palavra. 
    Retorna o palpite e o erro caso não seja válido
    """
    
    if not guess.isalpha() or len(guess.split(' ')) != 1: return guess, Error.INVALID_FORMAT

    if len(guess) != len(game_state.word): return guess, Error.INVALID_WORD_LENGTH

    if guess in game_state.guesses: return guess, Error.ALREADY_GUESSED

    return guess, None



def _process_guess(guess_type: str, guess: str, game_state: ServerGameState):
    
    if guess_type == "LETTER":
        if guess in game_state.word_array:
            for i in range(0, len(game_state.word_array)):
                if guess == game_state.word_array[i]:
                    game_state.word_progress[i] = guess
        else:
            game_state.lives -= 1
        

    if guess_type == "WORD":
        if guess == game_state.word:
            for i in range(0, len(game_state.word_array)):
                game_state.word_progress[i] = guess[i]
        else:
            game_state.lives -= 1