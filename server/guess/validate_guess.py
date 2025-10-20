from typing import Tuple

def validate_guess(guess: str) -> Tuple[str, str, str|None]:

    if guess.startswith("GUESS "):
        guess = guess[6:]

        if guess.startswith("LETTER "):
            guess = guess[7:].strip()
            guess_type = "LETTER"

            is_valid, validated_guess = _validate_guess_letter(guess)
            if not is_valid: return guess_type, None, "INVALID LETTER"
        
        elif guess.startswith("WORD "):
            guess = guess[5:].strip()
            guess_type = "WORD"
            
            is_valid, validated_guess = _validate_guess_word(guess)
            if not is_valid: return guess_type, None, "INVALID WORD"

        else: return None, None, "INVALID GUESS TYPE: MUST BE LETTER OR WORD"

        return guess_type, validated_guess, None

    else: return None, None, "INVALID FORMAT FOR GUESS: MUST BE GUESS [LETTER|WORD] <guess_str>"

def _validate_guess_letter(guess: str) -> Tuple[bool, str]:
    if (
        len(guess) == 1 and
        guess.isalpha()
    ): return True, guess.upper()
    else: return False, None

def _validate_guess_word(guess: str) -> Tuple[bool, str]:
    if (
        len(guess) > 0 and
        guess.isalpha() and
        len(guess.split(' ')) == 1
    ): return True, guess.upper()
    else: return False, None
