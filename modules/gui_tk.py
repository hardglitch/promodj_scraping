from .base import Base
from tkinter import Tk, ttk, font
from typing import Optional

from .base import Base
from .data import Data


class MainWindow(Tk):
    def __init__(self, loop, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.queue = Queue()
        self.refresh_ms = 25

        self._loop = loop
        self._downloading: Optional[Base] = None

        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.config(size=12)
        self.option_add("*Font", self.defaultFont)

        self.title("PromoDJ Music Downloader")
        self.geometry("630x200")
        self.resizable(False, False)

        self.cmbGenre = ttk.Combobox(self, values=["PromoDJ Music Downloader"], width=25, state="readonly")
        self.cmbGenre.place(x=10, y=10)
        self.cmbGenre.current(0)

        self.cmbForm = ttk.Combobox(self, values=Data.FORMS, width=5, state="readonly")
        self.cmbForm.place(x=260, y=10)
        self.cmbForm.current(1)

        self.cmbQuantity = ttk.Combobox(self, values=["1", "5", "10", "20", "50", "100"], width=4)
        self.cmbQuantity.place(x=330, y=10)
        self.cmbQuantity.current(2)
        # self.cmbQuantity.addItem(str(Data.Values.quantity), str(Data.Values.quantity))

        self.lblQuantity = ttk.Label(self, text="files")
        self.lblQuantity.place(x=390, y=10)

        self.chbPeriod = ttk.Checkbutton(self, text="Period")
        self.chbPeriod.place(x=330, y=40)
        # self.chbPeriod.setChecked(False)
        # self.chbPeriod.move(300, 40)
        # self.chbPeriod.toggled.connect(self.event_chb_period)
