import random

import pygame.sprite
from pygame import Rect

from .env import FoodTypeEnum, FOOD_COLOR_MAP, FOOD_LV1_SIZE, FOOD_LV2_SIZE, FOOD_LV3_SIZE
from mlgame.view.view_model import create_rect_view_data

FOOD1_VEL = 1


class Food(pygame.sprite.Sprite):
    def __init__(self, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface([8, 8])
        self.type = None
        self.score = 0
        self.color = None

        self.rect = self.image.get_rect()
        self.angle = 0

    def set_center_x_and_y(self, x: int, y: int):
        self.rect.centerx = x
        self.rect.centery = y

    def update(self, *args, **kwargs) -> None:
        pass

    @property
    def game_object_data(self):
        return create_rect_view_data(
            "food",
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height,
            self.color
        )


class GoodFoodLv1(Food):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.Surface([FOOD_LV1_SIZE, FOOD_LV1_SIZE])
        self.type = FoodTypeEnum.GOOD_1
        self.color = FOOD_COLOR_MAP[self.type]
        self.score = 1
        self.rect = self.image.get_rect()


class GoodFoodLv2(Food):
    def __init__(self, group):
        super().__init__(group)

        self.image = pygame.Surface([FOOD_LV2_SIZE, FOOD_LV2_SIZE])
        self.type = FoodTypeEnum.GOOD_2
        self.color = FOOD_COLOR_MAP[self.type]
        self.score = 2
        self.rect = self.image.get_rect()


class GoodFoodLv3(Food):
    def __init__(self, group):
        super().__init__(group)

        self.image = pygame.Surface([FOOD_LV3_SIZE, FOOD_LV3_SIZE])
        self.type = FoodTypeEnum.GOOD_3
        self.color = FOOD_COLOR_MAP[self.type]
        self.score = 4
        self.rect = self.image.get_rect()


class Food1(Food):
    def __init__(self, group):
        super().__init__(group)

        self.image = pygame.Surface([FOOD_LV1_SIZE, FOOD_LV1_SIZE])
        self.type = FoodTypeEnum.GOOD_1
        self.color = FOOD_COLOR_MAP[self.type]
        self.score = 1
        self.rect = self.image.get_rect()
        self.rect_float_x = 0
        self.rect_float_y = 0
        self._vel = FOOD1_VEL
    def set_center_x_and_y(self, x: int, y: int):
        self.rect.centerx = x
        self.rect.centery = y
        self.rect_float_x = self.rect.centerx
        self.rect_float_y = self.rect.centery

    def update(self, playground: Rect, squid: pygame.sprite.Sprite):

        self.rect_float_x += self._vel
        self.rect_float_y += random.choice([-0.3,-0.5,-0.7,0,0.3,0.5,0.7])
        self.rect.centerx = self.rect_float_x
        self.rect.centery = self.rect_float_y

        if self.rect.left < playground.left and self._vel < 0.0:
            self._vel = FOOD1_VEL
        elif self.rect.right > playground.right and self._vel>0.0:
            self._vel = - FOOD1_VEL



class BadFoodLv1(Food):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.Surface([FOOD_LV1_SIZE, FOOD_LV1_SIZE])
        self.type = FoodTypeEnum.BAD_1
        self.color = FOOD_COLOR_MAP[self.type]
        self.score = -1
        self.rect = self.image.get_rect()
        self.angle = 0


class BadFoodLv2(Food):
    def __init__(self, group):
        super().__init__(group)

        self.image = pygame.Surface([FOOD_LV2_SIZE, FOOD_LV2_SIZE])
        self.type = FoodTypeEnum.BAD_2
        self.color = FOOD_COLOR_MAP[self.type]
        self.score = -2
        self.rect = self.image.get_rect()


class BadFoodLv3(Food):
    def __init__(self, group):
        super().__init__(group)

        self.image = pygame.Surface([FOOD_LV3_SIZE, FOOD_LV3_SIZE])
        self.type = FoodTypeEnum.BAD_3
        self.color = FOOD_COLOR_MAP[self.type]
        self.score = -4
        self.rect = self.image.get_rect()
