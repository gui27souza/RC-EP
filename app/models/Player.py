from dataclasses import dataclass

from socket import socket

@dataclass
class Player:

    socket: socket
    name: str
    address: str
