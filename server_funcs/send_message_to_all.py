import socket

def send_message_to_all(players, message):
    """Função auxiliar para enviar uma mensagem a todos os jogadores."""

    terminator = "\r\n"
    full_message = (message + terminator).encode('ascii')
    
    for player in players:
        try: player['socket'].sendall(full_message)
        except: print(f"Aviso: Não foi possível enviar mensagem para o jogador {player['name']}")
