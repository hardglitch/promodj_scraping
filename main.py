import sys
import asyncio
from PyQt6.QtWidgets import QApplication
from modules import gui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = gui.MainWindow()
    # asyncio.run(window.start_gui(app))
    loop = asyncio.new_event_loop()
    loop.run_until_complete(window.set_genres())
    window.show()
    sys.exit(app.exec())
