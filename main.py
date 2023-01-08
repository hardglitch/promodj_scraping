import asyncio
import sys

### uncomment this "from..." to fix pyinstaller "missing file" bug
### I commented this out because PyCharm removes unused import lines by default
# from charset_normalizer import md__mypyc
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from modules import gui

if __name__ == "__main__":

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = gui.MainWindow(loop)
    window.set_settings()
    window.show()
    with loop:
        loop.run_forever()
