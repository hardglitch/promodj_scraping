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
                        self.NoLinkToWrite: str = "No Link to write to file"
                        self.UnableToDownloadAFile: str = "Unable to download a file"
                        self.WrongPath: str = "Wrong Path"
                        self.WrongFileName: str = "Wrong File Name"
                        self.LinkIsNotAStrType: str = "Link is not a 'str' type"
                        self.SecurityThreat: str = "Security Threat"

                    case "ru":
                        self.NoSuitableParameter: str = "Нет подходящего параметра"
                        self.NoLinksToFiltering: str = "Нет ссылок для фильтрации"
                        self.UnableToDownload: str = "Невозможно скачать"
                        self.NoLinkToExtractAName: str = "Нет ссылки для извлечения имени"
                        self.NoLinkToDownload: str = "Нет ссылки для скачивания"
                        self.NoLinksToDownload: str = "Нет ссылок для скачивания"
                        self.UnableToConnect: str = "Невозможно подключиться"
                        self.SomethingWentWrong: str = "Что-то пошло не так"
                        self.NoDate: str = "Нет даты"
                        self.NoLinkToWrite: str = "Нет ссылки для записи в файл"
                        self.UnableToDownloadAFile: str = "Невозможно скачать файл"
                        self.WrongPath: str = "Неправильный путь"
                        self.WrongFileName: str = "Неправильное имя файла"
                        self.LinkIsNotAStrType: str = "Ссылка не типа 'str'"
                        self.SecurityThreat: str = "Угроза безопасности"

                    case "uk":
                        self.NoSuitableParameter: str = "Немає відповідного параметра"
                        self.NoLinksToFiltering: str = "Немає посилань на фільтрацію"
                        self.UnableToDownload: str = "Неможливо завантажити"
                        self.NoLinkToExtractAName: str = "Немає посилання для отримання імені"
                        self.NoLinkToDownload: str = "Немає посилання для завантаження"
                        self.NoLinksToDownload: str = "Немає посилань для завантаження"
                        self.UnableToConnect: str = "Не може підключитися"
                        self.SomethingWentWrong: str = "Щось пішло не так"
                        self.NoDate: str = "Немає дати"
                        self.NoLinkToWrite: str = "Немає посилання для запису у файл"
                        self.UnableToDownloadAFile: str = "Неможливо завантажити файл"
                        self.WrongPath: str = "Неправильний шлях"
                        self.WrongFileName: str = "Неправильна назва файлу"
                        self.LinkIsNotAStrType: str = "Посилання не має типу 'str'"
                        self.SecurityThreat: str = "Загроза безпеці"


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
                        self.Quantity = "Количество файлов (если Период выключен)\n" \
                                        "или дней (если Период включен)"
                        self.Threads = "Количество одновременно скачиваемых файлов"
                        self.Period = "Если включено, искать все файлы за указанное количество дней\n" \
                                      "Если выключено, искать последние файлы"
                        self.Lossless = "Если включено, искать файлы со следующими расширениями: wav, flac, aiff\n" \
                                        "Если выключено, искать только mp3"
                        self.FileHistory = "Включить/Выключить историю скачанных файлов"
                        self.RewriteFiles = "Этот флажок работает только если История Файлов ВЫКЛЮЧЕНА!\n" \
                                            "Если включено, переписывать существующие файлы при скачивании\n" \
                                            "Если выключено, всегда создавать новые файлы"

                    case "uk":
                        self.Genre = "Жанр"
                        self.Quantity = "Кількість файлів (якщо Крапка вимкнено)\n" \
                                        "чи днів (якщо Крапка увімкнено)"
                        self.Threads = "Кількість файлів, що одночасно скачуються"
                        self.Period = "Якщо увімкнено, шукати всі файли за вказану кількість днів\n" \
                                      "Якщо выключено, шукати останні файли"
                        self.Lossless = "Якщо увімкнено, шукати файли з такими розширеннями: wav, flac, aiff\n" \
                                        "Якщо выключено, шукати тільки mp3"
                        self.FileHistory = "Увімкнути/Вимкнути історію завантажених файлів"
                        self.RewriteFiles = "Цей прапорець працює, лише якщо Iсторія файлів ВИМКНЕНО!\n" \
                                            "Якщо увімкнено, переписувати існуючі файли під час скачування\n" \
                                            "Якщо выключено, завжди створювати нові файли"



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
                case "uk":
                    self.MatchingFilesNotFound = "Відповідні файли не знайдено або вже завантажено"
                    self.AllFilesDownloaded = "100% - OK"
                    self.Searching = "пошук"
                    self.Analysis = "аналіз"



        def set_new_language(self, lang: CONST.DefaultValues.LANGUAGES) -> None:
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
                    self.PromoDJMusicDownloaderExtended = self.PromoDJMusicDownloader + " - Last download was _ days ago"
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
                    self.PromoDJMusicDownloaderExtended = self.PromoDJMusicDownloader + " - Последняя загрузка была _ дней назад"
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

                case "uk":
                    self.PromoDJMusicDownloader = "PromoDJ Завантажувач"
                    self.PromoDJMusicDownloaderExtended = self.PromoDJMusicDownloader + " - Останнє завантаження було _ днів тому"
                    self.Files = "файлів"
                    self.Period = "Крапка"
                    self.Lossless = "Без втрат"
                    self.FileHistory = "Iсторія"
                    self.RewriteFiles = "Переписувати"
                    self.Threads = "нитки"
                    self.SaveTo = "Зберегти у"
                    self.Download = "Завантажити"
                    self.Exit = "Вихід"
                    self.Cancel = "Відміна"
                    self.LastDays = "днiв"


    MESSAGES = __Messages()
    INSCRIPTIONS = __Inscriptions()

    def set_new_language(self, lang: CONST.DefaultValues.LANGUAGES = CONST.DefaultValues.language) -> None:
        self.MESSAGES = self.__Messages(lang)
        self.MESSAGES.set_new_language(lang)
        self.INSCRIPTIONS = self.__Inscriptions(lang)

Dictionary = __Dictionary()