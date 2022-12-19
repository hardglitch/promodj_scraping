import asyncio
from asyncio import AbstractEventLoop
from threading import Thread

from modules import gui_tk


class ThreadedEventLoop(Thread):
    def __init__(self, loop: AbstractEventLoop):
        super().__init__()
        self._loop = loop
        self.daemon = True
    def run(self):
        self._loop.run_forever()


if __name__ == "__main__":

    eloop = asyncio.new_event_loop()
    asyncio_thread = ThreadedEventLoop(eloop)
    asyncio_thread.start()

    app = gui_tk.MainWindow(eloop)
    app.mainloop()
