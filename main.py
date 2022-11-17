import requests
from bs4 import BeautifulSoup


def find_links(links_massive):
    formats = [".flac", ".wav", ".aiff"]
    filtered_links = {}
    for link in links_massive:
        for frmt in formats:
            if link.has_attr("href") and link["href"].find(frmt) > -1:
                filtered_links[link["href"]] = 1  # deduplication
    return list(filtered_links.keys())


def get_music(genre: str = "trance", form: str = "mixes", quantity: int = 10, download: bool = True):

    genres = ["trance", "uplifting_trance", "techno", "dnb", "deep_house", "2_step", "liquid_funk", "neurofunk", "jungle"]
    genre = genre.lower()
    if genre not in genres: return

    forms = ["mixes", "tracks", "lives"]
    form = form.lower()
    if form not in forms: return

    quantity = quantity if quantity < 1000 else 1000

    found_links: list = []
    page: int = 1
    while len(found_links) < quantity:
        r = requests.get(f"https://promodj.com/{form}/{genre}?bitrate=lossless&page={page}")
        if r.status_code == 404:
            break
        html = BeautifulSoup(r.content)
        links = html.findAll("a")
        found_links += find_links(links)
        page += 1

    tmp = {}
    for n in found_links: tmp[n] = 1
    found_links = list(tmp)[:quantity]

    decode_simbols = {"%20": " ", "%28": "(", "%29": ")", "%26": "&", "%23": "#"}

    for count, url in enumerate(found_links):
        response = None
        if download:
            response = requests.get(url)
        filename: str = found_links[count].split("/")[-1]

        for i in decode_simbols:
            filename = filename.replace(i, decode_simbols[i])

        index = 0
        while index != -1:
            index = filename.find(fr"%")
            smb = filename[index:index+3]
            filename = filename.replace(fr"{smb:2}", "")

        path = f"G:\\_DOWNLOADS\\_MUSIC\\" + filename.strip()
        print(count+1, path)

        if download:
            with open(path, "wb") as file:
                file.write(response.content)
            print("File downloaded.")

# --------------------------------------------------------


if __name__ == "__main__":
    get_music("liquid_funk", form="lives", quantity=50, download=True)
