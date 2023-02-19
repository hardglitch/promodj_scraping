from pathlib import Path
from sys import exit
from time import time
from typing import Dict, List, Optional, get_args

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QCheckBox, QComboBox, QFileDialog, QLabel, QMainWindow, QProgressBar, \
    QPushButton
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from qasync import asyncSlot

from data.data import CONST
from data.messages import MESSAGES
from modules import debug
from modules.manager import Manager
from utils.settings.settings import Parameter, Settings


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._settings_file: Settings = Settings()
        self._last_launch = int(time())
        self._music: Optional[Manager] = None
        self._genres: Dict[str, str] = CONST.DefaultValues.genres

        self.setWindowIcon(QIcon("logo.ico"))

        self.setFont(QFont("Arial", 12))
        self.setWindowTitle(CONST.Inscriptions.PromoDJMusicDownloader)
        self.setFixedSize(530, 200)

        self.cmbGenre = QComboBox(self)
        self.cmbGenre.resize(220, 24)
        self.cmbGenre.move(10, 10)
        self.cmbGenre.addItems(self._genres.keys())
        self.cmbGenre.setCurrentText(CONST.DefaultValues.genre)

        self.cmbForm = QComboBox(self)
        self.cmbForm.resize(70, 24)
        self.cmbForm.move(230, 10)
        self.cmbForm.addItems(get_args(CONST.FORMS))
        self.cmbForm.setCurrentIndex(1)

        self.cmbQuantity = QComboBox(self)
        self.cmbQuantity.resize(60, 24)
        self.cmbQuantity.move(300, 10)
        self.cmbQuantity.setEditable(True)
        self.cmbQuantity.setDuplicatesEnabled(False)
        self.cmbQuantity.addItems([str(i) for i in range(1,11)])
        self.cmbQuantity.addItems(["20", "30", "40", "50", "100"])
        self.cmbQuantity.setCurrentText(str(CONST.DefaultValues.quantity))

        self.lblQuantity = QLabel(CONST.Inscriptions.Files, self)
        self.lblQuantity.move(365, 8)

        self.chbPeriod = QCheckBox(CONST.Inscriptions.Period, self)
        self.chbPeriod.setChecked(CONST.DefaultValues.is_period)
        self.chbPeriod.move(300, 40)
        self.chbPeriod.toggled.connect(self.event_chb_period)

        self.chbFormat = QCheckBox(CONST.Inscriptions.Lossless, self)
        self.chbFormat.setChecked(True)
        self.chbFormat.move(30, 40)

        self.chbFileHistory = QCheckBox(CONST.Inscriptions.FileHistory, self)
        self.chbFileHistory.setChecked(CONST.DefaultValues.is_file_history)
        self.chbFileHistory.move(390, 40)
        self.chbFileHistory.resize(100, 30)
        self.chbFileHistory.toggled.connect(self.event_chb_file_history)

        self.chbRewriteFiles = QCheckBox(CONST.Inscriptions.RewriteFiles, self)
        self.chbRewriteFiles.move(130, 40)
        self.chbRewriteFiles.resize(120, 30)
        self.chbRewriteFiles.setEnabled(not self.chbFileHistory.isChecked())
        self.chbRewriteFiles.setChecked(not CONST.DefaultValues.is_file_history)

        self.cmbThreads = QComboBox(self)
        self.cmbThreads.resize(34, 24)
        self.cmbThreads.move(433, 10)
        [self.cmbThreads.addItem(str(i), i) for i in range(1, CONST.MaxValues.threads + 1)]
        self.cmbThreads.setCurrentText(str(CONST.DefaultValues.threads))

        self.lblThreads = QLabel(CONST.Inscriptions.Threads, self)
        self.lblThreads.move(470, 8)

        self.btnSaveTo = QPushButton(CONST.Inscriptions.SaveTo, self)
        self.btnSaveTo.setGeometry(10, 85, 70, 24)
        self.btnSaveTo.setCheckable(True)
        self.btnSaveTo.clicked.connect(self.save_to)

        self.lblSaveTo = QLabel(str(Path(Path.cwd()).joinpath(CONST.DefaultValues.download_dir)), self)
        self.lblSaveTo.resize(435, 24)
        self.lblSaveTo.move(85, 85)

        self.btnDownload = QPushButton(CONST.Inscriptions.Download, self)
        self.btnDownload.move(270, 160)
        self.btnDownload.clicked.connect(self.download_files)

        self.btnExit = QPushButton(CONST.Inscriptions.Exit, self)
        self.btnExit.move(160, 160)
        self.btnExit.clicked.connect(self.app_exit)

        self.progBar = QProgressBar(self)
        self.progBar.setGeometry(10, 125, 520, 20)
        self.progBar.setVisible(False)
        self.progBar.setMaximum(100)

        self.lblMessage = QLabel("", self)
        self.lblMessage.setGeometry(10, 125, 520, 20)
        self.lblMessage.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lblFiles = QLabel("", self)
        self.lblFiles.move(30, 160)
        self.lblFiles.setAlignment(Qt.AlignmentFlag.AlignCenter)

    @asyncSlot()
    async def download_files(self):
        try:
            self.progBar.setVisible(False)
            self.lblFiles.setText("")
            self.lblMessage.setText("")

            if self._music:
                self._music.cancel_downloading()
                self.btnDownload.setText(CONST.Inscriptions.Download)
                self._music = None
                return

            self.progBar.setValue(0)
            self.btnDownload.setText(CONST.Inscriptions.Cancel)

            quantity: int = int(self.cmbQuantity.currentText()) \
                if self.cmbQuantity.currentText().isnumeric() \
                   and 0 < int(self.cmbQuantity.currentText()) <= abs(CONST.MaxValues.quantity) \
                else abs(CONST.DefaultValues.quantity)
            self.cmbQuantity.setCurrentText(str(quantity))

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
                Path(CONST.DefaultValues.download_dir).mkdir()

            self._music.progress.connect(self.progBar.setValue)
            self._music.success.connect(self.download_successed)
            self._music.search.connect(self.search)
            self._music.message.connect(self.message)
            self._music.file_info.connect(self.file_info)
            self._music.start_downloading()

            await self._settings_file.write(
                Parameter(CONST.Parameters.LastDownload, str(int(time()))),
                Parameter(CONST.Parameters.DownloadDirectory, self.lblSaveTo.text()),
                Parameter(CONST.Parameters.Genre, self.cmbGenre.currentText()),
                Parameter(CONST.Parameters.Form, self.cmbForm.currentText()),
                Parameter(CONST.Parameters.Lossless, str(int(self.chbFormat.isChecked()))),
                Parameter(CONST.Parameters.Period, str(int(self.chbPeriod.isChecked()))),
                Parameter(CONST.Parameters.RewriteFiles, str(int(self.chbRewriteFiles.isChecked()))),
                Parameter(CONST.Parameters.FileHistory, str(int(self.chbFileHistory.isChecked()))),
                Parameter(CONST.Parameters.Quantity, self.cmbQuantity.currentText()),
                Parameter(CONST.Parameters.Threads, self.cmbThreads.currentText())
            )

        except Exception as error:
            debug.log("Error", error=error)


    def download_successed(self, value: int):
        self.progBar.setVisible(False)
        self.lblFiles.setText("")

        if value == 1: self.lblMessage.setText(MESSAGES.AllFilesDownloaded)
        else: self.lblMessage.setText(MESSAGES.MatchingFilesNotFound)

        if self._music:
            self.btnDownload.setText(CONST.Inscriptions.Download)
            self.btnDownload.setChecked(False)
            self._music.cancel_downloading()
            self._music = None

    def search(self, value: int = 0, mode: int = 0):
        if self.progBar.isVisible(): self.progBar.setVisible(False)
        if mode == 1:
            self.lblMessage.setText("." * value + MESSAGES.Searching + "." * value)
        elif mode == 2:
            self.lblMessage.setText("." * value + MESSAGES.Analysis + "." * value)
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
            self.lblQuantity.setText(CONST.Inscriptions.LastDays)
        else:
            self.lblQuantity.setText(CONST.Inscriptions.Files)

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
    async def set_actual_genres(self):
        async with ClientSession() as session:
            tags_link = fr"https://promodj.com/music"
            async with session.get(tags_link) as response:
                if response.status != 200:
                    self.lblMessage.setText(MESSAGES.Errors.UnableToConnect)
                    debug.log(MESSAGES.Errors.UnableToConnect + f" {response.status=}")
                    return
                links = BeautifulSoup(await response.read(), features="html.parser").findAll("a")
                tmp_dict = {}
                for link in links:
                    if link.has_attr("href") and link["href"].find("/music/") > -1:
                        tmp_dict.update({link.text: link["href"].replace("/music/", "")})
                if self._genres != tmp_dict:
                    self._genres.update(tmp_dict)
                    self.cmbGenre.clear()
                    self.cmbGenre.addItems(self._genres.keys())
                    self.cmbGenre.setCurrentText(CONST.DefaultValues.genre)


    @asyncSlot()
    async def set_settings(self):
        settings_list: Optional[List[Parameter]] = await self._settings_file.read()

        if settings_list:
            for param in settings_list:

                if param.name == CONST.Parameters.LastDownload and param.value.isnumeric():
                    self._last_launch = abs(int(param.value))
                    self.setWindowTitle(CONST.Inscriptions.PromoDJMusicDownloaderExtended.replace("_",
                                        str(int(abs((int(time()) - self._last_launch) / (3600 * 24))))))

                elif param.name == CONST.Parameters.Genre and param.value in self._genres.keys():
                    self.cmbGenre.setCurrentText(param.value)

                elif param.name == CONST.Parameters.DownloadDirectory and Path(param.value).exists():
                    self.lblSaveTo.setText(str(Path(param.value)))

                elif param.name == CONST.Parameters.Form and param.value in get_args(CONST.FORMS):
                    self.cmbForm.setCurrentText(param.value)

                elif param.name == CONST.Parameters.Lossless and param.value in ["0", "1"]:
                    self.chbFormat.setChecked(bool(int(param.value)))

                elif param.name == CONST.Parameters.Period and param.value in ["0", "1"]:
                    self.chbPeriod.setChecked(bool(int(param.value)))

                elif param.name == CONST.Parameters.FileHistory and param.value in ["0", "1"]:
                    self.chbFileHistory.setChecked(bool(int(param.value)))

                elif param.name == CONST.Parameters.RewriteFiles and param.value in ["0", "1"]:
                    self.chbRewriteFiles.setChecked(bool(int(param.value)))

                elif param.name == CONST.Parameters.Quantity:
                    param.value = param.value \
                        if param.value.isnumeric() and int(param.value) <= abs(CONST.MaxValues.quantity) \
                        else str(abs(CONST.DefaultValues.quantity))
                    self.cmbQuantity.setCurrentText(param.value)

                elif param.name == CONST.Parameters.Threads:
                    self.cmbThreads.setCurrentText(param.value)   # controlled by Qt

        await self.set_actual_genres()

        if settings_list:
            for param in settings_list:
                if param.name == CONST.Parameters.Genre and param.value in self._genres.keys():
                    self.cmbGenre.setCurrentText(param.value)
