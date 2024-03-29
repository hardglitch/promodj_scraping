import asyncio
import sys

from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from modules import gui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = gui.MainWindow()
    window.set_settings()
    window.show()

    with loop:
        loop.run_forever()
