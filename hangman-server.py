from socket import *
import sys
import random
import threading
import time
import funcs.check_funcs as check

# Constantes do protocolo e do jogo
LIVES = 7
HOST = '0.0.0.0'
DEFAULT_PORT = 6891

# Acessa os parâmetros de linha de comando usando a função que você criou
numero_jogadores, porta = check.check_server_execution_parameters()

def envia_mensagem(conn, mensagem):
    """Envia uma mensagem para o cliente, garantindo o terminador de linha."""
    try:
        conn.sendall(f"{mensagem}\r\n".encode('ascii'))
    except error as e:
        print(f"Erro ao enviar mensagem: {e}")

def recebe_mensagem(conn):
    """Recebe uma mensagem completa do cliente, lendo até o terminador de linha."""
    buffer = b''
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                return None  # Conexão fechada
            buffer += data
            if buffer.endswith(b'\r\n'):
                return buffer.decode('ascii').strip()
        except error as e:
            print(f"Erro ao receber mensagem: {e}")
            return None

def handle_client_connection(conn, addr, trava_estado_jogo, dado_estado_jogo):
    """Gerencia a comunicação com um cliente."""
    try:
        novo_player_msg = recebe_mensagem(conn)
        if not novo_player_msg or not novo_player_msg.startswith("NEWPLAYER "):
            envia_mensagem(conn, "ERROR INVALID_FORMAT")
            return
            
        player_name = novo_player_msg.split(" ", 1)[1]
        if not player_name or ' ' in player_name or not player_name.isalnum():
            envia_mensagem(conn, "ERROR INVALID_PLAYER_NAME")
            return

        with trava_estado_jogo:
            dado_estado_jogo['players'].append({'name': player_name, 'conn': conn})
            dado_estado_jogo['players_conectados'] += 1
        
        print(f"Jogador conectado: {player_name}")
        envia_mensagem(conn, "STANDBY")

        # Espera todos os jogadores se conectarem
        while True:
            with trava_estado_jogo:
                if dado_estado_jogo['players_conectados'] >= numero_jogadores:
                    break
            time.sleep(1)

        eh_mestre = False
        with trava_estado_jogo:
            if not dado_estado_jogo['mestre_escolhido']:
                dado_estado_jogo['mestre'] = random.choice(dado_estado_jogo['players'])['name']
                dado_estado_jogo['mestre_escolhido'] = True
            eh_mestre = (dado_estado_jogo['mestre'] == player_name)

        if eh_mestre:
            print(f"Jogador mestre: {player_name}")
            envia_mensagem(conn, "MASTER")
            
            palavra_msg = recebe_mensagem(conn)
            if not palavra_msg or not palavra_msg.startswith("WORD "):
                envia_mensagem(conn, "ERROR INVALID_MASTER_MESSAGE")
                return

            palavra = palavra_msg.split(" ", 1)[1].lower()
            if not palavra.isalpha() or '-' in palavra:
                envia_mensagem(conn, "ERROR INVALID_MASTER_MESSAGE")
                return
            
            with trava_estado_jogo:
                dado_estado_jogo['palavra_para_acertar'] = palavra
                dado_estado_jogo['palavra_recebida'] = True
            
            envia_mensagem(conn, "OK")
            print(f"Jogador mestre forneceu a palavra: {palavra}")

        # Espera a palavra ser recebida
        while True:
            with trava_estado_jogo:
                if dado_estado_jogo['palavra_recebida']:
                    break
            time.sleep(1)
        palavra_len = len(dado_estado_jogo['palavra_para_acertar'])
        envia_mensagem(conn, f"NEWGAME {LIVES} {palavra_len}")
        print("Jogo iniciado com sucesso!")

        while not dado_estado_jogo['fim_do_jogo']:
            with trava_estado_jogo:
                jogadores_comuns = [p for p in dado_estado_jogo['players'] if p['name'] != dado_estado_jogo['mestre']]
                eh_minha_vez = (jogadores_comuns[dado_estado_jogo['index_turno_atual']]['conn'] == conn)

            if eh_minha_vez:
                envia_mensagem(conn, "YOURTURN")
                palpite_msg = recebe_mensagem(conn)
                if palpite_msg == "QUIT":
                    envia_mensagem(conn, "OK")
                    return
                with trava_estado_jogo:
                    parte_palpite = palpite_msg.split(" ", 2)
                    if len(parte_palpite) < 3 or parte_palpite[0] != "GUESS":
                        envia_mensagem(conn, "ERROR INVALID_FORMAT")
                        continue
                    tipo_palpite = parte_palpite[1]
                    palpite = parte_palpite[2].lower()

                    if tipo_palpite == "WORD":
                        if len(palpite) != len(dado_estado_jogo['palavra_para_acertar']):
                            envia_mensagem(conn, "ERROR INVALID_WORD_LENGTH")
                            continue
                        if palpite == dado_estado_jogo['palavra_para_acertar']:
                            dado_estado_jogo['fim_do_jogo'] = True
                            dado_estado_jogo['resultado'] = 'WIN'
                            dado_estado_jogo['nome_vencedor'] = player_name
                        else:
                            dado_estado_jogo['vidas_restantes'] -= 1

                    elif tipo_palpite == "LETTER":
                        if len(palpite) != 1 or not palpite.isalpha():
                            envia_mensagem(conn, "ERROR INVALID_LETTER")
                            continue
                        if palpite in dado_estado_jogo['letras_palpitadas']:
                            envia_mensagem(conn, "ERROR ALREADY_GUESSED")
                            continue
                        dado_estado_jogo['letras_palpitadas'].add(palpite)
                        if palpite not in dado_estado_jogo['palavra_para_acertar']:
                            dado_estado_jogo['vidas_restantes'] -= 1

                    envia_mensagem(conn, "OK")

            if not dado_estado_jogo['fim_do_jogo']:
                estado = ''
                for letra in dado_estado_jogo['palavra_para_acertar']:
                    estado += letra if letra in dado_estado_jogo['letras_palpitadas'] else '_'

            if estado == dado_estado_jogo['palavra_para_acertar']:
                dado_estado_jogo['fim_do_jogo'] = True
                dado_estado_jogo['resultado'] = 'WIN'
                dado_estado_jogo['nome_vencedor'] = player_name

            if dado_estado_jogo['vidas_restantes'] <= 0:
                dado_estado_jogo['fim_do_jogo'] = True
                dado_estado_jogo['resultado'] = 'LOSE'

            status_msg = f"STATUS {dado_estado_jogo['vidas_restantes']} {estado} {player_name} {palpite}"
            for player in dado_estado_jogo['players']:
                envia_mensagem(player['conn'], status_msg)

            dado_estado_jogo['index_turno_atual'] = (dado_estado_jogo['index_turno_atual'] + 1) % len(jogadores_comuns)
            time.sleep(1)

        with trava_estado_jogo:
            gameover_msg = f"GAMEOVER {dado_estado_jogo['resultado']} {dado_estado_jogo['nome_vencedor']} {dado_estado_jogo['palavra_para_acertar']}"
            for jogador in dado_estado_jogo['players']:
                envia_mensagem(jogador['conn'], gameover_msg)

    except Exception as e:
        print(f"Erro inesperado na conexão com {addr}: {e}")
    finally:
        conn.close()

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((HOST, porta))
    serverSocket.listen(numero_jogadores)
    print(f"Servidor TCP pronto para receber na porta {porta}")

    while True:
        print("Iniciando novo jogo...")

        trava_estado_jogo = threading.Lock()
        dado_estado_jogo = {
            'players': [],
            'players_conectados': 0,
            'mestre': None,
            'mestre_escolhido': False,
            'palavra_para_acertar': '',
            'palavra_recebida': False,
            'letras_palpitadas': set(),
            'letras_corretas': set(),
            'vidas_restantes': LIVES,
            'index_turno_atual': 0,
            'fim_do_jogo': False,
            'nome_vencedor': None,
            'resultado': 'LOSE'
        }

        threads = []
        for _ in range(numero_jogadores):
            print("Aguardando nova conexão...")
            connectionSocket, clientAddress = serverSocket.accept()
            print("Conexão estabelecida com", clientAddress)
            thread = threading.Thread(target=handle_client_connection, args=(connectionSocket, clientAddress, trava_estado_jogo, dado_estado_jogo))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        print("Finalizando jogo....")

if __name__ == "__main__":
    main()
