from socket import *
import funcs.check_funcs as check

def envia_mensagem(sock, mensagem):
    """Envia mensagem ASCII terminada com CRLF."""
    try:
        sock.sendall(f"{mensagem}\r\n".encode('ascii'))
    except error as e:
        print(f"Erro ao enviar mensagem: {e}")

def recebe_mensagem(sock):
    """Recebe mensagem completa até CRLF."""
    buffer = b''
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                return None
            buffer += data
            if buffer.endswith(b'\r\n'):
                return buffer.decode('ascii').strip()
        except error as e:
            print(f"Erro ao receber mensagem: {e}")
            return None

def main():
    nome_jogador, ip, porta = check.check_client_execution_parameters()
    clientSocket = socket(AF_INET, SOCK_STREAM)
    print("Conectando ao servidor...")
    clientSocket.connect((ip, porta))
    print("Aguardando o jogo começar...")
    envia_mensagem(clientSocket, f"NEWPLAYER {nome_jogador}")
    letras_erradas = []
    palavras_erradas = []
    while True:
        msg = recebe_mensagem(clientSocket)
        if not msg:
            print("Conexão encerrada pelo servidor.")
            break
        partes = msg.split()
        comando = partes[0]
        if comando == "STANDBY":
            pass
        elif comando == "MASTER":
            print("Você é o mestre do jogo!")
            palavra = input("Digite a palavra: ").strip()
            envia_mensagem(clientSocket, f"WORD {palavra}")
        elif comando == "OK":
            pass
        elif comando == "NEWGAME":
            vidas = partes[1]
            tamanho = partes[2]
            print(f"\nJogo iniciado!")
            print(f"Vidas para adivinhar: {vidas}")
            print(f"Tamanho da palavra: {tamanho} letras.\n")
        elif comando == "YOURTURN":
            jogada = input("Digite sua jogada (letra ou palavra), ou \\q para sair: ").strip()
            if jogada == "\\q":
                envia_mensagem(clientSocket, "QUIT")
                print("Encerrando conexão com o servidor...")
                clientSocket.close()
                break
            if len(jogada) == 1:
                envia_mensagem(clientSocket, f"GUESS LETTER {jogada}")
            else:
                envia_mensagem(clientSocket, f"GUESS WORD {jogada}")
        elif comando == "STATUS":
            vidas = partes[1]
            estado = partes[2]
            jogador = partes[3]
            palpite = partes[4]
            if palpite not in estado:
                if len(palpite) == 1 and palpite not in letras_erradas:
                    letras_erradas.append(palpite)
                elif len(palpite) > 1 and palpite not in palavras_erradas:
                    palavras_erradas.append(palpite)
            print(f"\nJogador {jogador} fez uma jogada: {palpite}. Restam {vidas} vidas.")
            print("Estado atual:", estado)
            print("Letras erradas:", ", ".join(letras_erradas) if letras_erradas else "nenhuma")
            print("Palavras erradas:", ", ".join(palavras_erradas) if palavras_erradas else "nenhuma")
        elif comando == "GAMEOVER":
            resultado = partes[1]
            jogador = partes[2]
            palavra = partes[3]
            print("\nO jogo terminou.")
            if resultado == "WIN":
                print(f"A palavra '{palavra}' foi adivinhada por {jogador}!")
            else:
                print(f"A palavra '{palavra}' não foi adivinhada. Último palpite por: {jogador}.")
            print("Encerrando conexão com o servidor...")
            clientSocket.close()
            break
        elif comando == "ERROR":
            print("Erro recebido do servidor:", " ".join(partes[1:]))
            if "ALREADY_GUESSED" not in msg and "INVALID_LETTER" not in msg and "INVALID_WORD_LENGTH" not in msg:
                clientSocket.close()
                break
        else:
            print(f"Mensagem desconhecida recebida: {msg}")
if __name__ == "__main__":
    main()

