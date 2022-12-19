import asyncio
import sys
import traceback
from os import getcwd

import aiohttp
from PyQt6.QtCore import QThreadPool, pyqtSignal, QObject, QRunnable, QMutex, QMutexLocker, pyqtSlot
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QProgressBar, QPushButton, QMainWindow, QComboBox, QCheckBox, QLabel, \
    QFileDialog
from bs4 import BeautifulSoup
from qasync import asyncSlot

from .base import Base
from .data import Data


class WorkerSignals(QObject):
    finish = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(object)

class Worker(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.mutex = QMutex()
        self.is_stop = False

    @pyqtSlot()
    def run(self):
        try:
            with QMutexLocker(self.mutex):
                self.is_stop = False
            result = self.func(self, *self.args, **self.kwargs)
        except BaseException:
            traceback.print_exc()
            exc_type, value = sys.exc_info()[:2]
            self.signals.error.emit(exc_type, value, traceback.format_exc())
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finish.emit()

    def stop(self):
        with QMutexLocker(self.mutex):
            self.is_stop = True

class MainWindow(QMainWindow):

    stop_worker = pyqtSignal()

    def __init__(self, loop=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._loop = loop or asyncio.get_event_loop()
        # self._downloading: Optional[Base] = None

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
        self.cmbQuantity.addItem(str(Data.Values.quantity))

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
        self.btnExit.clicked.connect(QApplication.instance().quit)

        self.progBar = QProgressBar(self)
        self.progBar.setGeometry(10, 125, 520, 20)
        self.progBar.setVisible(False)
        self.progBar.setMaximum(100)

        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(Data.Values.threads)

        self.music: Base = None
        self.worker: Worker = None

    @asyncSlot()
    async def download_files(self):
        try:
            if self.threadpool.activeThreadCount() < self.threadpool.maxThreadCount():
                # if self._downloading is not None:
                #     self._downloading.cancel_downloading()
                #     self._downloading = None
                #     return

                # self.btnDownload.setEnabled(False)
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

                self.music.setTotalProgress.connect(self.progBar.setMaximum)
                self.music.setCurrentProgress.connect(self.progBar.setValue)
                self.music.succeeded.connect(self.download_successed)

                # self.worker = Worker(self.music.get_files)
                # self.worker = Worker(self.music.start_downloading)
                self.music.start_downloading()
                print("dfgdfg")

                # self.worker.signals.finish.connect(self.finish_thread)
                # self.worker.signals.error.connect(self.error_thread)
                # self.worker.signals.result.connect(self.result_thread)

                # self.threadpool.start(self.worker)

                self.btnDownload.setEnabled(True)
                self.btnDownload.setCheckable(True)
        except Exception as error:
            print("Error -", error)


    def error_thread(self, message):
        print("Outputs error logs that occur in asynchronous processing")
        print(message)

    def result_thread(self, message):
        print(f"Return value:{message}")

    def finish_thread(self):
        print("Asynchronous processing is complete")
        # Restore the standard output destination
        self.threadpool.waitForDone()

    def download_successed(self):
        self.progBar.setValue(self.progBar.maximum())

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
