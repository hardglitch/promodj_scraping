from pathlib import Path
from sys import exit
from time import time
from typing import Dict, List, Optional

from PyQt6 import QtCore
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QCheckBox, QComboBox, QFileDialog, QLabel, QMainWindow, QProgressBar, \
    QPushButton
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from qasync import asyncSlot

from modules import debug
from modules.data import Data
from modules.manager import Manager
from modules.messages import Messages
from utils.settings.settings import Parameter, Settings


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self._settings_file: Settings = Settings()
        self._last_launch = int(time())
        self._music: Optional[Manager] = None
        self._genres: Dict[str, str] = {}

        self.setWindowIcon(QIcon("logo.ico"))

        self.setFont(QFont("Arial", 12))
        self.setWindowTitle(Data.Inscriptions.PromoDJMusicDownloader)
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
        self.cmbQuantity.setCurrentText(str(Data.DefaultValues.quantity))

        self.lblQuantity = QLabel(Data.Inscriptions.Files, self)
        self.lblQuantity.move(365, 8)

        self.chbPeriod = QCheckBox(Data.Inscriptions.Period, self)
        self.chbPeriod.setChecked(Data.DefaultValues.is_period)
        self.chbPeriod.move(300, 40)
        self.chbPeriod.toggled.connect(self.event_chb_period)

        self.chbFormat = QCheckBox(Data.Inscriptions.Lossless, self)
        self.chbFormat.setChecked(True)
        self.chbFormat.move(30, 40)

        self.chbFileHistory = QCheckBox(Data.Inscriptions.FileHistory, self)
        self.chbFileHistory.setChecked(Data.DefaultValues.is_file_history)
        self.chbFileHistory.move(390, 40)
        self.chbFileHistory.resize(100, 30)
        self.chbFileHistory.toggled.connect(self.event_chb_file_history)

        self.chbRewriteFiles = QCheckBox(Data.Inscriptions.RewriteFiles, self)
        self.chbRewriteFiles.move(130, 40)
        self.chbRewriteFiles.resize(120, 30)
        self.chbRewriteFiles.setEnabled(not self.chbFileHistory.isChecked())
        self.chbRewriteFiles.setChecked(not Data.DefaultValues.is_file_history)

        self.cmbThreads = QComboBox(self)
        self.cmbThreads.resize(34, 24)
        self.cmbThreads.move(433, 10)
        [self.cmbThreads.addItem(str(i), i) for i in range(1, Data.MaxValues.threads + 1)]
        self.cmbThreads.setCurrentText(str(Data.DefaultValues.threads))

        self.lblThreads = QLabel(Data.Inscriptions.Threads, self)
        self.lblThreads.move(470, 8)

        self.btnSaveTo = QPushButton(Data.Inscriptions.SaveTo, self)
        self.btnSaveTo.setGeometry(10, 85, 70, 24)
        self.btnSaveTo.setCheckable(True)
        self.btnSaveTo.clicked.connect(self.save_to)

        self.lblSaveTo = QLabel(str(Path(Path.cwd()).joinpath(Data.DefaultValues.download_dir)), self)
        self.lblSaveTo.resize(435, 24)
        self.lblSaveTo.move(85, 85)

        self.btnDownload = QPushButton(Data.Inscriptions.Download, self)
        self.btnDownload.move(270, 160)
        self.btnDownload.clicked.connect(self.download_files)

        self.btnExit = QPushButton(Data.Inscriptions.Exit, self)
        self.btnExit.move(160, 160)
        self.btnExit.clicked.connect(self.app_exit)

        self.progBar = QProgressBar(self)
        self.progBar.setGeometry(10, 125, 520, 20)
        self.progBar.setVisible(False)
        self.progBar.setMaximum(100)

        self.lblMessage = QLabel("", self)
        self.lblMessage.setGeometry(10, 125, 520, 20)
        self.lblMessage.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.lblFiles = QLabel("", self)
        self.lblFiles.move(30, 160)
        self.lblFiles.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    @asyncSlot()
    async def download_files(self):
        try:
            self.progBar.setVisible(False)
            self.lblFiles.setText("")
            self.lblMessage.setText("")

            if self._music:
                self._music.cancel_downloading()
                self.btnDownload.setText(Data.Inscriptions.Download)
                self._music = None
                return

            self.progBar.setValue(0)
            self.btnDownload.setText(Data.Inscriptions.Cancel)

            quantity: int = int(self.cmbQuantity.currentText()) \
                if self.cmbQuantity.currentText().isnumeric() \
                   and int(self.cmbQuantity.currentText()) <= abs(Data.MaxValues.quantity) \
                else abs(Data.DefaultValues.quantity)

            self._music = Manager(download_dir=self.lblSaveTo.text(),
                     genre=self._genres[self.cmbGenre.currentText()],
                     form=self.cmbForm.currentText(),
                     is_lossless=self.chbFormat.isChecked(),
                     quantity=quantity,
                     is_period=self.chbPeriod.isChecked(),
                     threads=int(self.cmbThreads.currentText()),
                     is_rewrite_files=self.chbRewriteFiles.isChecked(),
                     is_file_history=self.chbFileHistory.isChecked()
            )
            if not Path(self.lblSaveTo.text()).exists():
                Path(Data.DefaultValues.download_dir).mkdir()

            self._music.progress.connect(self.progBar.setValue)
            self._music.success.connect(self.download_successed)
            self._music.search.connect(self.search)
            self._music.message.connect(self.message)
            self._music.file_info.connect(self.file_info)
            self._music.start_downloading()

            await self._settings_file.write(
                Parameter(Data.Parameters.LastDownload, str(int(time()))),
                Parameter(Data.Parameters.DownloadDirectory, self.lblSaveTo.text()),
                Parameter(Data.Parameters.Genre, self.cmbGenre.currentText()),
                Parameter(Data.Parameters.Form, self.cmbForm.currentText()),
                Parameter(Data.Parameters.Lossless, str(int(self.chbFormat.isChecked()))),
                Parameter(Data.Parameters.Period, str(int(self.chbPeriod.isChecked()))),
                Parameter(Data.Parameters.RewriteFiles, str(int(self.chbRewriteFiles.isChecked()))),
                Parameter(Data.Parameters.FileHistory, str(int(self.chbFileHistory.isChecked()))),
                Parameter(Data.Parameters.Quantity, self.cmbQuantity.currentText()),
                Parameter(Data.Parameters.Threads, self.cmbThreads.currentText())
            )

        except Exception as error:
            debug.log("Error", error=error)


    def download_successed(self, value: int):
        self.progBar.setVisible(False)
        self.lblFiles.setText("")

        if value == 1: self.lblMessage.setText(Messages.AllFilesDownloaded)
        else: self.lblMessage.setText(Messages.MatchingFilesNotFound)

        if self._music:
            self.btnDownload.setText(Data.Inscriptions.Download)
            self.btnDownload.setChecked(False)
            self._music.cancel_downloading()
            self._music = None

    def search(self, value: int = 0, mode: int = 0):
        if self.progBar.isVisible(): self.progBar.setVisible(False)
        if mode == 1:
            self.lblMessage.setText("." * value + Messages.Searching + "." * value)
        elif mode == 2:
            self.lblMessage.setText("." * value + Messages.Analysis + "." * value)
        else:
            self.lblMessage.setText("")
            self.progBar.setVisible(True)

    def message(self, value: str = ""):
        if self.progBar.isVisible(): self.progBar.setVisible(False)
        if value:
            self.lblMessage.setText(value[:100])
        else:
            self.lblMessage.setText("")
            self.progBar.setVisible(True)

    def file_info(self, total_downloaded: int = 0, total_files: int = 0):
        self.lblFiles.setText(f"{total_downloaded}/{total_files}")

    def event_chb_period(self):
        if self.chbPeriod.isChecked():
            self.lblQuantity.setText(Data.Inscriptions.LastDays)
        else:
            self.lblQuantity.setText(Data.Inscriptions.Files)

    def event_chb_file_history(self):
        self.chbRewriteFiles.setEnabled(not self.chbFileHistory.isChecked())

    def save_to(self):
        save_to_dir = QFileDialog.getExistingDirectory(self)
        self.lblSaveTo.setText(str(Path(save_to_dir)))
        self.btnSaveTo.setChecked(False)

    def app_exit(self):
        QApplication.instance().quit()
        exit(0)


    @asyncSlot()
    async def set_genres(self):
        async with ClientSession() as session:
            tags_link = fr"https://promodj.com/music"
            async with session.get(tags_link) as response:
                if response.status != 200:
                    self.lblMessage.setText(Messages.Errors.UnableToConnect)
                    debug.log(Messages.Errors.UnableToConnect + f" {response.status=}")
                    return
                links = BeautifulSoup(await response.read(), features="html.parser").findAll("a")
                for link in links:
                    if link.has_attr("href") and link["href"].find("/music/") > -1:
                        self._genres.update({link.text: link["href"].replace("/music/", "")})
                self.cmbGenre.addItems(self._genres.keys())
                self.cmbGenre.setCurrentText(Data.DefaultValues.genre)


    @asyncSlot()
    async def set_settings(self):
        settings_list: Optional[List[Parameter]] = await self._settings_file.read()

        if settings_list:
            for param in settings_list:

                if param.name == Data.Parameters.LastDownload and param.value.isnumeric():
                    self._last_launch = abs(int(param.value))
                    self.setWindowTitle(Data.Inscriptions.PromoDJMusicDownloaderExtended.replace("_",
                                        str(int(abs((int(time()) - self._last_launch) / (3600 * 24))))))

                elif param.name == Data.Parameters.DownloadDirectory and Path(param.value).exists():
                    self.lblSaveTo.setText(str(Path(param.value)))

                elif param.name == Data.Parameters.Genre and param.value in self._genres.keys():
                    self.cmbGenre.setCurrentText(param.value)

                elif param.name == Data.Parameters.Form and param.value in Data.FORMS:
                    self.cmbForm.setCurrentText(param.value)

                elif param.name == Data.Parameters.Lossless and param.value in ["0", "1"]:
                    self.chbFormat.setChecked(bool(int(param.value)))

                elif param.name == Data.Parameters.Period and param.value in ["0", "1"]:
                    self.chbPeriod.setChecked(bool(int(param.value)))

                elif param.name == Data.Parameters.FileHistory and param.value in ["0", "1"]:
                    self.chbFileHistory.setChecked(bool(int(param.value)))

                elif param.name == Data.Parameters.RewriteFiles and param.value in ["0", "1"]:
                    self.chbRewriteFiles.setChecked(bool(int(param.value)))

                elif param.name == Data.Parameters.Quantity:
                    param.value = param.value \
                        if param.value.isnumeric() and int(param.value) <= abs(Data.MaxValues.quantity) \
                        else str(abs(Data.DefaultValues.quantity))
                    self.cmbQuantity.setCurrentText(param.value)

                elif param.name == Data.Parameters.Threads:
                    self.cmbThreads.setCurrentText(param.value)   # controlled by Qt

        await self.set_genres()
