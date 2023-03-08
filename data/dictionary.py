from dataclasses import dataclass

from data.data import CONST


@dataclass()
class __Dictionary:

    @dataclass()
    class __Messages:

        @dataclass(slots=True)
        class __Errors:

            NoSuitableParameter: str
            NoLinksToFiltering: str
            UnableToDownload: str
            NoLinkToExtractAName: str
            NoLinkToDownload: str
            NoLinksToDownload: str
            UnableToConnect: str
            SomethingWentWrong: str
            NoDate: str
            NoLinkToWrite: str
            UnableToDownloadAFile: str
            WrongPath: str
            WrongFileName: str
            LinkIsNotAStrType: str
            SecurityThreat: str

            def __init__(self, lang: CONST.DefaultValues.LANGUAGES = "en"):
                match lang:
                    case "en":
                        self.NoSuitableParameter: str = "No suitable parameter"
                        self.NoLinksToFiltering: str = "No Links to filtering"
                        self.UnableToDownload: str = "Unable to download"
                        self.NoLinkToExtractAName: str = "No Link to extract a name"
                        self.NoLinkToDownload: str = "No Link to download"
                        self.NoLinksToDownload: str = "No Links to download"
                        self.UnableToConnect: str = "Unable to connect"
                        self.SomethingWentWrong: str = "Something went wrong"
                        self.NoDate: str = "No Date"
                        self.NoLinkToWrite: str = "No Link to write"
                        self.UnableToDownloadAFile: str = "Unable to download a file"
                        self.WrongPath: str = "Wrong Path"
                        self.WrongFileName: str = "Wrong File Name"
                        self.LinkIsNotAStrType: str = "Link is not a 'str' type"
                        self.SecurityThreat: str = "Security Threat"

                    case "ru":
                        self.NoSuitableParameter: str = "Нет подходящих параметров"
                        self.NoLinksToFiltering: str = "Нет ссылок для фильтрации"
                        self.UnableToDownload: str = "Невозможно скачать"
                        self.NoLinkToExtractAName: str = "Нет ссылки для извлечения имени"
                        self.NoLinkToDownload: str = "Нет ссылки для скачивания"
                        self.NoLinksToDownload: str = "Нет ссылок для скачивания"
                        self.UnableToConnect: str = "Невозможно подключиться"
                        self.SomethingWentWrong: str = "Что-то пошло не так"
                        self.NoDate: str = "Нет даты"
                        self.NoLinkToWrite: str = "Нет ссылки для записи"
                        self.UnableToDownloadAFile: str = "Невозможно скачать файл"
                        self.WrongPath: str = "Неправильный путь"
                        self.WrongFileName: str = "Неправильное имя файла"
                        self.LinkIsNotAStrType: str = "Ссылка не типа 'str'"
                        self.SecurityThreat: str = "Угроза безопасности"


        @dataclass(slots=True)
        class __ToolTips:
            Genre: str = ""
            Quantity: str = ""
            Threads: str = ""
            Period: str = ""
            Lossless: str = ""
            FileHistory: str = ""
            RewriteFiles: str = ""

            def __init__(self, lang: CONST.DefaultValues.LANGUAGES = "en"):
                match lang:
                    case "en":
                        self.Genre = "Genre"
                        self.Quantity = "Number of files (if Period disabled)\n" \
                                        "or days (if Period enabled)"
                        self.Threads = "Number of simultaneously downloaded files"
                        self.Period = "If enabled, search for all files within the specified number of recent days\n" \
                                      "If disabled, search for latest files"
                        self.Lossless = "If enabled, search for files with the following extensions: wav, flac, aiff\n" \
                                        "If disabled, only search for mp3"
                        self.FileHistory = "Enable/Disable history of downloaded files"
                        self.RewriteFiles = "This checkbox only works if File History is DISABLED!\n" \
                                            "If enabled, overwrites existing files on download\n" \
                                            "If disabled, always create new files"

                    case "ru":
                        self.Genre = "Жанр"
                        self.Quantity = "Количество файлов (Если Период выключен)\n" \
                                        "или дней (если Период включен)"
                        self.Threads = "Количество одновременно скачиваемых файлов"
                        self.Period = "Если включено, искать все файлы за указанное количество дней\n" \
                                      "Если выключено, искать последние файлы"
                        self.Lossless = "Если включено, искать файлы со следующими расширениями: wav, flac, aiff\n" \
                                        "Если выключено, искать только mp3"
                        self.FileHistory = "Включить/Выключить историю скачанных файлов"
                        self.RewriteFiles = "Этот чекбокс работает только если История Файлов ВЫКЛЮЧЕНА!\n" \
                                            "Если включено, переписывать существующие файлы при загрузке\n" \
                                            "Если выключено, всегда создавать новые файлы"


        Errors = __Errors()
        ToolTips = __ToolTips()

        MatchingFilesNotFound: str
        AllFilesDownloaded: str
        Searching: str
        Analysis: str

        def __init__(self, lang: CONST.DefaultValues.LANGUAGES = "en"):
            match lang:
                case "en":
                    self.MatchingFilesNotFound = "Matching files not found or already downloaded"
                    self.AllFilesDownloaded = "100% - OK"
                    self.Searching = "searching"
                    self.Analysis = "analysis"

                case "ru":
                    self.MatchingFilesNotFound = "Подходящих файлов не найдено или уже скачаны"
                    self.AllFilesDownloaded = "100% - OK"
                    self.Searching = "поиск"
                    self.Analysis = "анализ"


        def set_new_language(self, lang: CONST.DefaultValues.LANGUAGES):
            self.ToolTips = self.__ToolTips(lang)
            self.Errors = self.__Errors(lang)


    @dataclass(slots=True)
    class __Inscriptions:
        PromoDJMusicDownloader: str
        PromoDJMusicDownloaderExtended: str
        Files: str
        Period: str
        Lossless: str
        FileHistory: str
        RewriteFiles: str
        Threads: str
        SaveTo: str
        Download: str
        Exit: str
        Cancel: str
        LastDays: str

        def __init__(self, lang: CONST.DefaultValues.LANGUAGES = "en"):
            match lang:
                case "en":
                    self.PromoDJMusicDownloader = "PromoDJ Music Downloader"
                    self.PromoDJMusicDownloaderExtended = self.PromoDJMusicDownloader + " --- Last download was _ days ago"
                    self.Files = "files"
                    self.Period = "Period"
                    self.Lossless = "Lossless"
                    self.FileHistory = "File History"
                    self.RewriteFiles = "Overwrite Files"
                    self.Threads = "threads"
                    self.SaveTo = "Save to"
                    self.Download = "Download"
                    self.Exit = "Exit"
                    self.Cancel = "Cancel"
                    self.LastDays = "last days"

                case "ru":
                    self.PromoDJMusicDownloader = "PromoDJ Загрузчик"
                    self.PromoDJMusicDownloaderExtended = self.PromoDJMusicDownloader + " --- Последняя загрузка была _ дней назад"
                    self.Files = "файлов"
                    self.Period = "Период"
                    self.Lossless = "Без потерь"
                    self.FileHistory = "История"
                    self.RewriteFiles = "Переписывать"
                    self.Threads = "потоки"
                    self.SaveTo = "Сохранить в"
                    self.Download = "Скачать"
                    self.Exit = "Выход"
                    self.Cancel = "Отмена"
                    self.LastDays = "дней"


    MESSAGES = __Messages()
    INSCRIPTIONS = __Inscriptions()

    def set_new_language(self, lang: CONST.DefaultValues.LANGUAGES = CONST.DefaultValues.language):
        self.MESSAGES = self.__Messages(lang)
        self.MESSAGES.set_new_language(lang)
        self.INSCRIPTIONS = self.__Inscriptions(lang)

Dictionary = __Dictionary()