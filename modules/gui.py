import asyncio
import sys
from os import getcwd

import aiohttp
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QProgressBar, QPushButton, QMainWindow, QComboBox, QCheckBox, QLabel, \
    QFileDialog
from bs4 import BeautifulSoup
from qasync import asyncSlot

from .base import Base
from .data import Data


class MainWindow(QMainWindow):

    def __init__(self, loop=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._loop = loop or asyncio.get_event_loop()
        self._is_downloading: bool = False

        self.setWindowIcon(QIcon("logo.png"))

        self.setFont(QFont("Arial", 12))
        self.setWindowTitle("PromoDJ Music Downloader")
        self.setFixedSize(530, 200)

        self.cmbGenre = QComboBox(self)
        self.cmbGenre.resize(220, 24)
        self.cmbGenre.move(10, 10)
        self.cmbGenre.addItems(Data.GENRES)

        self.cmbForm = QComboBox(self)
        self.cmbForm.resize(70, 24)
        self.cmbForm.move(230, 10)
        self.cmbForm.addItems(Data.FORMS)
        self.cmbForm.setCurrentIndex(1)

        self.cmbQuantity = QComboBox(self)
        self.cmbQuantity.resize(60, 24)
        self.cmbQuantity.move(300, 10)
        self.cmbQuantity.setEditable(True)
        self.cmbQuantity.setDuplicatesEnabled(False)
        self.cmbQuantity.addItems(["1", "5", "10", "50", "100"])
        self.cmbQuantity.setCurrentText(str(Data.Values.quantity))

        self.lblQuantity = QLabel("files", self)
        self.lblQuantity.move(365, 8)

        self.chbPeriod = QCheckBox("Period", self)
        self.chbPeriod.setChecked(False)
        self.chbPeriod.move(300, 40)
        self.chbPeriod.toggled.connect(self.event_chb_period)

        self.chbFormat = QCheckBox("Lossless", self)
        self.chbFormat.setChecked(True)
        self.chbFormat.move(110, 40)

        self.cmbThreads = QComboBox(self)
        self.cmbThreads.resize(34, 24)
        self.cmbThreads.move(433, 10)
        for i in range(1, Data.MaxValues.threads + 1):
            self.cmbThreads.addItem(str(i), i)
        self.cmbThreads.setCurrentIndex(0)

        self.lblThreads = QLabel("threads", self)
        self.lblThreads.move(470, 8)

        self.btnSaveTo = QPushButton("Save to", self)
        self.btnSaveTo.setGeometry(10, 85, 70, 24)
        self.btnSaveTo.setCheckable(True)
        self.btnSaveTo.clicked.connect(self.save_to)

        Data.Values.download_dir = getcwd()
        self.lblSaveTo = QLabel(Data.Values.download_dir, self)
        self.lblSaveTo.resize(435, 24)
        self.lblSaveTo.move(85, 85)

        self.btnDownload = QPushButton("Download", self)
        self.btnDownload.move(270, 160)
        self.btnDownload.setCheckable(True)
        self.btnDownload.clicked.connect(self.download_files)

        self.btnExit = QPushButton("Exit", self)
        self.btnExit.move(160, 160)
        self.btnExit.setCheckable(True)
        self.btnExit.clicked.connect(self.exit)

        self.progBar = QProgressBar(self)
        self.progBar.setGeometry(10, 125, 520, 20)
        self.progBar.setVisible(False)
        self.progBar.setMaximum(100)

        self.music = None

    @asyncSlot()
    async def download_files(self):
        try:
            if self._is_downloading:
                self.music.cancel_downloading()
                self.btnDownload.setText("Download")
                self._is_downloading = False
                return
            else:
                self.btnDownload.setText("Cancel")
                self._is_downloading = True

            self.progBar.setVisible(True)
            self.progBar.setValue(0)

            Data.Values.genre = Data.GENRES[self.cmbGenre.currentText()]
            Data.Values.form = self.cmbForm.currentText()
            Data.Values.is_lossless = self.chbFormat.isChecked()
            Data.Values.quantity = int(self.cmbQuantity.currentText())
            Data.Values.threads = int(self.cmbThreads.currentText())

            self.music = Base(download_dir=Data.Values.download_dir + fr"\\",
                         genre=Data.Values.genre,
                         form=Data.Values.form,
                         lossless=Data.Values.is_lossless,
                         quantity=Data.Values.quantity,
                         period=self.chbPeriod.isChecked(),
                         download=Data.Values.is_download,
                         threads=Data.Values.threads,
                         loop=self._loop
            )

            self.music.progress.connect(self.progBar.setValue)
            self.music.succeeded.connect(self.download_successed)
            self.music.start_downloading()

        except Exception as error:
            print("Error -", error)


    def download_successed(self):
        self.progBar.setValue(self.progBar.maximum())
        self.music.cancel_downloading()
        self.btnDownload.setText("Download")
        self.btnDownload.setChecked(False)
        self._is_downloading = True

    def event_chb_period(self):
        if self.chbPeriod.isChecked():
            self.lblQuantity.setText("last days")
        else:
            self.lblQuantity.setText("files")

    def save_to(self):
        save_to_dir = QFileDialog.getExistingDirectory(self)
        self.lblSaveTo.setText(str(save_to_dir))
        Data.Values.download_dir = save_to_dir
        self.btnSaveTo.setChecked(False)

    def exit(self):
        QApplication.instance().quit()
        sys.exit(0)

    @asyncSlot()
    async def set_genres(self):
        async with aiohttp.ClientSession() as session:
            tags_link = fr"https://promodj.com/music"
            async with session.get(tags_link) as response:
                if response.status == 404: return {}
                links = BeautifulSoup(await response.read(), features="html.parser").findAll("a")
                for link in links:
                    if link.has_attr("href") and link["href"].find("/music/") > -1:
                        Data.GENRES.update({link.text: link["href"].replace("/music/", "")})
                self.cmbGenre.addItems(Data.GENRES.keys())
                self.cmbGenre.setCurrentText(Data.Values.genre)
