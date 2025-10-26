from socket import socket

from . import client

def run_game():

    nome_jogador, ip, porta = client.inputs.check()

    # Criação do objeto socket
    client_socket = socket(
        socket.AF_INET,     # especifica que o endereço será IPv4
        socket.SOCK_STREAM  # especifica que o transporte será TCP
    )

    client.server_conn.connect_to_server(client_socket, ip, porta)

