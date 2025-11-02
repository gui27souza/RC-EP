from typing import Tuple
from app.models import Player, ServerGameState, ServerMessage, Error

from app.debug import print_debug

def deal_guess(turn_player: Player, game_state: ServerGameState, guess_response: str) -> str:
    """
    Lida com palpite do jogador. Também lida com erros e informa ao cliente.
    """

    # Valida o palpite, retornando o tipo, o palpite validado e, caso ocorra, o tipo do erro
    guess_type, guess_str, guess_error = _validate_guess(guess_response, game_state)

    # Informa ao jogador caso algum erro ocorra
    if guess_error:

        print_debug(f"Palpite inválido de {turn_player.name}: {guess_type} {guess_str}\n{guess_error}")

        ServerMessage.send_message_to_player(turn_player, guess_error)

        if guess_error == Error.ALREADY_GUESSED: 
            return guess_str
        else:
            return None


    # Logs informativos
    if guess_type == "WORD": guess_type_msg = "palavra"
    if guess_type == "LETTER": guess_type_msg = "letra"
    print(f"Processando palpite de {guess_type_msg}: '{guess_str}'")

    # Processa o palpite
    _process_guess(guess_type, guess_str, game_state)

    # Avisa o jogador de que tudo ocorreu como esperado
    ServerMessage.send_message_to_player(turn_player, "OK")

    return guess_str



# =============== Funções Auxiliares ===============

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

    if len(guess) != 1:
        return guess, Error.INVALID_FORMAT
    
    if not guess.isalpha():
        return guess, Error.INVALID_LETTER

    if (
        guess in game_state.guesses or
        guess in game_state.word_progress
    ):
        return guess, Error.ALREADY_GUESSED

    return guess, None

def _validate_guess_word(guess: str, game_state: ServerGameState) -> Tuple[str, str|None]:
    """
    Valida palpilte de palavra. 
    Retorna o palpite e o erro caso não seja válido
    """

    if not guess.isalpha() or len(guess.split(' ')) != 1: 
        return guess, Error.INVALID_FORMAT

    if len(guess) != len(game_state.word): 
        return guess, Error.INVALID_WORD_LENGTH

    if guess in game_state.guesses: 
        return guess, Error.ALREADY_GUESSED

    return guess, None



def _process_guess(guess_type: str, guess: str, game_state: ServerGameState):
    """
    Processa o palpite, verificando se acertou ou errou, fazendo as devidas atualizações
    """

    if guess_type == "LETTER":

        # Palpite correto
        if guess in game_state.word_array:
            for i in range(0, len(game_state.word_array)):
                if guess == game_state.word_array[i]:
                    game_state.word_progress[i] = guess
            print_debug("Letra estava na palavra!")

        # Palpite incorreto
        else:
            game_state.lives -= 1
            game_state.guesses.append(guess)
            print_debug("Letra não estava na palavra!")


    if guess_type == "WORD":

        # Palpite correto
        if guess == game_state.word:
            for i in range(0, len(game_state.word_array)):
                game_state.word_progress[i] = guess[i]
            print_debug("Palavra acertada!")

        # Palpite incorreto
        else:
            game_state.lives -= 1
            game_state.guesses.append(guess)
            print_debug("Palavra não acertada!")
