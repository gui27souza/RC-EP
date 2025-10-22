class Error:
    '''Classe para centralização de erros.'''

    INVALID_FORMAT = "ERROR INVALID_FORMAT"
    '''mensagem de erro enviada sempre que houver erro de formatação da mensagem recebida'''

    # done
    INVALID_MASTER_MESSAGE = "ERROR INVALID_MASTER_MESSAGE"
    '''mensagem enviada para todos os jogadores caso o jogador mestre não envie uma palavra válida (não respondeu com mensagem WORD, ou a palavra estava ausente, ou a palavra contém caracteres inválidos'''

    UNEXPECTED_MESSAGE = "ERROR UNEXPECTED_MESSAGE"
    '''mensagem de erro enviada sempre que a mensagem recebida não for uma mensagem de erro, mas não for um dos tipos de mensagem esperada pelo protocolo naquele ponto de execução.'''

    # done
    INVALID_PLAYER_NAME = "ERROR INVALID_PLAYER_NAME"
    '''mensagem de erro enviada pelo servidor ao cliente se o  nome fornecido pela mensagem NEWPLAYER for inválido. O nome é considerado inválido se estiver vazio, se contiver espaços, ou se contiver caracteres não alfanuméricos.'''

    NOT_ENOUGH_PLAYERS = "ERROR NOT_ENOUGH_PLAYERS"
    '''Mensagem de erro enviada pelo servidor ao jogador mestre caso não haja jogadores comuns restantes para continuar o jogo.'''

    ALREADY_GUESSED = "ERROR ALREADY_GUESSED"
    '''Mensagem de erro enviada pelo servidor se a mensagem GUESS do cliente contiver um palpite já enviado anteriormente (por qualquer jogador). A conexão com entre cliente e servidor não é encerrada.'''

    INVALID_LETTER = "ERROR INVALID_LETTER"
    '''Mensagem de erro enviada pelo servidor se a mensagem GUESS LETTER do cliente contiver um caractere inválido. A conexão com entre cliente e servidor não é encerrada.'''

    INVALID_WORD_LENGTH = "ERROR INVALID_WORD_LENGTH"
    '''Mensagem de erro enviada pelo servidor se a mensagem GUESS WORD do cliente contiver uma palavra tamanho diferente da palavra a ser adivinhada. A conexão com entre cliente e servidor não é encerrada.'''

    QUIT = "QUIT"
    '''Esta mensagem não é exatamente um erro, mas pode ser enviada pelo cliente ao servidor para indicar que o jogador deseja se desconectar. O servidor deve responder com OK e encerrar a conexão.'''
    