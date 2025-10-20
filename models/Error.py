from dataclasses import dataclass, field

@dataclass
class Error:

    INVALID_FORMAT

    INVALID_MASTER_MESSAGE

    UNEXPECTED_MESSAGE

    INVALID_PLAYER_NAME

    NOT_ENOUGH_PLAYERS

    ALREADY_GUESSED

    INVALID_LETTER

    INVALID_WORD_LENGTH

    QUIT
    