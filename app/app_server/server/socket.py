import socket

def setup(total_players: int, porta: int, server_socket: socket.socket = None):

    if server_socket: server_socket.close()

    # Criação do objeto socket
    server_socket = socket.socket(
        socket.AF_INET,     # especifica que o endereço será IPv4
        socket.SOCK_STREAM  # especifica que o transporte será TCP
    )

    # Inicia o servidor no endereço especificado
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('0.0.0.0', porta) # O endereço 0.0.0.0 permite que o servidor escute em todas as interfaces
    server_socket.bind(server_address)

    # Abre X conexões, onde X é o número de jogadores
    server_socket.listen(total_players)

    return server_socket