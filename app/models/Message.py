from socket import socket
from .Player import Player
from typing import List

from app.debug import print_debug

class Message:

    @staticmethod
    def send_message(socket_end: socket, message: str):
        terminator = "\r\n"
        full_message = (message + terminator).encode('ascii')
        socket_end.sendall(full_message)

    @staticmethod
    def receive_message(socket: socket):

        # Inicia uma sequencia de bits vazia
        buffer = b''
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

class ServerMessage(Message):

    OK = "OK"
    STANDBY = "STANDBY"
    MASTER = "MASTER"
    @staticmethod
    def NEWGAME(lives, word_len): return f"NEWGAME {lives} {word_len}"
    YOURTURN = "YOURTURN"
    @staticmethod
    def STATUS(lives, state, player_name, guess): return f"STATUS {lives} {state} {player_name} {guess}"
    @staticmethod
    def GAMEOVER(result, player, word): return f"GAMEOVER {result} {player} {word}"

    @classmethod
    def send_message_to_player(cls, player: Player, message: str):
        """Função auxiliar para enviar uma mensagem a um jogador."""
        
        try: 
        
            cls.send_message(player.socket, message)
        
            print_debug(f"Enviei a mensagem para o jogador {player.name}:\n{message}")
        
        except:
            print(f"Aviso: Não foi possível enviar mensagem para o jogador {player.name}")

    @classmethod
    def send_message_to_all_players(cls, players: List[Player], message: str):
        """Função auxiliar para enviar uma mensagem a todos os jogadores."""
        for player in players: cls.send_message_to_player(player, message)

    @classmethod
    def receive_message_from_player(cls, player: Player) -> str:
        """Função auxiliar para receber uma mensagem de um jogador."""

        response = cls.receive_message(player.socket)

        print_debug(f"Recebi a mensagem do jogador {player.name}:\n{response}")

        return response


class ClientMessage(Message):

    @staticmethod
    def NEWPLAYER(player_name): return f"NEWPLAYER {player_name}"
    @staticmethod
    def WORD(word): return f"WORD {word}"
    @staticmethod
    def GUESS(type, guess): return f"GUESS {type} {guess}"

    @classmethod
    def send_message_to_server(cls, client_socket: socket, message: str):
        """Função auxiliar para enviar uma mensagem ao servidor."""
        try: 
            
            cls.send_message(client_socket, message)
            
            print_debug(f"Enviei a mensagem:\n{message}")

        except:
            print(f"Aviso: Não foi possível enviar mensagem para o servidor!\nMensagem: '{message}\n'")

    @classmethod
    def receive_message_from_server(cls, client_socket: socket):
        """Função auxiliar para receber uma mensagem do servidor."""

        response = cls.receive_message(client_socket)

        print_debug(f"Recebi a mensagem:\n{response}")

        return response