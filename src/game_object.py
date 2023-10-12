import math

import pygame.sprite

from games.easy_game.src.env import BALL_COLOR, BALL_VEL, BALL_H, BALL_W, BALL_GROWTH_SCORE_STEP, BALL_GROWTH_SIZE_STEP, \
    BALL_SIZE_MAX, BALL_GROWTH_VEL_STEP, BALL_VEL_MAX, BALL_SIZE_MIN, BALL_VEL_MIN
from games.easy_game.src.foods import Food
from games.easy_game.src.sound_controller import SoundController
from mlgame.view.view_model import create_rect_view_data


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.origin_image = pygame.Surface([BALL_W, BALL_H])
        self.image = self.origin_image
        self.color = BALL_COLOR
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self._score = 0
        self._vel = BALL_VEL
        self._lv =1

    def update(self, motion):
        # for motion in motions:
        if motion == "UP":
            self.rect.centery -= self._vel
        elif motion == "DOWN":
            self.rect.centery += self._vel
        elif motion == "LEFT":
            self.rect.centerx -= self._vel
            # self.angle += 5
        elif motion == "RIGHT":
            self.rect.centerx += self._vel
            # self.angle -= 5

        # self.image = pygame.transform.rotate(self.origin_image, self.angle)
        # print(self.angle)
        # center = self.rect.center
        # self.rect = self.image.get_rect()
        # self.rect.center = center

    @property
    def game_object_data(self):
        return create_rect_view_data(
            "ball",
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height,
            self.color
        )

    def eat_food_and_change_level_and_play_sound(self, food: Food,sound_controller:SoundController):
        self._score += food.score
        new_lv = math.ceil((self._score + 1) / BALL_GROWTH_SCORE_STEP)
        self.rect.width = max(BALL_SIZE_MIN,min(BALL_W + new_lv * BALL_GROWTH_SIZE_STEP, BALL_SIZE_MAX))
        self.rect.height = max(BALL_SIZE_MIN,min(BALL_H + new_lv * BALL_GROWTH_SIZE_STEP, BALL_SIZE_MAX))
        self._vel = max(BALL_VEL_MIN,min(BALL_VEL + new_lv * BALL_GROWTH_VEL_STEP, BALL_VEL_MAX))
        if new_lv > self._lv:
            sound_controller.play_lv_up()
        elif new_lv < self._lv:
            sound_controller.play_lv_down()
        self._lv=new_lv
        pass

    @property
    def score(self):
        return self._score
    @property
    def vel(self):
        return self._vel