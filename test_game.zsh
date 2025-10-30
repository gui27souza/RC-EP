#!/bin/zsh

# --- CONFIGURAÇÕES ---
PYTHON_CMD="python3"
SERVER_APP="app.app_server.main" # Assumindo que seu main.py está em app_server
CLIENT_APP="app.app_client.main"
NUM_JOGADORES=3
PORTA=6891
IP="127.0.0.1"
TERMINAL="gnome-terminal"

echo "Iniciando Servidor e 3 Clientes..."

# 1. INICIAR O SERVIDOR
# Note o uso de aspas simples para encapsular o comando completo:
$TERMINAL --title="Servidor Forca" -- /bin/sh -c "$PYTHON_CMD -m $SERVER_APP $NUM_JOGADORES $PORTA" &

sleep 2

# 2. INICIAR OS CLIENTES
$TERMINAL --title="Cliente Alice" -- /bin/sh -c "$PYTHON_CMD -m $CLIENT_APP Alice $IP:$PORTA" &
$TERMINAL --title="Cliente Bob" -- /bin/sh -c "$PYTHON_CMD -m $CLIENT_APP Bob $IP:$PORTA" &
$TERMINAL --title="Cliente Carla" -- /bin/sh -c "$PYTHON_CMD -m $CLIENT_APP Carla $IP:$PORTA" &

echo "Prontos! Verifique as novas janelas do terminal."