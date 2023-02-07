import asyncio
import socket
import sys

from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from modules.gui import MainWindow


class Start:
    def __init__(self):
        self._test_app = QApplication(sys.argv),
        self._test_loop: asyncio.AbstractEventLoop = QEventLoop(self._test_app)
        asyncio.set_event_loop(self._test_loop)
        MainWindow()

    def test_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ("127.0.0.1", 8181)
        server_socket.bind(server_address)
        server_socket.listen()
        connection, client_address = server_socket.accept()

