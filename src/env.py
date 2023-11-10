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
BALL_VEL = 10
BALL_W = 50
BALL_H = 70
BALL_GROWTH_SCORE_STEP = 15
BALL_GROWTH_SIZE_STEP=10
BALL_GROWTH_VEL_STEP=3
BALL_SIZE_MAX = 125
BALL_SIZE_MIN = 20
BALL_VEL_MAX = 25
BALL_VEL_MIN = 10

ASSET_IMAGE_DIR = path.join(path.dirname(__file__), "../asset/img")
# food
class FoodTypeEnum(StringEnum):
    GOOD_1 = auto()
    GOOD_2 = auto()
    GOOD_3 = auto()
    BAD_1 = auto()
    BAD_2 = auto()
    BAD_3 = auto()

FOOD_COLOR_MAP = {
    FoodTypeEnum.GOOD_1: "#009688",
    FoodTypeEnum.GOOD_2: "#009688",
    FoodTypeEnum.GOOD_3: "#009688",
    FoodTypeEnum.BAD_1: "#FF1744",
    FoodTypeEnum.BAD_2: "#FF1744",
    FoodTypeEnum.BAD_3: "#FF1744"
}
FOOD_LV1_SIZE = 30
FOOD_LV2_SIZE = 40
FOOD_LV3_SIZE = 50

# path of assets
ASSET_PATH = path.join(path.dirname(__file__), "..", "asset")
LEVEL_PATH = path.join(path.dirname(__file__), "..", "levels")
SOUND_PATH = path.join(path.dirname(__file__), "..", "asset", "sounds")
MUSIC_PATH = path.join(path.dirname(__file__), "..", "asset", "music")


