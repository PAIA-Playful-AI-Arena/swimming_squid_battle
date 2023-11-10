from enum import auto
from os import path

from mlgame.utils.enum import StringEnum
# game
WIDTH = 900
HEIGHT = 600
BG_COLOR = "#2B2B49"
PG_COLOR = "#B3E5FC"

# ball -> squid
# BALL_COLOR = "#FFEB3B"
SQUID_VEL = 10
SQUID_W = 50
SQUID_H = 70
SQUID_GROWTH_SCORE_STEP = 15
SQUID_GROWTH_SIZE_STEP=10
SQUID_GROWTH_VEL_STEP=3
SQUID_SIZE_MAX = 125
SQUID_SIZE_MIN = 20
SQUID_VEL_MAX = 25
SQUID_VEL_MIN = 10

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

# path of assets
ASSET_PATH = path.join(path.dirname(__file__), "..", "asset")
LEVEL_PATH = path.join(path.dirname(__file__), "..", "levels")
SOUND_PATH = path.join(path.dirname(__file__), "..", "asset", "sounds")
MUSIC_PATH = path.join(path.dirname(__file__), "..", "asset", "music")

BG_PATH = path.join(ASSET_IMAGE_DIR, "background.png")
SQUID_PATH = path.join(ASSET_IMAGE_DIR, "squid.png")
FOOD01_PATH = path.join(ASSET_IMAGE_DIR, "food_01.png")
FOOD02_PATH = path.join(ASSET_IMAGE_DIR, "food_02.png")
FOOD03_PATH = path.join(ASSET_IMAGE_DIR, "food_03.png")
GARBAGE01_PATH = path.join(ASSET_IMAGE_DIR, "garbage_01.png")
GARBAGE02_PATH = path.join(ASSET_IMAGE_DIR, "garbage_02.png")
GARBAGE03_PATH = path.join(ASSET_IMAGE_DIR, "garbage_03.png")

BG_URL = BG_PATH
SQUID_URL = SQUID_PATH
FOOD01_URL = FOOD01_PATH
FOOD02_URL = FOOD02_PATH
FOOD03_URL = FOOD03_PATH
GARBAGE01_URL = GARBAGE01_PATH
GARBAGE02_URL = GARBAGE02_PATH
GARBAGE03_URL = GARBAGE03_PATH
# BAR_URL = "https://raw.githubusercontent.com/PAIA/dont_touch/master/asset/image/bar.png"

