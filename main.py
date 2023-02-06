import asyncio
import sys

from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from modules import gui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    try:
        window = gui.MainWindow(loop)
        window.set_settings()
        window.show()
    except AttributeError:
        sys.exit()

    with loop:
        loop.run_forever()
