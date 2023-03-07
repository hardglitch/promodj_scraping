from dataclasses import dataclass

from data.data import CONST


@dataclass(frozen=True)
class __Messages:

    @dataclass(frozen=True)
    class __Errors:

        NoSuitableParameter: str = "No suitable parameter"
        NoLinksToFiltering: str = "No Links to filtering"
        UnableToDownload: str = "Unable to download"
        NoLinkToExtractAName: str = "No Link to extract a name"
        NoLinkToDownload: str = "No Link to download"
        NoLinksToDownload: str = "No Links to download"
        UnableToConnect: str = "Unable to connect"
        SomethingWentWrong: str = "Something went wrong"
        NoDate: str = "No Date"
        NoLinkToWrite: str = "No Link to write"
        UnableToDownloadAFile: str = "Unable to download a file"
        WrongPath: str = "Wrong Path"
        WrongFileName: str = "Wrong File Name"
        LinkIsNotAStrType: str = "Link is not a 'str' type"
        SecurityThreat: str = "Security Threat"

    Errors = __Errors()

    @dataclass(frozen=True)
    class __ToolTips:

        match CONST.DefaultValues.language:
            case "en":
                Genre: str = "Genre"
                Quantity: str = "Number of files (if Period disabled)\n" \
                                "or days (if Period enabled)"
                Threads: str = "Number of simultaneously downloaded files"
                Period: str = "If enabled, search for all files within the specified number of recent days\n" \
                              "If disabled, search for latest files"
                Lossless: str = "If enabled, search for files with the following extensions: wav, flac, aiff\n" \
                                "If disabled, only search for mp3"
                FileHistory: str = "Enable/Disable history of downloaded files"
                RewriteFiles: str = "This checkbox only works if File History is DISABLED!\n" \
                                    "If enabled, overwrites existing files on download\n" \
                                    "If disabled, always create new files"

    ToolTips = __ToolTips()

    MatchingFilesNotFound: str = "Matching files not found or already downloaded"
    AllFilesDownloaded: str = "100% - OK"
    Searching: str = "searching"
    Analysis: str = "analysis"

MESSAGES = __Messages()