FROM python:3.11.1
WORKDIR /app
COPY __main__.py modules requirements.txt ./
RUN apt update && apt install ffmpeg libsm6 libxext6 libegl1 libxcb-* libxkbcommon-x11-0 libgtk-3-0 libatk1.0-0 -y
RUN pip3 install -r requirements.txt
RUN pip3 install pyinstaller
CMD pyinstaller -n=PDJ_Scraper --icon=logo.ico --onefile -w __main__.py