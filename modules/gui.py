import asyncio
import os
import sys
import time
from os import getcwd
from pathlib import PurePath

import aiohttp
from PyQt6 import QtCore
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QCheckBox, QComboBox, QFileDialog, QLabel, QMainWindow, QProgressBar, \
    QPushButton
from bs4 import BeautifulSoup
from qasync import asyncSlot

from .base import Base
from .data import Data
from .messages import Messages
from .settings import Parameter, Settings


class MainWindow(QMainWindow):

    def __init__(self, loop=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._loop = loop or asyncio.get_event_loop()
        self._is_downloading: bool = False

        self.settings_file = Settings()
        self.last_launch = int(time.time())

        self.setWindowIcon(QIcon("logo.ico"))

        self.setFont(QFont("Arial", 12))
        self.setWindowTitle("PromoDJ Music Downloader")
        self.setFixedSize(530, 200)

        self.cmbGenre = QComboBox(self)
        self.cmbGenre.resize(220, 24)
        self.cmbGenre.move(10, 10)

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
        self.cmbQuantity.addItems([str(i) for i in range(1,11)])
        self.cmbQuantity.addItems(["20", "30", "40", "50", "100"])
        self.cmbQuantity.setCurrentText(str(Data.Values.quantity))

        self.lblQuantity = QLabel("files", self)
        self.lblQuantity.move(365, 8)

        self.chbPeriod = QCheckBox("Period", self)
        self.chbPeriod.setChecked(Data.Values.is_period)
        self.chbPeriod.move(300, 40)
        self.chbPeriod.toggled.connect(self.event_chb_period)

        self.chbFormat = QCheckBox("Lossless", self)
        self.chbFormat.setChecked(True)
        self.chbFormat.move(30, 40)

        self.chbRewriteFiles = QCheckBox("Rewrite Files", self)
        self.chbRewriteFiles.setChecked(True)
        self.chbRewriteFiles.move(130, 40)
        self.chbRewriteFiles.resize(120, 30)

        self.chbFileHistory = QCheckBox("File History", self)
        self.chbFileHistory.setChecked(False)
        self.chbFileHistory.move(390, 40)
        self.chbFileHistory.resize(100, 30)
        self.chbFileHistory.setEnabled(False)

        self.cmbThreads = QComboBox(self)
        self.cmbThreads.resize(34, 24)
        self.cmbThreads.move(433, 10)
        for i in range(1, Data.MaxValues.threads + 1):
            self.cmbThreads.addItem(str(i), i)
        self.cmbThreads.setCurrentText(str(Data.Values.threads))

        self.lblThreads = QLabel("threads", self)
        self.lblThreads.move(470, 8)

        self.btnSaveTo = QPushButton("Save to", self)
        self.btnSaveTo.setGeometry(10, 85, 70, 24)
        self.btnSaveTo.setCheckable(True)
        self.btnSaveTo.clicked.connect(self.save_to)

        self.lblSaveTo = QLabel(os.path.join(getcwd(), Data.Values.download_dir), self)
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

        self.lblMessage = QLabel("", self)
        self.lblMessage.setGeometry(10, 125, 520, 20)
        self.lblMessage.setVisible(False)
        self.lblMessage.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.music = None
        self.genres = {}

    @asyncSlot()
    async def download_files(self):
        try:
            if self._is_downloading:
                self.music.cancel_downloading()
                self.btnDownload.setText("Download")
                self._is_downloading = False
                self.progBar.setVisible(False)
                return
            else:
                self.btnDownload.setText("Cancel")
                self._is_downloading = True

            self.lblMessage.setVisible(False)
            self.progBar.setVisible(True)
            self.progBar.setValue(0)

            quantity = int(self.cmbQuantity.currentText()) \
                if self.cmbQuantity.currentText().isnumeric() and int(self.cmbQuantity.currentText()) <= abs(Data.MaxValues.quantity) \
                else abs(Data.Values.quantity)

            self.music = Base(download_dir=self.lblSaveTo.text(),
                         genre=self.genres[self.cmbGenre.currentText()],
                         form=self.cmbForm.currentText(),
                         is_lossless=self.chbFormat.isChecked(),
                         quantity=quantity,
                         is_period=self.chbPeriod.isChecked(),
                         is_download=Data.Values.is_download,
                         threads=int(self.cmbThreads.currentText()),
                         is_rewrite_files=self.chbRewriteFiles.isChecked(),
                         is_file_history=self.chbFileHistory.isChecked(),
                         loop=self._loop
            )

            self.music.progress.connect(self.progBar.setValue)
            self.music.succeeded.connect(self.download_successed)
            self.music.start_downloading()

            settings_list = [
                Parameter(Data.Parameters.LastDownload, str(int(time.time()))),
                Parameter(Data.Parameters.DownloadDirectory, self.lblSaveTo.text()),
                Parameter(Data.Parameters.Genre, self.cmbGenre.currentText()),
                Parameter(Data.Parameters.Form, self.cmbForm.currentText()),
                Parameter(Data.Parameters.Lossless, str(int(self.chbFormat.isChecked()))),
                Parameter(Data.Parameters.Period, str(int(self.chbPeriod.isChecked()))),
                Parameter(Data.Parameters.RewriteFiles, str(int(self.chbRewriteFiles.isChecked()))),
                Parameter(Data.Parameters.FileHistory, str(int(self.chbFileHistory.isChecked()))),
                Parameter(Data.Parameters.Quantity, self.cmbQuantity.currentText()),
                Parameter(Data.Parameters.Threads, self.cmbThreads.currentText()),
            ]
            await self.settings_file.write(settings_list)

        except Exception as error:
            print("Error -", error)


    def download_successed(self, value):
        if value == 1:
            self.progBar.setValue(self.progBar.maximum())
        else:
            self.progBar.setVisible(False)
            self.lblMessage.setVisible(True)
            self.lblMessage.setText(Messages.MatchingFilesNotFound)

        self.music.cancel_downloading()
        self.btnDownload.setText("Download")
        self.btnDownload.setChecked(False)
        self._is_downloading = False

    def event_chb_period(self):
        if self.chbPeriod.isChecked():
            self.lblQuantity.setText("last days")
        else:
            self.lblQuantity.setText("files")

    def save_to(self):
        save_to_dir = QFileDialog.getExistingDirectory(self)
        self.lblSaveTo.setText(str(PurePath(save_to_dir)))
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
                        self.genres.update({link.text: link["href"].replace("/music/", "")})
                self.cmbGenre.addItems(self.genres.keys())
                self.cmbGenre.setCurrentText(Data.Values.genre)


    @asyncSlot()
    async def set_settings(self):
        await self.set_genres()

        try:
            settings_list: list[Parameter] = await self.settings_file.read()

            if settings_list:
                for param in settings_list:

                    if param.name == Data.Parameters.LastDownload and param.value.isnumeric():
                        self.last_launch = int(param.value)
                        self.setWindowTitle(
                            f"PromoDJ Music Downloader --- Last download was"
                            f" {int(abs((self.last_launch - int(time.time())) / (3600 * 24)))} days ago")


                    elif param.name == Data.Parameters.DownloadDirectory and os.path.exists(param.value):
                        self.lblSaveTo.setText(str(PurePath(param.value)))

                    elif param.name == Data.Parameters.Genre and param.value in self.genres.keys():
                        self.cmbGenre.setCurrentText(param.value)

                    elif param.name == Data.Parameters.Form and param.value in Data.FORMS:
                        self.cmbForm.setCurrentText(param.value)

                    elif param.name == Data.Parameters.Lossless and param.value in ["0", "1"]:
                        self.chbFormat.setChecked(int(param.value))

                    elif param.name == Data.Parameters.Period and param.value in ["0", "1"]:
                        self.chbPeriod.setChecked(int(param.value))

                    elif param.name == Data.Parameters.RewriteFiles and param.value in ["0", "1"]:
                        self.chbRewriteFiles.setChecked(int(param.value))

                    elif param.name == Data.Parameters.FileHistory and param.value in ["0", "1"]:
                        self.chbFileHistory.setChecked(int(param.value))

                    elif param.name == Data.Parameters.Quantity:
                        param.value = param.value \
                            if param.value.isnumeric() and int(param.value) <= abs(Data.MaxValues.quantity) \
                            else abs(Data.Values.quantity)
                        self.cmbQuantity.setCurrentText(str(param.value))

                    elif param.name == Data.Parameters.Threads:
                        self.cmbThreads.setCurrentText(param.value)   # controlled by Qt

        except FileNotFoundError:
            pass
