from dataclasses import dataclass
from typing import Literal, Tuple


@dataclass(frozen=True, slots=True)
class Data:

    LOSSLESS_UNCOMPRESSED_FORMATS: Tuple[str, str] = (".wav", ".aiff")
    LOSSLESS_COMPRESSED_FORMATS: Tuple[str] = (".flac",)
    LOSSY_FORMATS: Tuple[str] = (".mp3",)
    DB_NAME: str = "history.db"
    INTERNAL_THREADS: int = 10
    VERSION: str = "v1.5.7"

    @dataclass(frozen=True, slots=True)
    class __DefaultValues:
        FORMS = Literal["mixes", "tracks", "lives"]
        LANGUAGES = Literal["en", "ru", "uk"]
        THEMES = Literal["dark", "light"]

        theme: THEMES = "dark"
        language: LANGUAGES = "en"
        download_dir: str = "Downloaded Music"
        genre: str = "Trance"
        form: FORMS = "tracks"
        quantity: int = 10
        threads: int = 1
        is_lossless: bool = True
        is_period: bool = False
        is_rewrite_files: bool = False
        is_file_history: bool = True
        file_threshold: int = 50
        genres: Tuple[str, ...] = (
            "2 Step", "2_step",
            "8-bit", "8bit",
            "Abstract Hip-Hop", "abstract_hip-hop",
            "Acid", "acid",
            "Acid Breaks", "acid_breaks",
            "Acid House", "acid_house",
            "Acid Jazz", "acid_jazz",
            "Acid Techno", "acid_techno",
            "Acid Trance", "acid_trance",
            "Acoustic", "acoustic",
            "Afro House", "afro_house",
            "Aggrotech", "aggrotech",
            "Alternative Rap", "alternative_rap",
            "Alternative Rock", "alternative_rock",
            "Ambient", "ambient",
            "Ambient Breaks", "ambient_breaks",
            "Ambient Dub", "ambient_dub",
            "Ambient House", "ambient_house",
            "Art Rock", "art_rock",
            "Atmospheric Breaks", "atmospheric_breaks",
            "Baile Funk", "bailefunk",
            "Balearic Beat", "balearic_beat",
            "Bass House", "bass_house",
            "Bassline", "bassline",
            "Beatboxing", "beatboxing",
            "Berlin School", "berlin_school",
            "Big Beat", "big_beat",
            "Big Room House", "big_room_house",
            "Blues", "blues",
            "Bouncy Techno", "bouncy_techno",
            "Breakcore", "breakcore",
            "Breaks", "break_beat",
            "Breakstep", "breakstep",
            "British Rap", "british_rap",
            "Britpop", "britpop",
            "Brokenbeat", "brokenbeat",
            "Brostep", "brostep",
            "Chicago House", "chicago_house",
            "Chillout", "chillout",
            "Chillstep", "chillstep",
            "Chillwave", "chillwave",
            "Chiptune", "chiptune",
            "Classical Crossover", "classical_crossover",
            "Club House", "club_house",
            "Comedy Rap", "comedy_rap",
            "Complextro", "complextro",
            "Crunk", "crunk",
            "Dance Pop", "dance_pop",
            "Dancecore", "dancecore",
            "Dancehall", "dancehall",
            "Dark Ambient", "dark_ambient",
            "Dark Progressive", "dark_progressive",
            "Dark Psy Trance", "dark_psy_trance",
            "Darkstep", "darkstep",
            "Deep House", "deep_house",
            "Deep Techno", "deep_techno",
            "Detroit Techno", "detroit_techno",
            "Digital Hardcore", "digital_hardcore",
            "Dirty Rap", "dirty_rap",
            "Disco", "disco",
            "Disco House", "disco_house",
            "Diss", "diss",
            "Downtempo", "downtempo",
            "Drill'n'bass", "drill_n_bass",
            "Drum & Bass", "dnb",
            "Drumfunk", "drumfunk",
            "Dub", "dub",
            "Dub Techno", "dub_techno",
            "Dubstep", "dubstep",
            "Dubwise", "dubwise",
            "Dutch House", "dutch_house",
            "East Coast Rap", "east_coast_rap",
            "Easy Listening", "easy_listening",
            "Electro", "electro2",
            "Electro House", "electrohouse",
            "Electro Progressive", "electro_progressive",
            "Electro Swing", "electro_swing",
            "Electro Techno", "electro_techno",
            "Electro-punk", "electro_punk",
            "Electroclash", "electroclash",
            "Electronic Body Music", "ebm",
            "Euro Techno", "euro_techno",
            "Euro Trance", "euro_trance",
            "Eurodance", "eurodance",
            "Experimental", "experimental",
            "Fidget House", "fidget",
            "Florida Breaks", "florida_breaks",
            "Footwork", "footwork",
            "Freestyle", "freestyle",
            "French Electro", "french_electro",
            "French House", "french_house",
            "Frenchcore", "frenchcore",
            "Full-On", "full_on",
            "Funk", "funk",
            "Funky Breaks", "funky_breaks",
            "Funky House", "funky_house",
            "Funky Techno", "funky_techno",
            "Future Bass", "future_bass",
            "Future Garage", "future_garage",
            "Future House", "future_house",
            "Futurepop", "futurepop",
            "G-Funk", "g_funk",
            "G-House", "g_house",
            "Gangsta Rap", "gangsta_rap",
            "Garage", "garage",
            "Ghetto House", "ghetto_house",
            "Ghettotech", "ghettotech",
            "Glam Rock", "glam_rock",
            "Glitch", "glitch",
            "Glitch Hop", "glitch_hop",
            "Goa Trance", "goa",
            "Gothic Rock", "gothic_rock",
            "Grime", "grime",
            "Grunge", "grunge",
            "Happy Hardcore", "happy_hardcore",
            "Hard House", "hardhouse",
            "Hard IDM", "hard_idm",
            "Hard Rock", "hard_rock",
            "Hard Techno", "hard_techno",
            "Hard Trance", "hardtrance",
            "Hardcore", "hardcore",
            "Hardcore Continuum ", "hardcore_continuum",
            "Hardcore rap", "hardcore_rap",
            "Hardstep", "hardstep",
            "Hardstyle", "hardstyle",
            "Heavy metal", "heavy_metal",
            "Hi-NRG", "hi_nrg",
            "Hip House", "hip_house",
            "Hip-hop/Rap", "hip_hop",
            "Horrorcore", "horrorcore",
            "House", "house",
            "IDM", "idm",
            "Illbient", "illbient",
            "Indie Dance", "indie_dance",
            "Indie rock", "indie_rock",
            "Indietronica", "indietronica",
            "Industrial", "industrial",
            "Industrial Techno", "industrial_techno",
            "Instrumental", "instrumental",
            "Intelligent", "intelligent",
            "Italo Disco", "italo_disco",
            "Jazz", "jazz",
            "Jazz-Rap", "jazz-rap",
            "Jazzstep", "jazzstep",
            "Jump Up", "jump-up",
            "JumpStyle", "jumpstyle",
            "Jungle", "jungle",
            "Krautrock", "krautrock",
            "Latin House", "latin_house",
            "Latin Pop", "latin_pop",
            "Left-field House", "left_field_house",
            "Leftfield Bass", "leftfield_bass",
            "Liquid funk", "liquid_funk",
            "Live Looping", "live_looping",
            "Lo-Fi", "lofi",
            "Lounge", "lounge",
            "Lowercase", "lowercase",
            "Melbourne Bounce", "melbourne_bounce",
            "Melodic Techno", "",
            "Melodic Trance", "melodic_trance",
            "Miami Bass", "miami_bass",
            "Microhouse", "microhouse",
            "Minimal Techno", "minimal_techno",
            "Minimal psytrance", "minimal_psytrance",
            "Moombahcore", "moombahcore",
            "Moombahsoul", "moombahsoul",
            "Moombahton", "moombahton",
            "Music Concrete", "music_concrete",
            "Neo-Soul", "neo-soul",
            "Neotrance", "neotrance",
            "Neurofunk", "neurofunk",
            "New Age", "new_age",
            "New Beat", "new_beat",
            "New Rave", "new_rave",
            "Noise", "noise",
            "Nortec", "nortec",
            "Nu Breaks", "nu_breaks",
            "Nu Disco", "nu_disco",
            "Nu Jazz", "nu_jazz",
            "Nu metal", "nu_metal",
            "Old School Rap", "old_school_rap",
            "Organic House", "",
            "Pop", "pop",
            "Pop Rap", "pop_rap",
            "Pop Rock", "pop_rock",
            "Post Dubstep", "post_dubstep",
            "Post-punk", "post_punk",
            "Post-rock", "post_rock",
            "Power Noise", "power_noise",
            "Progressive Breaks", "progressive_breaks",
            "Progressive House", "progressive_house",
            "Progressive Trance", "progressive_trance",
            "Progressive rock", "progressive_rock",
            "Psy Chill", "psy_chill",
            "Psy Trance", "psychedelic",
            "Psybient", "psybient",
            "Psychedelic breakbeat", "psy_breaks",
            "Psychedelic rock", "psychedelic_rock",
            "Pumping House", "pumping",
            "Punk rock", "punk_rock",
            "R&B", "rnb",
            "Ragga Jungle", "raggajungle",
            "Raggacore", "raggacore",
            "Rave", "rave",
            "Reggae", "reggae",
            "Reggaeton", "reggaeton",
            "Rock", "rock",
            "Rock'n'roll", "rock_n_roll",
            "Rockabilly", "rockabilly",
            "Russian Pop", "russian_pop",
            "Sambass", "sambass",
            "Schranz", "schranz",
            "Scouse House", "scouse_house",
            "Shoegazing", "shoegazing",
            "Ska", "ska",
            "Slap House", "",
            "Slow Motion House (Disco)", "slow_motion_house_disco",
            "Smooth Jazz", "smooth_jazz",
            "Soul", "soul",
            "Soulful House", "soulful_house",
            "Southern Rap", "southern_rap",
            "Space Disco", "space_disco",
            "Spacesynth", "spacesynth",
            "Speed Garage", "speed_garage",
            "Speedcore", "speedcore",
            "Stoner rock", "stoner_rock",
            "Surf", "surf",
            "Synth-Pop", "synth_pop",
            "Synthwave", "synthwave",
            "Tech House", "techhouse",
            "Tech Trance", "tech_trance",
            "Techno", "techno",
            "Technoid", "technoid",
            "Techstep", "techstep",
            "Teen Pop", "teen_pop",
            "Trance", "trance",
            "Trancestep", "trancestep",
            "Trap", "trap",
            "Tribal House", "tribal_house",
            "Trip-Hop", "trip_hop",
            "Tropical House", "tropical_house",
            "Turntablism", "turntablism",
            "Twerk", "twerk",
            "UK Funky", "uk_funky",
            "UK Garage", "uk_garage",
            "Uplifting Trance", "uplifting_trance",
            "Vocal House", "vocal_house",
            "Vocal Trance", "vocal_trance",
            "West Coast Rap", "west_coast_rap",
            "Witch House", "witch_house",
            "Wonky", "wonky",
            "Yorkshire Bleeps and Bass", "yorkshire_bleeps_and_bass",
            "Аналитика", "analytics",
            "Интервью", "interview",
            "Новости", "news",
            "Обзор", "review",
            "Разговорный", "talk"
        )

    DefaultValues = __DefaultValues()

    @dataclass(frozen=True, slots=True)
    class __MaxValues:
        quantity: int = 1000
        threads: int = 4

    MaxValues = __MaxValues()

    @dataclass(frozen=True, slots=True)
    class __Parameters:
        DownloadDirectory: str = "DownloadDirectory"
        Genre: str = "Genre"
        Form: str = "Form"
        Lossless: str = "Lossless"
        Period: str = "Period"
        Quantity: str = "Quantity"
        Threads: str = "Threads"
        RewriteFiles: str = "RewriteFiles"
        FileHistory: str = "FileHistory"
        LastDownload: str = "LastDownload"
        Language: str = "Language"
        Theme: str = "Theme"
        Dark: str = "dark"
        Light: str = "light"

    Parameters = __Parameters()

CONST = Data()