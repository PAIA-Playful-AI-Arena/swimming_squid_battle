import random

import pygame.sprite
from pygame import Rect

from .env import FoodTypeEnum, FOOD_COLOR_MAP, FOOD_LV1_SIZE, FOOD_LV2_SIZE, FOOD_LV3_SIZE
from mlgame.view.view_model import create_rect_view_data, create_image_view_data

FOOD1_VEL = 1
FOOD2_VEL = 2
FOOD3_VEL = 4


class Food(pygame.sprite.Sprite):
    def __init__(self, group, type: FoodTypeEnum, image_id: str, image_size=None, score: int = 1):
        pygame.sprite.Sprite.__init__(self, group)
        if image_size is None:
            image_size = [FOOD_LV1_SIZE, FOOD_LV1_SIZE]
        self.image = pygame.Surface(image_size)
        self.type = type
        self.score = score
        self.rect = self.image.get_rect()
        self.angle = 0
        self.rect_float_x = 0
        self.rect_float_y = 0
        self.image_id = image_id

    def update(self, *args, **kwargs) -> None:
        pass

    @property
    def game_object_data(self):
        return create_image_view_data(
            self.image_id,
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height,
        )

    def set_center_x_and_y(self, x: int, y: int):
        self.rect.centerx = x
        self.rect.centery = y
        self.rect_float_x = self.rect.centerx
        self.rect_float_y = self.rect.centery


class Food1(Food):
    def __init__(self, group):
        super().__init__(group,FoodTypeEnum.FOOD_1,"food01",[FOOD_LV1_SIZE, FOOD_LV1_SIZE],
                         1)
        self._vel = FOOD1_VEL

    def update(self, playground: Rect, squid: pygame.sprite.Sprite):

        self.rect_float_x += self._vel
        self.rect_float_y += random.choice([-0.3, -0.5, -0.7, 0, 0.3, 0.5, 0.7])
        self.rect.centerx = self.rect_float_x
        self.rect.centery = self.rect_float_y

        if self.rect.left < playground.left and self._vel < 0.0:
            self._vel = FOOD1_VEL
        elif self.rect.right > playground.right and self._vel > 0.0:
            self._vel = - FOOD1_VEL


class Food2(Food):
    def __init__(self, group):
        super().__init__(group, FoodTypeEnum.FOOD_2, "food02", [FOOD_LV2_SIZE, FOOD_LV2_SIZE], 2)
        self._vel = FOOD2_VEL


    def update(self, playground: Rect, squid: pygame.sprite.Sprite):

        self.rect_float_x += self._vel
        self.rect_float_y += random.choice([-0.5, -0.7, -1, -1.3, 0, 1, 1.3, 0.3, 0.5, 0.7])
        self.rect.centerx = self.rect_float_x
        self.rect.centery = self.rect_float_y

        if self.rect.left < playground.left and self._vel < 0.0:
            self._vel = FOOD2_VEL
        elif self.rect.right > playground.right and self._vel > 0.0:
            self._vel = - FOOD2_VEL


class Food3(Food):
    def __init__(self, group):
        super().__init__(group, FoodTypeEnum.FOOD_3, "food03", [FOOD_LV3_SIZE, FOOD_LV3_SIZE], 4)
        self._vel = FOOD3_VEL

    def update(self, playground: Rect, squid: pygame.sprite.Sprite):

        self.rect_float_x += self._vel
        self.rect_float_y += random.choice([-0.7, -1, -1.3, -1.7, 0, 1.7, 1, 1.3, 0.3, 0.7])
        self.rect.centerx = self.rect_float_x
        self.rect.centery = self.rect_float_y

        if self.rect.left < playground.left and self._vel < 0.0:
            self._vel = FOOD3_VEL
        elif self.rect.right > playground.right and self._vel > 0.0:
            self._vel = - FOOD3_VEL


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
