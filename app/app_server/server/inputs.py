import sys
from typing import Tuple

# Verificação de parâmetros para execução do script de servidor
def check() -> Tuple[int, int]:
    '''
    Checa os parâmetros de execução do script de servidor.\n
    Retorna o número de jogadores e a porta.\n
    Caso a porta não seja definida, por default é 6891.\n
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
        print("\nUso correto dos parâmetros: python3 -m app.app_server.main <numero-de-jogadores> [<porta>]\n")
        sys.exit(1)
