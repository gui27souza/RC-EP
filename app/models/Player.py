from dataclasses import dataclass, field

from socket import socket

@dataclass
class Player:

    socket: socket
    name: str
    address: str
