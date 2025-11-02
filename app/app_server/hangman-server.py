import sys, traceback

from .run import run_game

if __name__ == "__main__":

    try:
        run_game()

    except KeyboardInterrupt:
        print("\n\nServidor encerrado pelo usuário.\n")
        sys.exit(0)

    except Exception as e:
        print(f"\n\n[ERRO FATAL] O servidor encontrou um erro inesperado: {e}")
        print("--- TRACEBACK COMPLETO ---")
        traceback.print_exc()
        print("--------------------------")
        sys.exit(1)
