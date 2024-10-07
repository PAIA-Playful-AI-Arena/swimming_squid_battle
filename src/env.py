import json
import os
from enum import auto
from os import path

from mlgame.utils.enum import StringEnum
from mlgame.view.audio_model import SoundProgressSchema

# game
WIDTH = 950
WIDTH_OF_INFO = 250

HEIGHT = 600
BG_COLOR = "#2B2B49"
PG_COLOR = "#B3E5FC"
SCORE_COLOR_PLUS = "#76ff03"
SCORE_COLOR_MINUS = "#ec407a"

# ball -> squid
# BALL_COLOR = "#FFEB3B"
SQUID_W = 30
SQUID_H = 45
LEVEL_THRESHOLDS = [10, 30, 60, 100, 150, 200]
LEVEL_PROPERTIES = {
    1: {'size_ratio': 1.0, 'vel': 25},
    2: {'size_ratio': 1.2, 'vel': 21},
    3: {'size_ratio': 1.4, 'vel': 18},
    4: {'size_ratio': 1.6, 'vel': 16},
    5: {'size_ratio': 1.8, 'vel': 12},
    6: {'size_ratio': 2.0, 'vel': 9},
}

COLLISION_SCORE = {
    "WIN": 10,
    "LOSE": -10,
    "DRAW": -5
}

ASSET_IMAGE_DIR = path.join(path.dirname(__file__), "../asset/img")


# food
class FoodTypeEnum(StringEnum):
    FOOD_1 = auto()
    FOOD_2 = auto()
    FOOD_3 = auto()
    GARBAGE_1 = auto()
    GARBAGE_2 = auto()
    GARBAGE_3 = auto()


FOOD_LV1_SIZE = 30
FOOD_LV2_SIZE = 40
FOOD_LV3_SIZE = 50


def get_game_version(json_file_path):
    """
    Load a JSON file and return the value of the 'game_version' field.

    :param json_file_path: Path to the JSON file.
    :return: The game version if found, otherwise None.
    """
    if not os.path.exists(json_file_path):
        print(f"Error: The file '{json_file_path}' does not exist.")
        return None

    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError as jde:
        print(f"Error decoding JSON: {jde}")
        return "develop"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "develop"

    # Check if 'game_version' exists in the JSON data
    if 'version' in data:
        return data['version']
    else:
        print("Error: 'game_version' field is missing in the JSON data.")
        return 'develop'


# path of assets
ASSET_PATH = path.join(path.dirname(__file__), "..", "asset")
LEVEL_PATH = path.join(path.dirname(__file__), "..", "levels")
SOUND_PATH = path.join(path.dirname(__file__), "..", "asset", "sounds")
MUSIC_PATH = path.join(path.dirname(__file__), "..", "asset", "music")
BGM01_FILE_NAME = "bgm01.mp3"
BGM01_PATH = path.join(MUSIC_PATH, BGM01_FILE_NAME)
BGM02_FILE_NAME = "bgm02.mp3"
BGM02_PATH = path.join(MUSIC_PATH, BGM02_FILE_NAME)
BGM02_FILE_NAME = "bgm03.mp3"
BGM03_PATH = path.join(MUSIC_PATH, BGM02_FILE_NAME)
EATING_GOOD_PATH = path.join(SOUND_PATH, "eat_good_food.mp3")
EATING_BAD_PATH = path.join(SOUND_PATH, "eat_bad_food.mp3")
PASS_PATH = path.join(SOUND_PATH, "pass.mp3")
FAIL_PATH = path.join(SOUND_PATH, "fail.mp3")
LV_UP_PATH = path.join(SOUND_PATH, "lv_up.mp3")
LV_DOWN_PATH = path.join(SOUND_PATH, "lv_down.mp3")
COLLISION_PATH = path.join(SOUND_PATH, "collision.mp3")

BG_PATH = path.join(ASSET_IMAGE_DIR, "background.png")
SQUID_PATH = path.join(ASSET_IMAGE_DIR, "squid.png")
SQUID_HURT_PATH = path.join(ASSET_IMAGE_DIR, "squid-hurt.png")
SQUID2_PATH = path.join(ASSET_IMAGE_DIR, "squid2.png")
SQUID2_HURT_PATH = path.join(ASSET_IMAGE_DIR, "squid2-hurt.png")
STAR_PATH = path.join(ASSET_IMAGE_DIR, "star.png")

IMG_ID_FOOD01_L = "food_01_L"
IMG_ID_FOOD02_L = "food_02_L"
IMG_ID_FOOD03_L = "food_03_L"
IMG_ID_FOOD01_R = "food_01_R"
IMG_ID_FOOD02_R = "food_02_R"
IMG_ID_FOOD03_R = "food_03_R"

FOOD01_L_PATH = path.join(ASSET_IMAGE_DIR, "food_01_L.png")
FOOD02_L_PATH = path.join(ASSET_IMAGE_DIR, "food_02_L.png")
FOOD03_L_PATH = path.join(ASSET_IMAGE_DIR, "food_03_L.png")
FOOD01_R_PATH = path.join(ASSET_IMAGE_DIR, "food_01_R.png")
FOOD02_R_PATH = path.join(ASSET_IMAGE_DIR, "food_02_R.png")
FOOD03_R_PATH = path.join(ASSET_IMAGE_DIR, "food_03_R.png")

GARBAGE01_PATH = path.join(ASSET_IMAGE_DIR, "garbage_01.png")
GARBAGE02_PATH = path.join(ASSET_IMAGE_DIR, "garbage_02.png")
GARBAGE03_PATH = path.join(ASSET_IMAGE_DIR, "garbage_03.png")
GAME_VER = get_game_version(path.join(path.dirname(__file__), "..", "game_config.json"))
ASSET_IMG_URL = "https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/swimming_squid_battle/main/asset/img/"
MUSIC_URL = "https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/swimming_squid_battle/main/asset/music/"
SOUND_URL = "https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/swimming_squid_battle/main/asset/sounds/"
BG_URL = ASSET_IMG_URL + "background.png"
SQUID_URL = ASSET_IMG_URL + "squid.png"
SQUID_HURT_URL = ASSET_IMG_URL + "squid-hurt.png"
SQUID2_URL = ASSET_IMG_URL + "squid2.png"
SQUID2_HURT_URL = ASSET_IMG_URL + "squid2-hurt.png"
STAR_URL = ASSET_IMG_URL + "star.png"
# Food URLs
FOOD01_L_URL = ASSET_IMG_URL + "food_01_L.png"
FOOD02_L_URL = ASSET_IMG_URL + "food_02_L.png"  # Assuming the naming pattern is similar
FOOD03_L_URL = ASSET_IMG_URL + "food_03_L.png"
FOOD01_R_URL = ASSET_IMG_URL + "food_01_R.png"
FOOD02_R_URL = ASSET_IMG_URL + "food_02_R.png"
FOOD03_R_URL = ASSET_IMG_URL + "food_03_R.png"

# Garbage URLs
GARBAGE01_URL = ASSET_IMG_URL + "garbage_01.png"
GARBAGE02_URL = ASSET_IMG_URL + "garbage_02.png"
GARBAGE03_URL = ASSET_IMG_URL + "garbage_03.png"
# Music URL
BGM01_URL = MUSIC_URL + BGM01_FILE_NAME
BGM02_URL = MUSIC_URL + BGM02_FILE_NAME
BGM03_URL = MUSIC_URL + BGM02_FILE_NAME

# Sound URLs
EATING_GOOD_URL = SOUND_URL + "eat_good_food.mp3"
EATING_BAD_URL = SOUND_URL + "eat_bad_food.mp3"
PASS_URL = SOUND_URL + "pass.mp3"
FAIL_URL = SOUND_URL + "fail.mp3"
LV_UP_URL = SOUND_URL + "lv_up.mp3"
LV_DOWN_URL = SOUND_URL + "lv_down.mp3"
COLLISION_URL = SOUND_URL + "collision.mp3"

EATING_GOOD_OBJ = SoundProgressSchema(sound_id='eat_good_food').__dict__
EATING_BAD_OBJ = SoundProgressSchema(sound_id='eat_bad_food').__dict__
PASS_OBJ = SoundProgressSchema(sound_id='pass').__dict__
FAIL_OBJ = SoundProgressSchema(sound_id='fail').__dict__
LV_UP_OBJ = SoundProgressSchema(sound_id='lv_up').__dict__
LV_DOWN_OBJ = SoundProgressSchema(sound_id='lv_down').__dict__
COLLISION_OBJ = SoundProgressSchema(sound_id='collision').__dict__
