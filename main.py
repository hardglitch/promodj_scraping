import requests
from bs4 import BeautifulSoup
import threading
from time import sleep
from shutil import copyfileobj
from os import remove


# ----------------------------------------------------------------
def get_one_page_links(links_massive) -> list:
    formats = [".flac", ".wav", ".aiff"]
    filtered_links = {}
    for link in links_massive:
        for frmt in formats:
            if link.has_attr("href") and link["href"].find(frmt) > -1:
                filtered_links[link["href"]] = 1  # deduplication
    return list(filtered_links.keys())


# ----------------------------------------------------------------
def get_all_links(form: str = "", genre: str = "", quantity: int = 0) -> list:

    if form == "" or genre == "" or quantity == 0: return []

    found_links: list = []
    page: int = 1
    while len(found_links) < quantity:
        r = requests.get(f"https://promodj.com/{form}/{genre}?bitrate=lossless&page={page}")
        if r.status_code == 404:
            break
        html = BeautifulSoup(r.content)
        links = html.findAll("a")
        found_links += get_one_page_links(links)
        page += 1

    tmp = {}
    for n in found_links: tmp[n] = 1
    return list(tmp)[:quantity]


# ----------------------------------------------------------------
def clean_name(filename: str = ""):
    decode_simbols = {"%20": " ", "%28": "(", "%29": ")", "%26": "&", "%23": "#"}

    for i in decode_simbols:
        filename = filename.replace(i, decode_simbols[i])
    index = 0

    while index != -1:
        index = filename.find(fr"%")
        smb = filename[index:index + 3]
        filename = filename.replace(fr"{smb:2}", "")

    return filename.strip()


# ----------------------------------------------------------------
def set_thread(link: str = "", dl_dir: str = "", filename: str = "file", start: int = 0, current_chunk_size: int = 0, part: int = 0):
    r = requests.get(link, headers={"Range": f"bytes={start + current_chunk_size-1}"}, stream=True)
    filename = filename + str(part)

    print(f"Downloading {filename}")
    with open(dl_dir + filename, "wb") as file:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: file.write(chunk)
    print(f"File save as {dl_dir + filename}")


# ----------------------------------------------------------------
def get_file(link: str = "", dl_dir: str = "", filename: str = "", connections: int = 8):
    r = requests.head(link)
    accept_ranges = "accept-ranges" in r.headers and "bytes" in r.headers["accept-ranges"]
    print(accept_ranges)
    if not accept_ranges:
        return print("No accept-ranges")
    print("sdfdfs - ", r.headers)
    try:
        size: int = int(r.headers["Content-Length"])
        chunk_size: int = int(size / connections)
        remainder: int = (size % connections)
    except KeyError:
        size = 1
        chunk_size = 1
        remainder = 0

    threads: list = []
    for start in range(0, size, chunk_size):
        part = len(threads)
        current_chunk_size = chunk_size if part != connections - 1 else chunk_size + remainder
        trd = threading.Thread(target=set_thread, args=(link, dl_dir, filename, start, current_chunk_size, part))
        threads.append(trd)
        trd.daemon = True
        trd.start()

    file_assembler(dl_dir, filename)


# ----------------------------------------------------------------
def file_assembler(dl_dir: str = "", filename: str = "", connections: int = 8):
    while threading.active_count() > 1:
        sleep(0.1)

    with open(dl_dir + filename, "wb") as file:
        for i in range(connections):
            tmp_filename = filename + str(i)
            copyfileobj(open(dl_dir + tmp_filename, "rb"), file)
            remove(dl_dir + tmp_filename)


# ----------------------------------------------------------------
def get_music(dl_dir: str = "MUSIC", genre: str = "trance", form: str = "mixes", quantity: int = 10, download: bool = True):
    genres = ["trance", "uplifting_trance", "techno", "dnb", "deep_house", "2_step", "liquid_funk", "neurofunk",
              "jungle"]
    genre = genre.lower()
    if genre not in genres: return

    forms = ["mixes", "tracks", "lives"]
    form = form.lower()
    if form not in forms: return

    quantity = quantity if quantity < 1000 else 1000

    found_links = get_all_links(form, genre, quantity)

    for count, link in enumerate(found_links):
        filename: str = found_links[count].split("/")[-1]
        filename = clean_name(filename)
        if download:
            get_file(link, dl_dir, filename)
        else:
            print(count, filename)


# --------------------------------------------------------

if __name__ == "__main__":

    dldir = f"G:\\_DOWNLOADS\\_MUSIC\\"
    get_music(dldir, genre="liquid_funk", form="mixes", quantity=2, download=True)
