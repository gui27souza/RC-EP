from typing import Tuple
from ...models import GameState, Error

def validate_guess(guess: str, game_state: GameState) -> Tuple[str, str, str|None]:
    """
    Valida o palpite, retornando o tipo do palpite (LETTER ou WORD), o palpite em upper, e o erro se for o caso.
    """

    if guess.startswith("GUESS "):
        guess = guess[6:]

        if guess.startswith("LETTER "):
            guess = guess[7:].strip().upper()
            guess_type = "LETTER"

            validated_guess, guess_error = _validate_guess_letter(guess)
        
        elif guess.startswith("WORD "):
            guess = guess[5:].strip().upper()
            guess_type = "WORD"
            
            validated_guess, guess_error = _validate_guess_word(guess, game_state)

        else: return None, None, Error.INVALID_FORMAT

        return guess_type, validated_guess, guess_error 
    
    return None, None, Error.UNEXPECTED_MESSAGE


def _validate_guess_letter(guess: str, game_state: GameState) -> Tuple[str, str|None]:
    """
    Valida palpilte de palavra. 
    Retorna o palpite e o erro caso não seja válido
    """

    if len(guess) != 1 or not guess.isalpha():
        return guess, Error.INVALID_LETTER
    
    if guess in game_state.guesses: return guess, Error.ALREADY_GUESSED
        
    return guess, None
    

def _validate_guess_word(guess: str, game_state: GameState) -> Tuple[str, str|None]:
    """
    Valida palpilte de palavra. 
    Retorna o palpite e o erro caso não seja válido
    """
    
    if not guess.isalpha() or len(guess.split(' ')) != 1: return guess, Error.INVALID_FORMAT

    if len(guess) != len(game_state.word): return guess, Error.INVALID_WORD_LENGTH

    if guess in game_state.guesses: return guess, Error.ALREADY_GUESSED

    return guess, None
