from app.models import ClientGameState

def update(game_state: ClientGameState, status_message: str):

    # STATUS <vidas> <estado> <jogador> <palpite>
    status_parts = status_message.split(' ')
    status = status_parts[0]
    lives = status_parts[1]
    word_progress = status_parts[2]
    last_player = status_parts[3]
    last_guess = status_parts[4]
    game_state.lives = lives
    game_state.word_progress = word_progress.split()

    print(f"jogador {last_player} fez uma jogada: {last_guess}. Restam {lives} vidas.\n")
    print(
        _forca_by_lives(int(lives), word_progress)
    )

    return game_state



def _forca_by_lives(lives: int, word_progress: str):

    if lives == 7:
        return """
        _____
        |   |
        |   
        |   
        |   
        |
        ------
        """ + word_progress

    elif lives == 6:
        return """
        _____
        |   |
        |   o
        |   
        |   
        |
        ------
        """ + word_progress

    elif lives == 5:
        return """

        _____
        |   |
        |   o
        |   l
        |   
        |
        ------
        """ + word_progress

    elif lives == 4:
        return """
        _____
        |   |
        |   o
        | --l
        |   
        |
        ------
        """ + word_progress

    elif lives == 3:
        return """
        _____
        |   |
        |   o
        | --l--
        |   
        |
        ------
        """ + word_progress

    elif lives == 2:
        return """
        _____
        |   |
        |   o
        | --l--
        |  / 
        |
        ------
        """ + word_progress

    elif lives == 1 or lives == 0:
        return """
        _____
        |   |
        |   o
        | --l--
        |  / \\
        |
        ------
        """ + word_progress

    else:
        return "Valor de vidas inválido"