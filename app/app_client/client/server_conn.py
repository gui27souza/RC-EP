import sys
from socket import socket

def connect_to_server(client_socket: socket, ip: str, porta: str):

    server_address = (ip, porta)
    print(f"Tentando conectar ao servidor em {ip}:{porta}...")
    try:
        client_socket.connect(server_address)
        print("Conexão estabelecida com sucesso!")
    except ConnectionRefusedError:
        print("Conexão recusada: verifique se o servidor está ativo.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado durante a conexão: {e}")
        sys.exit(1)