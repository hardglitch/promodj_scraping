from dataclasses import dataclass

@dataclass(frozen=True)
class Messages:

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

    Errors = __Errors()

    MatchingFilesNotFound: str = "Matching files not found or already downloaded"
    AllFilesDownloaded: str = "100% - OK"
    Searching: str = "searching"
    Analysis: str = "analysis"

MESSAGES = Messages()