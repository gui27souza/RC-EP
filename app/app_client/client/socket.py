import socket

from . import server_conn

def setup(ip:str, porta:int):

    # Criação do objeto socket
    client_socket = socket.socket(
        socket.AF_INET,     # especifica que o endereço será IPv4
        socket.SOCK_STREAM  # especifica que o transporte será TCP
    )
    
    # Conecta com o servidor pelo socket
    server_conn.connect_to_server(client_socket, ip, porta)

    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    return client_socket
