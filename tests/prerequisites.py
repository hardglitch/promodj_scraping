import asyncio
import sys

from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from modules.gui import MainWindow


class Start:
    def __init__(self):
        self._test_app = QApplication(sys.argv)
        self._test_loop: asyncio.AbstractEventLoop = QEventLoop(self._test_app)
        asyncio.set_event_loop(self._test_loop)
        MainWindow()

    # def stop(self):
    #     self._test_loop.close()
