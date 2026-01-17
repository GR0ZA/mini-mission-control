
import socket


class TcUplink:
    def __init__(self, host="sat-simulator", port=6000):
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, packet: bytes):
        self.sock.sendto(packet, self.addr)
        print(f"Sent TC packet to {self.addr[0]}:{self.addr[1]} ({len(packet)} bytes)")
