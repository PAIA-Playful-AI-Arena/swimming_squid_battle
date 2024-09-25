import math
import random

import pydantic
import pygame.sprite
from pydantic import validator, BaseModel

from mlgame.view.view_model import create_image_view_data, create_text_view_data
from .env import *
from .foods import Food


class LevelParams(pydantic.BaseModel):
    playground_size_w: int = 300
    playground_size_h: int = 300
    score_to_pass: int = 10
    time_to_play: int = 300

    food_1: int = 3
    food_1_max: int = 3
    food_2: int = 0
    food_2_max: int = 0
    food_3: int = 0
    food_3_max: int = 0
    garbage_1: int = 0
    garbage_1_max: int = 0
    garbage_2: int = 0
    garbage_2_max: int = 0
    garbage_3: int = 0
    garbage_3_max: int = 0
    # 補充給玩家需要的資訊
    left: int = -1
    right: int = -1
    top: int = -1
    bottom: int = -1

    @validator('playground_size_w', pre=True)
    def validate_playground_size_w(cls, value):
        min_size = 100
        max_size = 650
        if value < min_size:
            return min_size
        if value > max_size:
            return max_size
        return value

    @validator('playground_size_h', pre=True)
    def validate_playground_size_h(cls, value):
        min_size = 100
        max_size = 550
        if value < min_size:
            return min_size
        if value > max_size:
            return max_size
        return value


# level_thresholds = [10, 15, 20, 25, 30]


class Squid(pygame.sprite.Sprite):
    ANGLE_TO_RIGHT = math.radians(-10)
    ANGLE_TO_LEFT = math.radians(10)

    def __init__(self, ai_id, x, y):
        pygame.sprite.Sprite.__init__(self)

        self._ai_num = ai_id
        self._img_id = f"squid{self._ai_num}"

        self.origin_image = pygame.Surface([SQUID_W, SQUID_H])
        self.image = self.origin_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self._score = 0
        self._vel = LEVEL_PROPERTIES[1]['vel']
        self._lv = 1
        self.rank = 1
        self.angle = 0
        self._last_collision = 0
        self._collision_dir = None
        self._motion = None

    def update(self, frame, motion):
        # for motion in motions:
        self._motion = motion
        if frame - self._last_collision <= 3:
            # 反彈
            if self._collision_dir == "UP":
                self.rect.centery += self._vel
            elif self._collision_dir == "DOWN":
                self.rect.centery -= self._vel
            elif self._collision_dir == "LEFT":
                self.rect.centerx += self._vel
                self.angle = self.ANGLE_TO_RIGHT
            elif self._collision_dir == "RIGHT":
                self.rect.centerx -= self._vel
                self.angle = self.ANGLE_TO_LEFT
            else:
                self.angle = 0
            return 0
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
        if frame - self._last_collision > 30 and self._img_id == f"squid{self._ai_num}-hurt":
            self._img_id = f"squid{self._ai_num}"

        # self.image = pygame.transform.rotate(self.origin_image, self.angle)
        # print(self.angle)
        # center = self.rect.center
        # self.rect = self.image.get_rect()
        # self.rect.center = center

    @property
    def game_object_data(self):
        return create_image_view_data(
            self._img_id,
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height,
            self.angle

        )

    def eat_food_and_change_level_and_play_sound(self, food: Food, sounds: list):
        self._score += food.score
        new_lv = get_current_level(self._score)

        if new_lv > self._lv:
            sounds.append(LV_UP_OBJ)
        elif new_lv < self._lv:
            sounds.append(LV_DOWN_OBJ)
        if new_lv != self._lv:
            self.rect.width = SQUID_W * LEVEL_PROPERTIES[new_lv]['size_ratio']
            self.rect.height = SQUID_H * LEVEL_PROPERTIES[new_lv]['size_ratio']
            self._vel = LEVEL_PROPERTIES[new_lv]['vel']
            self._lv = new_lv

    def collision_between_squids(self, collision_score, frame, sounds: list):
        if frame - self._last_collision > 3:
            self._score += collision_score
            self._last_collision = frame
            sounds.append(COLLISION_OBJ)

            if self._motion != "NONE":
                self._collision_dir = self._motion
            else:
                self._collision_dir = random.choice(["UP", "DOWN", "RIGHT", "LEFT"])

            if collision_score < 0:
                self._img_id = f"squid{self._ai_num}-hurt"

        new_lv = get_current_level(self._score)

        if new_lv > self._lv:
            sounds.append(LV_UP_OBJ)

        elif new_lv < self._lv:
            sounds.append(LV_DOWN_OBJ)
        if new_lv != self._lv:
            self.rect.width = SQUID_W * LEVEL_PROPERTIES[new_lv]['size_ratio']
            self.rect.height = SQUID_H * LEVEL_PROPERTIES[new_lv]['size_ratio']
            self._vel = LEVEL_PROPERTIES[new_lv]['vel']
            self._lv = new_lv

    @property
    def score(self):
        return self._score

    @property
    def vel(self):
        return self._vel

    @property
    def lv(self):
        return self._lv


def get_current_level(score: int) -> int:
    """
    Determines the current level based on the player's score.

    :param score: int - The current score of the player.
    :return: int - The current level of the player.
    """

    for level, threshold in enumerate(LEVEL_THRESHOLDS, start=1):
        if score < threshold:
            return min(level, 6)
    return len(LEVEL_THRESHOLDS)  # Return the next level if score is beyond all thresholds


class ScoreText(pygame.sprite.Sprite):
    def __init__(self, text, color, x, y, groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.rect = pygame.Rect(x, y, SQUID_W, SQUID_H)
        self.rect.center = (x, y)
        self._text = text
        self._color = color
        self._live_frame = 15

    def update(self):
        self._live_frame -= 1
        self.rect.centery -= 3
        if self._live_frame <= 0:
            self.kill()

    @property
    def game_object_data(self):
        return create_text_view_data(
            self._text, self.rect.centerx, self.rect.centery, self._color,
            "24px Arial BOLD")


class CryingStar(pygame.sprite.Sprite):
    def __init__(self, x, y, groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.rect = pygame.Rect(x, y, SQUID_H, SQUID_H)
        self.rect.center = (x, y)

        self._live_frame = 15

    def update(self):
        self._live_frame -= 1
        self.rect.centery -= 5

        if self._live_frame <= 0:
            self.kill()

    @property
    def game_object_data(self):
        return create_image_view_data(
            f"star",
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height,
            angle=0.1

        )


class WindowConfig(BaseModel):
    left: int
    right: int
    top: int
    bottom: int