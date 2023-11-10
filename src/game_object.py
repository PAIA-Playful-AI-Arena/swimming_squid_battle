import math

from typing import List

import pydantic
import pygame.sprite

from .env import SQUID_VEL, SQUID_H, SQUID_W, SQUID_GROWTH_SCORE_STEP, SQUID_GROWTH_SIZE_STEP, \
    SQUID_SIZE_W_MAX, SQUID_GROWTH_VEL_STEP, SQUID_VEL_MAX, SQUID_SIZE_W_MIN, SQUID_VEL_MIN
from .foods import Food
from .sound_controller import SoundController
from mlgame.view.view_model import create_rect_view_data, create_image_view_data


class LevelParams(pydantic.BaseModel):
    # TODO max w 700 and min 100
    # TODO max h 600 and min 100
    playground_size_w: int = 300
    playground_size_h: int = 300
    score_to_pass: int = 10
    time_to_play: int = 300

    food_1: int = 3
    food_2: int = 0
    food_3: int = 0
    garbage_1: int = 0
    garbage_2: int = 0
    garbage_3: int = 0


# level_thresholds = [10, 15, 20, 25, 30]
LEVEL_THRESHOLDS = [10, 30, 60, 100, 150]
LEVEL_PROPERTIES = {
    1: {'size_ratio': 1.0, 'vel': 10},
    2: {'size_ratio': 1.2, 'vel': 12},
    3: {'size_ratio': 1.4, 'vel': 15},
    4: {'size_ratio': 1.6, 'vel': 18},
    5: {'size_ratio': 1.8, 'vel': 21},
    6: {'size_ratio': 2.0, 'vel': 25},
}


class Squid(pygame.sprite.Sprite):
    ANGLE_TO_RIGHT = math.radians(-10)
    ANGLE_TO_LEFT = math.radians(10)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.origin_image = pygame.Surface([SQUID_W, SQUID_H])
        self.image = self.origin_image
        self.rect = self.image.get_rect()
        self.rect.center = (350, 300)
        self._score = 0
        self._vel = SQUID_VEL
        self._lv = 1
        self.angle = 0

    def update(self, motion):
        # for motion in motions:
        if motion == "UP":
            self.rect.centery -= self._vel
        elif motion == "DOWN":
            self.rect.centery += self._vel
        elif motion == "LEFT":
            self.rect.centerx -= self._vel
            self.angle = self.ANGLE_TO_LEFT
        elif motion == "RIGHT":
            self.rect.centerx += self._vel
            self.angle = self.ANGLE_TO_RIGHT
        else:
            self.angle = 0
        # self.image = pygame.transform.rotate(self.origin_image, self.angle)
        # print(self.angle)
        # center = self.rect.center
        # self.rect = self.image.get_rect()
        # self.rect.center = center

    @property
    def game_object_data(self):

        return create_image_view_data(
            "squid",
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height,
            self.angle

        )

    def eat_food_and_change_level_and_play_sound(self, food: Food, sound_controller: SoundController):
        self._score += food.score
        new_lv = get_current_level(self._score)
        self.rect.width = SQUID_W * LEVEL_PROPERTIES[new_lv]['size_ratio']
        self.rect.height = SQUID_H * LEVEL_PROPERTIES[new_lv]['size_ratio']

        self._vel = LEVEL_PROPERTIES[new_lv]['vel']
        if new_lv > self._lv:
            sound_controller.play_lv_up()
        elif new_lv < self._lv:
            sound_controller.play_lv_down()
        self._lv = new_lv
        pass

    @property
    def score(self):
        return self._score

    @property
    def vel(self):
        return self._vel


def get_current_level(score: int) -> int:
    """
    Determines the current level based on the player's score.

    :param score: int - The current score of the player.
    :return: int - The current level of the player.
    """

    for level, threshold in enumerate(LEVEL_THRESHOLDS, start=1):
        if score < threshold:
            return level
    return len(LEVEL_THRESHOLDS) + 1  # Return the next level if score is beyond all thresholds
