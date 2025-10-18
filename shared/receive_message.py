from socket import socket

# Função auxiliar para receber uma mensagem completa
def receive_message(socket: socket):

    # Inicia uma sequencia de bits vazia
    buffer = b''

    # Identificação do fim de uma mensagem
    terminator = b'\r\n'

    # Leitura de s em porções
    while True:

        # Lê uma porção dos dados.
        data = socket.recv(1024) 
        
        # Conexão encerrada pelo cliente ou erro de rede
        if not data: return None 
        
        # Adiciona a porção ao buffer
        buffer += data
        
        # Verifica se o terminador está no buffer
        if terminator in buffer:

            # Limpa para retornar apenas a mensagem
            message_end_index = buffer.find(terminator) 
            message = buffer[:message_end_index].decode('ascii')
             
            return message
