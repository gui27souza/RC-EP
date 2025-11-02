import sys
from typing import Tuple

# Verificação de parâmetros para execução do script de cliente
def check() -> Tuple[str, str, int]:
    '''
    Checa os parâmetros de execução do script de cliente.\n
    Retorna o nome do jogador, o ip e a porta.\n
    Caso o ip e a porta não sejam definidos, por default é 127.0.0.1:6891
    '''
    
    try:
      
        # Quantidade de parâmetros
        if len(sys.argv) < 2 or len(sys.argv) > 3: raise Exception

        # Nome do jogador
        nome_jogador = sys.argv[1]

        # Armazena a string ip:porta e faz a devida separação
        if len(sys.argv) == 3:
            ip_porta = sys.argv[2]
            ip, porta_str = ip_porta.split(":")
            porta = int(porta_str)
            if porta < 0 or porta > 65535: raise Exception

            if ip == "localhost":
                ip = "127.0.0.1"
            else:
                ip_check = ip.split(".")
                if len(ip_check) != 4: raise Exception
                for ip_part in ip_check:
                    if ip_part[0] == '0' and len(ip_part) != 1 or \
                    not 0 <= int(ip_part) <= 255: raise Exception

        # Valor default
        else:
            ip = "127.0.0.1"
            porta = 6891

        return nome_jogador, ip, porta

    # Erro - Parâmetros inválidos
    except Exception:
        print("\nUso correto dos parâmetros: python3 -m app.app_client.main <nome-do-jogador> <IP>:<Porta>\nO nome do jogador não deve ter espaços, e o endereço/porta deve ter o formato X.X.X.X:X\n")
        sys.exit(1)
