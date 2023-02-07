import asyncio
import sys

from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from modules.gui import MainWindow


def start() -> asyncio.AbstractEventLoop:
    test_app = QApplication(sys.argv)
    test_loop = QEventLoop(test_app)
    asyncio.set_event_loop(test_loop)
    MainWindow(test_loop)
    return test_loop
