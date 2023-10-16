import pygame.sprite

from .env import FoodTypeEnum, FOOD_COLOR_MAP, FOOD_LV1_SIZE, FOOD_LV2_SIZE, FOOD_LV3_SIZE
from mlgame.view.view_model import create_rect_view_data


class Food(pygame.sprite.Sprite):
    def __init__(self, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface([8, 8])
        self.type = None
        self.score = 0
        self.color = None

        self.rect = self.image.get_rect()
        self.angle = 0

    def update(self) -> None:
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
