import math


from typing import List

import pydantic
import pygame.sprite

from .env import  SQUID_VEL, SQUID_H, SQUID_W, SQUID_GROWTH_SCORE_STEP, SQUID_GROWTH_SIZE_STEP, \
    SQUID_SIZE_MAX, SQUID_GROWTH_VEL_STEP, SQUID_VEL_MAX, SQUID_SIZE_MIN, SQUID_VEL_MIN
from .foods import Food
from .sound_controller import SoundController
from mlgame.view.view_model import create_rect_view_data, create_image_view_data


class LevelParams(pydantic.BaseModel):
    # TODO max and min
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


class Squid(pygame.sprite.Sprite):
    ANGLE_TO_RIGHT = math.radians(-10)
    ANGLE_TO_LEFT = math.radians(10)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.origin_image = pygame.Surface([SQUID_W, SQUID_H])
        self.image = self.origin_image
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self._score = 0
        self._vel = SQUID_VEL
        self._lv = 1
        self.angle =0
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
        new_lv = math.ceil((self._score - SQUID_GROWTH_SCORE_STEP + 1) / SQUID_GROWTH_SCORE_STEP)
        self.rect.width = max(SQUID_SIZE_MIN, min(SQUID_W + new_lv * SQUID_GROWTH_SIZE_STEP, SQUID_SIZE_MAX))
        self.rect.height = max(SQUID_SIZE_MIN, min(SQUID_H + new_lv * SQUID_GROWTH_SIZE_STEP, SQUID_SIZE_MAX))
        self._vel = max(SQUID_VEL_MIN, min(SQUID_VEL + new_lv * SQUID_GROWTH_VEL_STEP, SQUID_VEL_MAX))
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
