from socket import socket
from app.models import ClientMessage, Error

from . import game_flow

def master_setup(client_socket: socket) -> True:
    """
    Permite o jogador mestre escolhido definir a palavra, lidando com erros.
    """

    print("Voce é o mestre do jogo!")
    while True:

        # Pega palavra do jogador mestre
        word_input = input("Digite a palavra: ")

        # Valida a palavra
        try:
            if not word_input or not word_input.isalpha() or '-' in word_input: raise ValueError
            word_input.encode('ascii')
        except (ValueError, UnicodeEncodeError):
            print("\nPalavra inválida. Use apenas letras, sem acentos e não deixe espaços.\n")
            continue

        # =============== WORD ===============
        # Envia a palavra validada ao servidor
        ClientMessage.send_message_to_server(
            client_socket,
            ClientMessage.WORD(word_input.upper())
        )

        # Aguarda OK do servidor
        response = ClientMessage.receive_message_from_server(client_socket)

        # Palavra do mestre foi escolhida com sucesso
        if response == "OK": return True

        # Erro recuperável - servidor negou a palavra
        if response == Error.INVALID_FORMAT:
            print(f"Servidor não pode lidar com a palavra {word_input.upper()} enviada.\nUse apenas letras, sem acentos e não deixe espaços.\n")
            continue


        # =============== Erros irrecuperáveis ===============
        abort_game_msg:str

        # Perda de conexão
        if response == None: 
            abort_game_msg = "Conexão perdida com o servidor."
        
        # Mensagem de erro do servidor
        elif response.startswith("ERROR "):    
            abort_game_msg = f"Servidor respondeu com uma mensagem de erro:\n{response}"
        
        # Mensagem inesperada
        else:
            abort_game_msg = f"Mensagem inesperada recebida:\n{response}"

        # Encerra o jogo
        game_flow.abort_game(
            client_socket, 1,
            abort_game_msg+"\nEncerrando programa..."
        )
