import copy
import json
import os.path

import pygame

from mlgame.game.paia_game import PaiaGame, GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.decorator import check_game_progress, check_game_result
from mlgame.view.view_model import *
from .env import *
from .foods import *
from .game_object import Ball
from .sound_controller import SoundController


def revise_ball(ball: Ball, playground: pygame.Rect):
    ball_rect = copy.deepcopy(ball.rect)
    if ball_rect.left < playground.left:
        ball_rect.left = playground.left
    elif ball_rect.right > playground.right:
        ball_rect.right = playground.right

    if ball_rect.top < playground.top:
        ball_rect.top = playground.top
    elif ball_rect.bottom > playground.bottom:
        ball_rect.bottom = playground.bottom
    ball.rect = ball_rect
    pass


class EasyGame(PaiaGame):
    """
    This is a Interface of a game
    """

    def __init__(
            self,
            level: int = -1,
            level_file: str = "",
            sound: str = "off",
            *args, **kwargs):
        super().__init__(user_num=1)
        self.game_result_state = GameResultState.FAIL
        self.scene = Scene(width=WIDTH, height=HEIGHT, color=BG_COLOR, bias_x=0, bias_y=0)
        self._level = level
        self._level_file = level_file
        self.foods = pygame.sprite.Group()
        self.sound_controller = SoundController(sound)

        self._init_game()


    def _init_game_by_file(self, level_file_path: str):
        try:
            with open(level_file_path) as f:
                game_params = json.load(f)
        except:
            # If the file doesn't exist, use default parameters
            print("此關卡檔案不存在，遊戲將會會自動使用第一關檔案 001.json。")
            print("This level file is not existed , game will load 001.json automatically.")
            with open(os.path.join(LEVEL_PATH, "001.json")) as f:
                game_params = json.load(f)
                self._level = 1
                self._level_file = None
        finally:
            # set game params
            self._playground_w = int(game_params["playground_size"][0])
            self._playground_h = int(game_params["playground_size"][1])
            self.playground = pygame.Rect(
                0, 0,
                self._playground_w,
                self._playground_h
            )
            self._good_food_count = game_params["good_food_count"]
            self._bad_food_count = game_params["bad_food_count"]
            self._score_to_pass = int(game_params["score_to_pass"])
            self._frame_limit = int(game_params["time_to_play"])
            self.playground.center = (WIDTH / 2, HEIGHT / 2)

            # init game
            self.ball = Ball()
            self.foods.empty()

            if not isinstance(self._good_food_count,list) or len(self._good_food_count)<3:
                raise Exception("你的關卡檔案格式有誤，請在'good_food_count' 欄位後面填入一個長度為3的陣列，舉例： [1,2,3]")
            elif not isinstance(self._bad_food_count, list) or len(self._bad_food_count) < 3:
                raise Exception("你的關卡檔案格式有誤，請在'bad_food_count' 欄位後面填入一個長度為3的陣列，舉例： [1,2,3]")

            else:
                self._create_foods(GoodFoodLv1, self._good_food_count[0])
                self._create_foods(GoodFoodLv2, self._good_food_count[1])
                self._create_foods(GoodFoodLv3, self._good_food_count[2])
                self._create_foods(BadFoodLv1, self._bad_food_count[0])
                self._create_foods(BadFoodLv2, self._bad_food_count[1])
                self._create_foods(BadFoodLv3, self._bad_food_count[2])

            self.frame_count = 0
            self._frame_count_down = self._frame_limit
            self.sound_controller.play_music()



    def update(self, commands):
        # handle command
        ai_1p_cmd = commands[get_ai_name(0)]
        if ai_1p_cmd is not None:
            action = ai_1p_cmd[0]
        else:
            action = "NONE"

        self.ball.update(action)
        revise_ball(self.ball, self.playground)
        # update sprite
        self.foods.update()

        # handle collision

        self._check_foods_collision()
        # self._timer = round(time.time() - self._begin_time, 3)

        self.frame_count += 1
        self._frame_count_down = self._frame_limit - self.frame_count
        # self.draw()

        if not self.is_running:
            return "RESET"

    def _check_foods_collision(self):
        hits = pygame.sprite.spritecollide(self.ball, self.foods, True)
        if hits:
            for food in hits:
                # self.ball.score += food.score
                # growth play special sound
                self.ball.eat_food_and_change_level_and_play_sound(food,self.sound_controller)
                self._create_foods(food.__class__, 1)
                if isinstance(food, (GoodFoodLv1,GoodFoodLv2,GoodFoodLv3,)):
                    self.sound_controller.play_eating_good()
                elif isinstance(food, (BadFoodLv1,BadFoodLv2,BadFoodLv3,)):
                    self.sound_controller.play_eating_bad()

    def get_data_from_game_to_player(self):
        """
        send something to game AI
        we could send different data to different ai
        """
        to_players_data = {}
        foods_data = []
        for food in self.foods:
            # TODO 確認要提供中心點座標還是左上角座標。
            foods_data.append({"x": food.rect.x, "y": food.rect.y, "type": food.type, "score": food.score})

        data_to_1p = {
            "frame": self.frame_count,
            # TODO 確認要提供中心點座標還是左上角座標。
            "player_x": self.ball.rect.centerx,
            "player_y": self.ball.rect.centery,
            "player_size":self.ball.rect.width,
            "player_vel":self.ball.vel,
            "foods": foods_data,

            "score": self.ball.score,
            "score_to_pass":self._score_to_pass,
            "status": self.get_game_status()

        }

        to_players_data[get_ai_name(0)] = data_to_1p
        # should be equal to config. GAME_SETUP["ml_clients"][0]["name"]

        return to_players_data

    def get_game_status(self):

        if self.is_running:
            status = GameStatus.GAME_ALIVE
        elif self.is_passed:
            status = GameStatus.GAME_PASS
        else:
            status = GameStatus.GAME_OVER
        return status

    def reset(self):

        if self.is_passed:
            self._level += 1
            self.sound_controller.play_cheer()

        self._init_game()



        pass

    def _init_game(self):
        if path.isfile(self._level_file):
            # set by injected file
            self._init_game_by_file(self._level_file)
            pass
        else:
            level_file_path = os.path.join(LEVEL_PATH, f"{self._level:03d}.json")
            self._init_game_by_file(level_file_path)

    @property
    def is_passed(self):
        return self.ball.score > self._score_to_pass

    @property
    def is_running(self):
        return self.frame_count < self._frame_limit

    def get_scene_init_data(self):
        """
        Get the initial scene and object information for drawing on the web
        """
        # bg_path = path.join(ASSET_PATH, "img/background.jpg")
        # background = create_asset_init_data(
        #     "background", WIDTH, HEIGHT, bg_path,
        #     github_raw_url="https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/easy_game/main/asset/img/background.jpg")
        scene_init_data = {"scene": self.scene.__dict__,
                           "assets": [
                               # background
                           ],
                           # "audios": {}
                           }
        return scene_init_data

    @check_game_progress
    def get_scene_progress_data(self):
        """
        Get the position of game objects for drawing on the web
        """
        foods_data = []
        for food in self.foods:
            foods_data.append(food.game_object_data)
        game_obj_list = [self.ball.game_object_data]
        game_obj_list.extend(foods_data)
        backgrounds = [
            # create_image_view_data("background", 0, 0, WIDTH, HEIGHT),
            create_rect_view_data(
                "playground", self.playground.x, self.playground.y,
                self.playground.w, self.playground.h, PG_COLOR)
        ]
        foregrounds = [

        ]
        toggle_objs = [
            create_text_view_data(f"Score:{self.ball.score:04d}", 600, 50, "#A5D6A7", "24px Arial BOLD"),
            create_text_view_data(f" Next:{self._score_to_pass:04d}", 600, 100, "#FF4081", "24px Arial BOLD"),
            create_text_view_data(f" Time:{self._frame_count_down:04d}", 600, 150, "#FF5722", "24px Arial BOLD"),

        ]
        scene_progress = create_scene_progress_data(frame=self.frame_count, background=backgrounds,
                                                    object_list=game_obj_list,
                                                    foreground=foregrounds, toggle=toggle_objs)
        return scene_progress

    @check_game_result
    def get_game_result(self):
        """
        send game result
        """
        if self.get_game_status() == GameStatus.GAME_PASS:
            self.game_result_state = GameResultState.FINISH
        return {"frame_used": self.frame_count,
                "state": self.game_result_state,
                "attachment": [
                    {
                        "player": get_ai_name(0),
                        "rank": 1,
                        "score": self.ball.score,
                        "passed": self.is_passed
                    }
                ]

                }

    def get_keyboard_command(self):
        """
        Define how your game will run by your keyboard
        """
        cmd_1p = []
        key_pressed_list = pygame.key.get_pressed()
        if key_pressed_list[pygame.K_UP]:
            cmd_1p.append("UP")
        elif key_pressed_list[pygame.K_DOWN]:
            cmd_1p.append("DOWN")
        elif key_pressed_list[pygame.K_LEFT]:
            cmd_1p.append("LEFT")
        elif key_pressed_list[pygame.K_RIGHT]:
            cmd_1p.append("RIGHT")
        else:
            cmd_1p.append("NONE")
        return {get_ai_name(0): cmd_1p}

    def _create_foods(self, FOOD_TYPE, count: int = 5):
        for i in range(count):
            # add food to group
            food = FOOD_TYPE(self.foods)
            food.rect.centerx = random.randint(self.playground.left, self.playground.right)
            food.rect.centery = random.randint(self.playground.top, self.playground.bottom)
        pass
