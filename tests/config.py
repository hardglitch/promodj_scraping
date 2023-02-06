from dataclasses import dataclass

@dataclass()
class Config:

    DEBUG = True

    MOCK_Parameter = False
    MOCK_Settings = False
    MOCK_MainWindow = True
