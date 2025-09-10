'''
### Funções de Checagem de parâmetros
'''

import sys

# Verificação de parâmetros para execução do script de servidor
def check_server_execution_parameters() -> {int, int}:
  '''
  #### Checagem de parâmetros server
  - Checa os parâmetros de execução do script de servidor
  - Retorna o número de jogadores e a porta
  - Caso a porta não seja definida, por default é 6891
  '''
  
  # Verificação de parâmetros
  try:

    # Quantidade de parâmetros
    if len(sys.argv) < 2 or len(sys.argv) > 3: raise Exception

    # Número de jogadores
    numero_jogadores = int(sys.argv[1])
    
    # Porta escolhida ou padrão
    if len(sys.argv) == 3:
      porta = int(sys.argv[2])
      if porta < 0 or porta > 65535: raise Exception
    else: porta = 6891

    return numero_jogadores, porta

  # Erro - Parâmetros inválidos
  except Exception:
    print("\nUso correto dos parâmetros: python3 hangman-server.py <numero-de-jogadores> [<porta>]\n")
    sys.exit(1)

# Verificação de parâmetros para execução do script de cliente
def check_client_execution_parameters() -> {str, str, int}:
  '''
  #### Checagem de parâmetros client
  - Checa os parâmetros de execução do script de cliente
  - Retorna o nome do jogador, o ip e a porta
  - Caso o ip e a porta não sejam definidos, por default é 127.0.0.1:6891
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
    print("\nUso correto dos parâmetros: python3 hangman-client.py <nome-do-jogador> <IP>:<Porta>\nO nome do jogador não deve ter espaços, e o endereço/porta deve ter o formato X.X.X.X:X\n")
    sys.exit(1)
