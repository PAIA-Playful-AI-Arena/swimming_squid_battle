import pygame.sprite

from games.easy_game.src.env import BALL_COLOR, BALL_VEL, BALL_H, BALL_W
from games.easy_game.src.foods import Food
from mlgame.view.view_model import create_rect_view_data


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.origin_image = pygame.Surface([BALL_W, BALL_H])
        self.image = self.origin_image
        self.color = BALL_COLOR
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.score = 0
        self.vel = BALL_VEL
        # TODO refactor score
        # TODO add velocity and size in Ball


    def update(self, motion):
        # for motion in motions:
        if motion == "UP":
            self.rect.centery -= self.vel
        elif motion == "DOWN":
            self.rect.centery += self.vel
        elif motion == "LEFT":
            self.rect.centerx -= self.vel
            # self.angle += 5
        elif motion == "RIGHT":
            self.rect.centerx += self.vel
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


