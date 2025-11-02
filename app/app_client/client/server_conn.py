import sys
import socket

def setup(ip:str, porta:int):

    # Criação do objeto socket
    client_socket = socket.socket(
        socket.AF_INET,     # especifica que o endereço será IPv4
        socket.SOCK_STREAM  # especifica que o transporte será TCP
    )
    
    # Conecta com o servidor pelo socket
    server_address = (ip, porta)
    try:
        client_socket.connect(server_address)
        print("Conexão estabelecida com sucesso!\n")
    except ConnectionRefusedError:
        print("Conexão recusada: verifique se o servidor está ativo.\n")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado durante a conexão: {e}\n")
        sys.exit(1)

    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    return client_socket
