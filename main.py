import asyncio
import sys

from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from modules import gui
from tests import tests
from tests.config import Config

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    try:                                     # this construction is temporary
        window = gui.MainWindow(loop) if not Config.DEBUG else tests.mock_main_window(loop=loop)
        window.set_settings()
        window.show()
    except AttributeError:
        sys.exit()

    with loop:
        loop.run_forever()
