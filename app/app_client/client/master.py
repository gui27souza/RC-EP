from socket import socket
from app.models import ClientGameState, ClientMessage

def master_setup(client_socket: socket) -> bool:

    print("Voce é o mestre do jogo!")

    while True:
        
        word_input = input("Digite a palavra: ")

        if not word_input or not word_input.isalpha() or '-' in word_input:
            print("\nPalavra inválida. Use apenas letras, sem acentos e não deixe espaços.\n")
            continue

        try:
            word_input.encode('ascii')
        except UnicodeEncodeError:
            print("\nPalavra inválida. Use apenas letras, sem acentos e não deixe espaços.\n")
            continue

        ClientMessage.send_message(
            client_socket,
            ClientMessage.WORD(word_input.upper())
        )

        response = ClientMessage.receive_message_from_server(client_socket)

        if response.startswith("OK"): 
            return True
        elif response.startswith("ERROR"):
            error_code = response.split(' ', 1)[1]
            print(f"\nERRO do Servidor: {error_code}. Por favor, tente novamente.\n")
        else:
            print(f"ERRO FATAL: Resposta inesperada do servidor: {response}")
            return False
