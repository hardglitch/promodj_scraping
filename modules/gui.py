from pathlib import Path
from sys import exit
from time import time
from typing import Any, Dict, List, Optional, get_args

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QCheckBox, QComboBox, QFileDialog, QLabel, QMainWindow, QProgressBar, \
    QPushButton, QStyle
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from qasync import asyncSlot
from qdarktheme import setup_theme

from data.data import CONST
from data.dictionary import Dictionary
from modules import debug
from modules.manager import Manager
from util.settings_module.settings_module import Parameter, Settings


class MainWindow(QMainWindow):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._font = QFont("Arial", 10)
        self._settings_file: Settings = Settings()
        self._last_launch = int(time())
        self._music: Optional[Manager] = None
        self._genres: Dict[str, str] = {}
        [self._genres.update({value: CONST.DefaultValues.genres[n + 1]})
                for n, value in enumerate(CONST.DefaultValues.genres) if n % 2 == 0]

        self._theme: CONST.DefaultValues.THEMES = CONST.DefaultValues.theme
        setup_theme(theme=self._theme, additional_qss="QToolTip {color: black;}")
        self.setWindowIcon(QIcon("logo.ico"))

        self.setWindowTitle(Dictionary.INSCRIPTIONS.PromoDJMusicDownloader)
        self.setFixedSize(530, 200)

        self.cmbGenre = QComboBox(self)
        self.cmbGenre.setToolTip(Dictionary.MESSAGES.ToolTips.Genre)
        self.cmbGenre.resize(220, 24)
        self.cmbGenre.move(10, 10)
        self.cmbGenre.setDuplicatesEnabled(False)
        self.cmbGenre.addItems(self._genres.keys())
        self.cmbGenre.setCurrentText(CONST.DefaultValues.genre)
        self.cmbGenre.setFont(self._font)

        self.cmbForm = QComboBox(self)
        self.cmbForm.resize(70, 24)
        self.cmbForm.move(230, 10)
        self.cmbForm.addItems(get_args(CONST.DefaultValues.FORMS))
        self.cmbForm.setCurrentIndex(1)
        self.cmbForm.setFont(self._font)

        self.cmbQuantity = QComboBox(self)
        self.cmbQuantity.resize(60, 24)
        self.cmbQuantity.move(300, 10)
        self.cmbQuantity.setEditable(True)
        self.cmbQuantity.setDuplicatesEnabled(False)
        self.cmbQuantity.addItems([str(i) for i in range(1,11)])
        self.cmbQuantity.addItems(["20", "30", "40", "50", "100"])
        self.cmbQuantity.setCurrentText(str(CONST.DefaultValues.quantity))
        self.cmbQuantity.setToolTip(Dictionary.MESSAGES.ToolTips.Quantity)
        self.cmbQuantity.setFont(self._font)

        self.lblQuantity = QLabel(Dictionary.INSCRIPTIONS.Files, self)
        self.lblQuantity.move(360, 10)
        self.lblQuantity.setFont(self._font)

        self.chbPeriod = QCheckBox(Dictionary.INSCRIPTIONS.Period, self)
        self.chbPeriod.setChecked(CONST.DefaultValues.is_period)
        self.chbPeriod.move(300, 40)
        self.chbPeriod.toggled.connect(self.period)
        self.chbPeriod.setToolTip(Dictionary.MESSAGES.ToolTips.Period)
        self.chbPeriod.setFont(self._font)

        self.chbFormat = QCheckBox(Dictionary.INSCRIPTIONS.Lossless, self)
        self.chbFormat.setChecked(True)
        self.chbFormat.move(410, 40)
        self.chbFormat.setToolTip(Dictionary.MESSAGES.ToolTips.Lossless)
        self.chbFormat.setFont(self._font)

        self.chbFileHistory = QCheckBox(Dictionary.INSCRIPTIONS.FileHistory, self)
        self.chbFileHistory.setChecked(CONST.DefaultValues.is_file_history)
        self.chbFileHistory.move(30, 40)
        self.chbFileHistory.resize(100, 30)
        self.chbFileHistory.toggled.connect(self.file_history)
        self.chbFileHistory.setToolTip(Dictionary.MESSAGES.ToolTips.FileHistory)
        self.chbFileHistory.setFont(self._font)

        self.chbRewriteFiles = QCheckBox(Dictionary.INSCRIPTIONS.RewriteFiles, self)
        self.chbRewriteFiles.move(150, 40)
        self.chbRewriteFiles.resize(130, 30)
        self.chbRewriteFiles.setEnabled(not self.chbFileHistory.isChecked())
        self.chbRewriteFiles.setChecked(not CONST.DefaultValues.is_file_history)
        self.chbRewriteFiles.setToolTip(Dictionary.MESSAGES.ToolTips.RewriteFiles)
        self.chbRewriteFiles.setFont(self._font)

        self.cmbThreads = QComboBox(self)
        self.cmbThreads.resize(50, 24)
        self.cmbThreads.move(423, 10)
        [self.cmbThreads.addItem(str(i), i) for i in range(1, CONST.MaxValues.threads + 1)]
        self.cmbThreads.setCurrentText(str(CONST.DefaultValues.threads))
        self.cmbThreads.setToolTip(Dictionary.MESSAGES.ToolTips.Threads)
        self.cmbThreads.setFont(self._font)

        self.lblThreads = QLabel(Dictionary.INSCRIPTIONS.Threads, self)
        self.lblThreads.move(475, 10)
        self.lblThreads.setFont(self._font)

        self.btnSaveTo = QPushButton(self)
        save_pixmap = QStyle.StandardPixmap.SP_DialogSaveButton
        save_icon = self.style().standardIcon(save_pixmap)
        self.btnSaveTo.setIcon(save_icon)
        self.btnSaveTo.setIconSize(QSize(24, 24))
        self.btnSaveTo.setGeometry(10, 85, 24, 24)
        self.btnSaveTo.setToolTip(Dictionary.INSCRIPTIONS.SaveTo)
        self.btnSaveTo.setCheckable(True)
        self.btnSaveTo.clicked.connect(self.save_to)

        self.lblSaveTo = QLabel(str(Path(Path.cwd()).joinpath(CONST.DefaultValues.download_dir)), self)
        self.lblSaveTo.setToolTip(self.lblSaveTo.text())
        self.lblSaveTo.resize(480, 24)
        self.lblSaveTo.move(40, 85)
        self.lblSaveTo.setFont(self._font)

        self.btnDownload = QPushButton(Dictionary.INSCRIPTIONS.Download, self)
        self.btnDownload.move(270, 160)
        self.btnDownload.clicked.connect(self.download_files)
        self.btnDownload.setFont(self._font)

        self.btnExit = QPushButton(Dictionary.INSCRIPTIONS.Exit, self)
        self.btnExit.move(160, 160)
        self.btnExit.clicked.connect(self.app_exit)
        self.btnExit.setFont(self._font)

        self.progBar = QProgressBar(self)
        self.progBar.setGeometry(10, 125, 510, 20)
        self.progBar.setVisible(False)
        self.progBar.setMaximum(100)
        self.progBar.setFont(self._font)

        self.lblMessage = QLabel("", self)
        self.lblMessage.setGeometry(10, 125, 520, 20)
        self.lblMessage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblMessage.setFont(self._font)

        self.lblFiles = QLabel("", self)
        self.lblFiles.move(30, 150)
        self.lblFiles.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblFiles.setFont(self._font)

        self.lblVersion = QLabel(CONST.VERSION, self)
        self.lblVersion.setFont(QFont("Arial", 8))
        self.lblVersion.move(5, 175)

        self.lblAuthor = QLabel('<a href="https://github.com/hardglitch/promodj_scraping" style="text-decoration:none">homepage</a>', self)
        self.lblAuthor.setFont(QFont("Arial", 8))
        self.lblAuthor.setOpenExternalLinks(True)
        self.lblAuthor.move(40, 175)
        self.lblAuthor.setToolTip("https://github.com/hardglitch/promodj_scraping")

        self.cmbLanguage = QComboBox(self)
        self.cmbLanguage.resize(50, 20)
        self.cmbLanguage.move(474, 168)
        self.cmbLanguage.setDuplicatesEnabled(False)
        self.cmbLanguage.addItems(get_args(CONST.DefaultValues.LANGUAGES))
        self.cmbLanguage.setCurrentText(str(CONST.DefaultValues.language))
        self.cmbLanguage.currentTextChanged.connect(self.change_language)
        self.cmbLanguage.setFont(self._font)

        self.btnTheme = QPushButton(self)
        self.btnTheme.setText("☼")
        self.btnTheme.setGeometry(442, 167, 28, 28)
        self.btnTheme.setToolTip(Dictionary.INSCRIPTIONS.SaveTo)
        self.btnTheme.clicked.connect(self.toggle_theme)
        self.btnTheme.setCheckable(True)
        self.btnTheme.setFont(QFont("Arial", 10))

    @asyncSlot()
    async def download_files(self) -> None:
        try:
            self.progBar.setVisible(False)
            self.lblFiles.setText("")
            self.lblMessage.setText("")

            if self._music:
                self._music.cancel_downloading()
                self.btnDownload.setText(Dictionary.INSCRIPTIONS.Download)
                self._music = None
                return

            self.progBar.setValue(0)
            self.btnDownload.setText(Dictionary.INSCRIPTIONS.Cancel)

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
                Parameter(CONST.Parameters.Threads, self.cmbThreads.currentText()),
                Parameter(CONST.Parameters.Language, self.cmbLanguage.currentText()),
                Parameter(CONST.Parameters.Theme, self._theme)
            )

        except Exception as error:
            debug.log("Error", error=error)


    def download_successed(self, value: int) -> None:
        self.progBar.setVisible(False)
        self.lblFiles.setText("")

        if value == 1: self.lblMessage.setText(Dictionary.MESSAGES.AllFilesDownloaded)
        else: self.lblMessage.setText(Dictionary.MESSAGES.MatchingFilesNotFound)

        if self._music:
            self.btnDownload.setText(Dictionary.INSCRIPTIONS.Download)
            self.btnDownload.setChecked(False)
            self._music.cancel_downloading()
            self._music = None

    def search(self, value: int = 0, mode: int = 0) -> None:
        if self.progBar.isVisible(): self.progBar.setVisible(False)
        if mode == 1:
            self.lblMessage.setText("." * value + Dictionary.MESSAGES.Searching + "." * value)
        elif mode == 2:
            self.lblMessage.setText("." * value + Dictionary.MESSAGES.Analysis + "." * value)
        else:
            self.lblMessage.setText("")
            self.progBar.setVisible(True)

    def message(self, value: str = "") -> None:
        if self.progBar.isVisible(): self.progBar.setVisible(False)
        if value:
            self.lblMessage.setText(value[:100])
        else:
            self.lblMessage.setText("")
            self.progBar.setVisible(True)

    def file_info(self, total_downloaded: int = 0, total_files: int = 0) -> None:
        self.lblFiles.setText(f"{total_downloaded}/{total_files}")

    def period(self) -> None:
        if self.chbPeriod.isChecked():
            self.lblQuantity.setText(Dictionary.INSCRIPTIONS.LastDays)
        else:
            self.lblQuantity.setText(Dictionary.INSCRIPTIONS.Files)

    def file_history(self) -> None:
        self.chbRewriteFiles.setEnabled(not self.chbFileHistory.isChecked())

    def save_to(self) -> None:
        save_to_dir = QFileDialog.getExistingDirectory(self)
        if save_to_dir:
            self.lblSaveTo.setText(str(Path(save_to_dir)))
            self.lblSaveTo.setToolTip(self.lblSaveTo.text())
        self.btnSaveTo.setChecked(False)

    def change_language(self) -> None:
        Dictionary.set_new_language(self.cmbLanguage.currentText())
        self.cmbGenre.setToolTip(Dictionary.MESSAGES.ToolTips.Genre)
        self.cmbQuantity.setToolTip(Dictionary.MESSAGES.ToolTips.Quantity)
        self.chbPeriod.setToolTip(Dictionary.MESSAGES.ToolTips.Period)
        self.chbFormat.setToolTip(Dictionary.MESSAGES.ToolTips.Lossless)
        self.chbFormat.setText(Dictionary.INSCRIPTIONS.Lossless)
        self.chbFileHistory.setToolTip(Dictionary.MESSAGES.ToolTips.FileHistory)
        self.chbRewriteFiles.setToolTip(Dictionary.MESSAGES.ToolTips.RewriteFiles)
        self.cmbThreads.setToolTip(Dictionary.MESSAGES.ToolTips.Threads)
        self.btnSaveTo.setToolTip(Dictionary.INSCRIPTIONS.SaveTo)
        self.btnExit.setText(Dictionary.INSCRIPTIONS.Exit)
        self.period()
        if self._music: self.btnDownload.setText(Dictionary.INSCRIPTIONS.Cancel)
        else: self.btnDownload.setText(Dictionary.INSCRIPTIONS.Download)
        self.lblThreads.setText(Dictionary.INSCRIPTIONS.Threads)
        self.chbPeriod.setText(Dictionary.INSCRIPTIONS.Period)
        self.chbFileHistory.setText(Dictionary.INSCRIPTIONS.FileHistory)
        self.chbRewriteFiles.setText(Dictionary.INSCRIPTIONS.RewriteFiles)
        self.setWindowTitle(Dictionary.INSCRIPTIONS.PromoDJMusicDownloaderExtended.replace("_",
                            str(int(abs((int(time()) - self._last_launch) / (3600 * 24))))))

    def toggle_theme(self) -> None:
        self._theme = CONST.Parameters.Light if self._theme == CONST.Parameters.Dark else CONST.Parameters.Dark
        setup_theme(theme=self._theme, additional_qss="QToolTip {color: black;}")
        self.btnTheme.setChecked(False)

    def app_exit(self) -> None:
        QApplication.instance().quit()
        exit(0)


    @asyncSlot()
    async def set_actual_genres(self) -> None:
        async with ClientSession() as session:
            tags_link = r"https://promodj.com/music"
            async with session.get(tags_link) as response:
                if response.status != 200:
                    self.lblMessage.setText(Dictionary.MESSAGES.Errors.UnableToConnect)
                    debug.log(Dictionary.MESSAGES.Errors.UnableToConnect + f" {response.status=}")
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
    async def set_settings(self) -> None:
        settings_list: Optional[List[Parameter]] = await self._settings_file.read()

        if settings_list:
            for param in settings_list:

                if param.name == CONST.Parameters.Theme and param.value in get_args(CONST.DefaultValues.THEMES):
                    self._theme = param.value
                    setup_theme(theme=self._theme, additional_qss="QToolTip {color: black;}")

                if param.name == CONST.Parameters.LastDownload and param.value.isnumeric():
                    self._last_launch = abs(int(param.value))
                    self.setWindowTitle(Dictionary.INSCRIPTIONS.PromoDJMusicDownloaderExtended.replace("_",
                                        str(int(abs((int(time()) - self._last_launch) / (3600 * 24))))))

                elif param.name == CONST.Parameters.Genre and param.value in self._genres.keys():
                    self.cmbGenre.setCurrentText(param.value)

                elif param.name == CONST.Parameters.DownloadDirectory and Path(param.value).exists():
                    self.lblSaveTo.setText(str(Path(param.value)))
                    self.lblSaveTo.setToolTip(self.lblSaveTo.text())

                elif param.name == CONST.Parameters.Form and param.value in get_args(CONST.DefaultValues.FORMS):
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

                elif param.name == CONST.Parameters.Language and param.value in get_args(CONST.DefaultValues.LANGUAGES):
                    self.cmbLanguage.setCurrentText(param.value)

        await self.set_actual_genres()

        if settings_list:
            for param in settings_list:
                if param.name == CONST.Parameters.Genre and param.value in self._genres.keys():
                    self.cmbGenre.setCurrentText(param.value)
