import socket

import funcs.check_funcs as check
import server_funcs

# Verificação de parâmetros
numero_jogadores, porta = check.check_server_execution_parameters()

# Criação do objeto socket
server_socket = socket.socket(
    socket.AF_INET,     # especifica que o endereço será IPv4
    socket.SOCK_STREAM  # especifica que o transporte será TCP
)

# O endereço 0.0.0.0 permite que o servidor escute em todas as interfaces
server_address = ('0.0.0.0', porta)

# Inicia o servidor no endereço especificado
server_socket.bind(server_address)
print(f"Servidor iniciado na porta {porta}")

# Abre X conexões, onde X é o número de jogadores
server_socket.listen(numero_jogadores)

while True:

    print("Iniciando novo jogo...")

    # Aguarda e armazena todos os jogadores
    connected_players = server_funcs.init_players(server_socket, numero_jogadores)

    # Define o mestre e a palavra da rodada
    master, word = server_funcs.master_setup(connected_players)
    
    if not master or not word:
        # TRATAR ERRO DE MASTER_SETUP
        pass

    # Inicia jogo

    word_array = []
    empty_array = []
    for letter in word:
        word_array.append(letter)
        empty_array.append('_')

    game_state = {
        'word': word_array,
        'empty_word': empty_array,
        'lives': 7,
        'guesses': []
    }
    