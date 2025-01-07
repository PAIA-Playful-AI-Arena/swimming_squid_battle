import copy
from enum import Enum
import os.path

import pandas as pd
import pygame

from mlgame.game.paia_game import PaiaGame, GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.audio_model import create_music_init_data, create_sound_init_data, MusicProgressSchema
from mlgame.view.decorator import check_game_progress, check_game_result, check_scene_init_data
from mlgame.view.view_model import *
from .foods import *
from .game_object import Squid, LevelParams, ScoreText, CryingStar, WindowConfig

FOOD_LIST = [Food1, Food2, Food3, Garbage1, Garbage2, Garbage3]
class RunningState(Enum):
    OPENING = 0
    TRANSITION = 1
    ENDING = 2
    PLAYING = 3
    RESET = 4
class EndingState():
    def __init__(self):
        self.frame_count = 0
        self._info_text = {}
        self._sound = [PASS_OBJ]
        self._reset()
    def update(self,result):
        self._info_text["content"] = result
        if self.frame_count == 0:
            self._sound = [PASS_OBJ]
        else:
            self._sound = []
        
        if 0 < self.frame_count < 30:
            self._info_text["y"] +=10 
        elif 30 <= self.frame_count < 60:
            pass
        elif 60 <= self.frame_count < 90:
            self._info_text["y"] +=10 
        elif 90 <= self.frame_count:
            self._reset()
            return RunningState.RESET
        self.frame_count += 1
        return RunningState.ENDING
    def get_scene_progress_data(self):
        return create_scene_progress_data(
            frame=self.frame_count, 
            background=[], 
            object_list=[self._info_text], 
            foreground=[], 
            toggle=[], 
            musics=[], sounds=self._sound
            )
    def _reset(self):
        self.frame_count = 0
        self._info_text = create_text_view_data("Ending", 130, 0, "#EEEEEE", "64px Consolas BOLD")
        self._sound = [PASS_OBJ]

class TransitionState():
    def __init__(self):
        self.frame_count = 0
        self._info_text = {}
        self._sound = [PASS_OBJ]
        self._reset()
    def update(self,p1_score,p2_score):
        text = f"1P: {p1_score} vs 2P: {p2_score}"
        self._info_text["content"] = text
        if self.frame_count == 0:
            self._sound = [PASS_OBJ]
        else:
            self._sound = []

        if self.frame_count < 30:
            self._info_text["y"] += 10
        elif 30 <= self.frame_count < 60:
            pass
        elif 60 <= self.frame_count < 90:
            self._info_text["y"] += 10
        elif self.frame_count ==90:
            self._sound=[PASS_OBJ]
        elif 91 <= self.frame_count:
            self._reset()
            return RunningState.PLAYING
        self.frame_count += 1
        return RunningState.TRANSITION
    def get_scene_progress_data(self):
        return create_scene_progress_data(
            frame=self.frame_count, 
            background=[], 
            object_list=[self._info_text], 
            foreground=[], 
            toggle=[], 
            musics=[], sounds=self._sound
            )
    def _reset(self):
        self.frame_count = 0
        self._info_text = create_text_view_data("Ready", 230, 0, "#EEEEEE", "64px Consolas BOLD")
        self._sound.append(PASS_OBJ)


class OpeningState():
    def __init__(self):
        self.frame_count = 0
        self._ready_text = create_text_view_data("Ready", 300, 300, "#EEEEEE", "64px Consolas BOLD")
        self._go_text = create_text_view_data("Go! ", -300, -360, "#EEEEEE", "64px Consolas BOLD")
    def update(self):
        if self.frame_count < 30:
            self._ready_text["content"] = "Ready "+"."*(self.frame_count%5)
            # self._ready_text["x"] += 10
        elif 30 <= self.frame_count < 60:
            self._ready_text["content"] = "Ready"
            
            self._go_text = create_text_view_data("Fight! ", 320, 360, "#EEEEEE", "64px Consolas BOLD")

        elif 60 <= self.frame_count < 90:
            self._ready_text["x"] += 30
            self._go_text["x"] -= 30
        elif 90 <= self.frame_count:
            self.frame_count=0
            self._reset()
            return RunningState.PLAYING
        self.frame_count += 1
        return RunningState.OPENING
        
    def get_scene_progress_data(self):
        return create_scene_progress_data(
            frame=self.frame_count, 
            background=[], 
            object_list=[self._ready_text, self._go_text], 
            foreground=[], 
            toggle=[], 
            musics=[], sounds=[]
            )

    def _reset(self):
        self.frame_count = 0
        self._ready_text = create_text_view_data("Ready", 300, 300, "#EEEEEE", "64px Consolas BOLD")
        self._go_text = create_text_view_data("Go! ", -300, -360, "#EEEEEE", "64px Consolas BOLD")

class SwimmingSquidBattle(PaiaGame):
    """
    This is a Interface of a game
    """

    def __init__(
            self,
            level: int = -1,
            level_file: str = "",
            game_times: int = 1,
            sound: str = "off",
            *args, **kwargs):
        super().__init__(user_num=1)
        self._new_food_frame = 0
        self._music = []
        self._status = GameStatus.GAME_ALIVE
        self._running_state = RunningState.OPENING
        self.game_result_state = GameResultState.FAIL
        self.scene = Scene(width=WIDTH, height=HEIGHT, color=BG_COLOR, bias_x=0, bias_y=0)
        self._level = level
        self._level_file = level_file
        self._used_file = ""
        self.foods = pygame.sprite.Group()
        self.squids = pygame.sprite.Group()
        self._help_texts = pygame.sprite.Group()
        self._sounds = []
        # self.sound_controller = SoundController(sound)
        self._overtime_count = 0
        self._game_times = game_times
        self._winner = []
        self._foods_num = []
        self._foods_max_num = []
        self._add_score = {"1P": 0, "2P": 0}
        self._game_params = {}
        self._current_round_num = 1
        self._record1 = {
            "player_num": get_ai_name(0),
        }
        self._record2 = {
            "player_num": get_ai_name(1),
        }
        self._last_collision = -30
        self._init_game()
        self._opening_state = OpeningState()
        self._transition_state = TransitionState()
        self._ending_state = EndingState()
    def _init_game_by_file(self, level_file_path: str):
        try:
            with open(level_file_path) as f:
                game_params = LevelParams(**json.load(f))
                self._used_file = level_file_path

        except:
            # If the file doesn't exist, use default parameters
            print("此關卡檔案不存在，遊戲將會會自動使用第一關檔案 001.json。")
            print("This level file is not existed , game will load 001.json automatically.")
            with open(os.path.join(LEVEL_PATH, "001.json")) as f:
                game_params = LevelParams(**json.load(f))
                self._level = 1
                self._level_file = ""
                self._used_file = "001.json"
        finally:
            # set game params
            self._foods_num = [game_params.food_1, game_params.food_2, game_params.food_3, game_params.garbage_1,
                               game_params.garbage_2, game_params.garbage_3]
            self._foods_max_num = [game_params.food_1_max, game_params.food_2_max, game_params.food_3_max,
                                   game_params.garbage_1_max,
                                   game_params.garbage_2_max, game_params.garbage_3_max]

            self.playground = pygame.Rect(
                0, 0,
                game_params.playground_size_w,
                game_params.playground_size_h
            )

            self._score_to_pass = game_params.score_to_pass
            self._frame_limit = game_params.time_to_play

            self.playground.center = ((WIDTH - WIDTH_OF_INFO) / 2, HEIGHT / 2)
            self._food_window = WindowConfig(
                left=self.playground.left, right=self.playground.right,
                top=self.playground.top, bottom=self.playground.bottom)
            self._garbage_window = WindowConfig(
                left=self.playground.left, right=self.playground.right,
                top=self.playground.top - 60, bottom=self.playground.top - 10)

            self._food_pos_list = []
            self._garbage_pos_list = []

            # init game
            self.squid1 = Squid(1, 200, 300)
            self.squid2 = Squid(2, 500, 300)
            self.squids.empty()
            self.squids.add(self.squid1)
            self.squids.add(self.squid2)
            self.foods.empty()
            for i in range(6):
                self._create_foods(FOOD_LIST[i], self._foods_num[i])

            self.frame_count = 0
            self._last_collision = -30
            self._frame_count_down = self._frame_limit
            self._new_food_frame = 0
            self._overtime_count = 0

            self._status = GameStatus.GAME_ALIVE
            game_params.left = self.playground.left
            game_params.right = self.playground.right
            game_params.bottom = self.playground.bottom
            game_params.top = self.playground.top
            self._game_params = game_params

            # change bgm
            self._music = [MusicProgressSchema(music_id=f"bgm0{(self._current_round_num - 1) % 3 + 1}").__dict__]

    
    def update(self, commands):
        # handle command
        # TODO add game state to decide to render opening or game
        if self._running_state == RunningState.OPENING:
            self._running_state = self._opening_state.update()
            self.frame_count += 1
        elif self._running_state == RunningState.TRANSITION:
            self._running_state = self._transition_state.update(self._winner.count("1P"), self._winner.count("2P"))
            self.frame_count += 1
        elif self._running_state == RunningState.ENDING:
            result = f"1P {self._winner.count('1P')} vs 2P {self._winner.count('2P')}"
            if self._winner.count("1P") > self._game_times / 2:  # 1P 贏
                result+="  1P win !"
                
            elif self._winner.count("2P") > self._game_times / 2:  # 2P 贏
                result+="  2P win!"

            self._running_state = self._ending_state.update(result)
            self.frame_count += 1
        elif self._running_state == RunningState.RESET:
            return "RESET"
        elif self._running_state == RunningState.PLAYING:
            
        
            ai_1p_cmd = commands[get_ai_name(0)]
            if ai_1p_cmd is not None:
                action_1 = ai_1p_cmd[0]
            else:
                action_1 = "NONE"

            ai_2p_cmd = commands[get_ai_name(1)]
            if ai_2p_cmd is not None:
                action_2 = ai_2p_cmd[0]
            else:
                action_2 = "NONE"

            self.squid1.update(self.frame_count, action_1)
            self.squid2.update(self.frame_count, action_2)
            revise_squid_coordinate(self.squid1, self.playground)
            revise_squid_coordinate(self.squid2, self.playground)
            # create new food
            if self.frame_count - self._new_food_frame > 150:
                for i in range(6):
                    if self._foods_max_num[i] > self._foods_num[i]:
                        self._foods_num[i] += 1
                        self._create_foods(FOOD_LIST[i], 1)
                self._new_food_frame = self.frame_count

            # update sprite
            self.foods.update(playground=self.playground, squid=self.squid1)
            self._help_texts.update()
            # handle collision

            self._check_foods_collision()
            # self._timer = round(time.time() - self._begin_time, 3)
            self._check_squids_collision()

            self.frame_count += 1
            self._frame_count_down = self._frame_limit - self.frame_count
            # self.draw()

            if not self.is_running:
                # 五戰三勝的情況下不能直接回傳，因此紀錄 winner 後，重啟遊戲
                self.update_winner()

                # if self.is_passed:
                #     self._sounds.append(PASS_OBJ)
                # else:
                #     self._sounds.append(FAIL_OBJ)

                status = GameStatus.GAME_ALIVE
                if self.squid1.score > self.squid2.score:
                    status = GameStatus.GAME_1P_WIN
                elif self.squid2.score > self.squid1.score:
                    status = GameStatus.GAME_2P_WIN
                else:
                    status = GameStatus.GAME_DRAW
                self._status = status

                if self._winner.count("1P") > self._game_times / 2:  # 1P 贏
                    print("玩家 1 獲勝！")
                    self._running_state = RunningState.ENDING
                    # return "RESET"
                elif self._winner.count("2P") > self._game_times / 2:  # 2P 贏

                    print("玩家 2 獲勝！")
                    self._running_state = RunningState.ENDING
                    # return "RESET"
                else:
                    self._current_round_num += 1
                    self._running_state = RunningState.TRANSITION
                    self._init_game()
                self._status = status
            else:
                self._status = GameStatus.GAME_ALIVE
                # return "RESET"

    def _check_foods_collision(self):
        hits = pygame.sprite.groupcollide(self.squids, self.foods, dokilla=False, dokillb=False)
        to_remove_foods = set()

        for squid, foods in hits.items():
            for food in foods:
                squid.eat_food_and_change_level_and_play_sound(food, self._sounds)
                to_remove_foods.add(food)
                if isinstance(food, (Food1, Food2, Food3,)):
                    ScoreText(
                        text=f"+{food.score}",
                        color=SCORE_COLOR_PLUS,
                        x=food.rect.centerx,
                        y=food.rect.centery,
                        groups=self._help_texts
                    )
                    self._sounds.append(EATING_GOOD_OBJ)
                elif isinstance(food, (Garbage1, Garbage2, Garbage3,)):
                    ScoreText(
                        text=f"{food.score}",
                        color=SCORE_COLOR_MINUS,
                        x=food.rect.centerx,
                        y=food.rect.centery,
                        groups=self._help_texts
                    )
                    self._sounds.append(EATING_BAD_OBJ)
        for food in to_remove_foods:
            food.kill()
            self._create_foods(food.__class__, 1)

    def _check_squids_collision(self):
        hit = pygame.sprite.collide_rect(self.squid1, self.squid2)
        if hit and (self.frame_count - self._last_collision) > (INVINCIBLE_TIME+PARALYSIS_TIME):
            self._last_collision = self.frame_count

            # add effect
            center = (
                (self.squid1.rect.centerx + self.squid2.rect.centerx) / 2,
                (self.squid1.rect.centery + self.squid2.rect.centery) / 2
            )
            CryingStar(center[0], center[1], self._help_texts)
            if self.squid1.lv > self.squid2.lv:
                self.squid1.collision_between_squids(COLLISION_SCORE["WIN"], self.frame_count, self._sounds)
                ScoreText(
                    text=f"+{COLLISION_SCORE['WIN']}",
                    color=SCORE_COLOR_PLUS,
                    x=self.squid1.rect.centerx,
                    y=self.squid1.rect.centery,
                    groups=self._help_texts
                )
                self.squid2.collision_between_squids(COLLISION_SCORE["LOSE"], self.frame_count, self._sounds)
                ScoreText(
                    text=f"{COLLISION_SCORE['LOSE']}",
                    color=SCORE_COLOR_MINUS,
                    x=self.squid2.rect.centerx,
                    y=self.squid2.rect.centery,
                    groups=self._help_texts
                )
            elif self.squid1.lv < self.squid2.lv:
                self.squid1.collision_between_squids(COLLISION_SCORE["LOSE"], self.frame_count, self._sounds)
                ScoreText(
                    text=f"{COLLISION_SCORE['LOSE']}",
                    color=SCORE_COLOR_MINUS,
                    x=self.squid1.rect.centerx,
                    y=self.squid1.rect.centery,
                    groups=self._help_texts
                )
                self.squid2.collision_between_squids(COLLISION_SCORE["WIN"], self.frame_count, self._sounds)
                ScoreText(
                    text=f"+{COLLISION_SCORE['WIN']}",
                    color=SCORE_COLOR_PLUS,
                    x=self.squid2.rect.centerx,
                    y=self.squid2.rect.centery,
                    groups=self._help_texts
                )
            else:
                # draw
                self.squid1.collision_between_squids(COLLISION_SCORE["DRAW"], self.frame_count, self._sounds)
                ScoreText(
                    text=f"{COLLISION_SCORE['DRAW']}",
                    color=SCORE_COLOR_MINUS,
                    x=self.squid1.rect.centerx,
                    y=self.squid1.rect.centery,
                    groups=self._help_texts
                )
                self.squid2.collision_between_squids(COLLISION_SCORE["DRAW"], self.frame_count, self._sounds)
                ScoreText(
                    text=f"{COLLISION_SCORE['DRAW']}",
                    color=SCORE_COLOR_MINUS,
                    x=self.squid2.rect.centerx,
                    y=self.squid2.rect.centery,
                    groups=self._help_texts
                )

    def get_data_from_game_to_player(self):
        """
        send something to game AI
        we could send different data to different ai
        """
        to_players_data = {}
        foods_data = []

        foods_data = [
            {
                "x": food.rect.centerx,
                "y": food.rect.centery,
                "w": food.rect.width,
                "h": food.rect.height,
                "type": str(food.type),
                "score": food.score
            }
            for food in self.foods
            if (
                    food.rect.bottom > self.playground.top and
                    food.rect.top < self.playground.bottom and
                    food.rect.right > self.playground.left and
                    food.rect.left < self.playground.right
            )
        ]
        data_to_1p = {
            "frame": self.frame_count,
            "self_x": self.squid1.rect.centerx,
            "self_y": self.squid1.rect.centery,
            "self_w": self.squid1.rect.width,
            "self_h": self.squid1.rect.height,
            "self_vel": self.squid1.vel,
            "self_lv": self.squid1.lv,
            "opponent_x": self.squid2.rect.centerx,
            "opponent_y": self.squid2.rect.centery,
            "opponent_lv": self.squid2.lv,
            "foods": foods_data,
            "score": self.squid1.score,
            "score_to_pass": self._score_to_pass,
            "status": self.get_game_status(),
            "env": self._game_params.__dict__
        }

        data_to_2p = {
            "frame": self.frame_count,
            "self_x": self.squid2.rect.centerx,
            "self_y": self.squid2.rect.centery,
            "self_w": self.squid2.rect.width,
            "self_h": self.squid2.rect.height,
            "self_vel": self.squid2.vel,
            "self_lv": self.squid2.lv,
            "opponent_x": self.squid1.rect.centerx,
            "opponent_y": self.squid1.rect.centery,
            "opponent_lv": self.squid1.lv,
            "foods": foods_data,
            "score": self.squid2.score,
            "score_to_pass": self._score_to_pass,
            "status": self.get_game_status(),
            "env": self._game_params.__dict__
        }

        to_players_data[get_ai_name(0)] = data_to_1p
        to_players_data[get_ai_name(1)] = data_to_2p
        # should be equal to config. GAME_SETUP["ml_clients"][0]["name"]

        return to_players_data

    def get_game_status(self):

        return self._status

    def reset(self):
        # 重新啟動遊戲
        self._running_state=RunningState.OPENING
        self._current_round_num = 1
        self._winner.clear()
        self._init_game()

    def _init_game(self):
        if path.isfile(self._level_file):
            # set by injected file
            self._init_game_by_file(self._level_file)
        else:
            level_file_path = os.path.join(LEVEL_PATH, f"{self._level:03d}.json")
            self._init_game_by_file(level_file_path)

    @property
    def is_passed(self):
        if self.squid1.score >= self._score_to_pass or self.squid2.score >= self._score_to_pass:  # 達成目標分數
            if self.squid1.score == self.squid2.score and self._overtime_count < 1:  # 延長賽
                self._frame_limit += 600
                self._score_to_pass += 50
                self._overtime_count += 1
                print("同分延長賽")
                return False
            return True
        else:
            return False

    @property
    def time_out(self):
        if self.frame_count >= self._frame_limit:
            if self.squid1.score == self.squid2.score and self._overtime_count < 1:  # 延長賽
                self._frame_limit += 300
                self._overtime_count += 1
                print("超時延長賽")
                return False
            else:
                print("時間到")
                return True
        else:
            return False

    @property
    def is_running(self):

        # return self.frame_count < self._frame_limit
        return (not self.time_out) and (not self.is_passed)

    @check_scene_init_data
    def get_scene_init_data(self):
        """
        Get the initial scene and object information for drawing on the web
        """
        # bg_path = path.join(ASSET_PATH, "img/background.jpg")
        # background = create_asset_init_data(
        #     "background", WIDTH, HEIGHT, bg_path,
        #     github_raw_url="https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/easy_game/main/asset/img/background.jpg")

        scene_init_data = {
            "scene": self.scene.__dict__,
            "assets": [
                create_asset_init_data("bg", 1000, 1000, BG_PATH, BG_URL),
                create_asset_init_data("squid1", SQUID_W, SQUID_H, SQUID_PATH, SQUID_URL),
                create_asset_init_data("squid1-hurt", SQUID_W, SQUID_H, SQUID_HURT_PATH, SQUID_HURT_URL),
                create_asset_init_data("squid2", SQUID_W, SQUID_H, SQUID2_PATH, SQUID2_URL),
                create_asset_init_data("squid2-hurt", SQUID_W, SQUID_H, SQUID2_HURT_PATH, SQUID2_HURT_URL),
                create_asset_init_data("star", SQUID_H, SQUID_H, STAR_PATH, STAR_URL),
                create_asset_init_data(IMG_ID_FOOD01_L, FOOD_LV1_SIZE, FOOD_LV1_SIZE, FOOD01_L_PATH, FOOD01_L_URL),
                create_asset_init_data(IMG_ID_FOOD02_L, FOOD_LV2_SIZE, FOOD_LV2_SIZE, FOOD02_L_PATH, FOOD02_L_URL),
                create_asset_init_data(IMG_ID_FOOD03_L, FOOD_LV3_SIZE, FOOD_LV3_SIZE, FOOD03_L_PATH, FOOD03_L_URL),
                create_asset_init_data(IMG_ID_FOOD01_R, FOOD_LV1_SIZE, FOOD_LV1_SIZE, FOOD01_R_PATH, FOOD01_R_URL),
                create_asset_init_data(IMG_ID_FOOD02_R, FOOD_LV2_SIZE, FOOD_LV2_SIZE, FOOD02_R_PATH, FOOD02_R_URL),
                create_asset_init_data(IMG_ID_FOOD03_R, FOOD_LV3_SIZE, FOOD_LV3_SIZE, FOOD03_R_PATH, FOOD03_R_URL),
                create_asset_init_data("garbage01", FOOD_LV1_SIZE, FOOD_LV1_SIZE, GARBAGE01_PATH, GARBAGE01_URL),
                create_asset_init_data("garbage02", FOOD_LV2_SIZE, FOOD_LV2_SIZE, GARBAGE02_PATH, GARBAGE02_URL),
                create_asset_init_data("garbage03", FOOD_LV3_SIZE, FOOD_LV3_SIZE, GARBAGE03_PATH, GARBAGE03_URL),
            ],
            "background": [
                # create_image_view_data(
                #     'bg', self.playground.x, self.playground.y,
                #     self.playground.w, self.playground.h)
            ],
            "musics": [
                create_music_init_data("bgm01", file_path=BGM01_PATH, github_raw_url=BGM01_URL),
                create_music_init_data("bgm02", file_path=BGM02_PATH, github_raw_url=BGM02_URL),
                create_music_init_data("bgm03", file_path=BGM03_PATH, github_raw_url=BGM03_URL),

            ],
            # Create the sounds list using create_sound_init_data
            "sounds": [
                create_sound_init_data("eat_good_food", file_path=EATING_GOOD_PATH, github_raw_url=EATING_GOOD_URL),
                create_sound_init_data("eat_bad_food", file_path=EATING_BAD_PATH, github_raw_url=EATING_BAD_URL),
                create_sound_init_data("pass", file_path=PASS_PATH, github_raw_url=PASS_URL),
                create_sound_init_data("fail", file_path=FAIL_PATH, github_raw_url=FAIL_URL),
                create_sound_init_data("lv_up", file_path=LV_UP_PATH, github_raw_url=LV_UP_URL),
                create_sound_init_data("lv_down", file_path=LV_DOWN_PATH, github_raw_url=LV_DOWN_URL),
                create_sound_init_data("collision", file_path=COLLISION_PATH, github_raw_url=COLLISION_URL)
            ]
        }
        return scene_init_data


    @check_game_progress
    def get_scene_progress_data(self):
        """
        Get the position of game objects for drawing on the web
        """
        if self._running_state == RunningState.OPENING:
            return self._opening_state.get_scene_progress_data()
        elif self._running_state == RunningState.TRANSITION:
            return self._transition_state.get_scene_progress_data()
        elif self._running_state == RunningState.ENDING:
            return self._ending_state.get_scene_progress_data()
        foods_data = [food.game_object_data for food in self.foods]

        game_obj_list = [self.squid1.game_object_data, self.squid2.game_object_data]
        help_texts = [
            obj.game_object_data for obj in self._help_texts
        ]
        game_obj_list.extend(foods_data)
        game_obj_list.extend(help_texts)
        toggle_objs = [
            create_text_view_data(f"Round {self._current_round_num} / {self._game_times}", 770, 10, "#EEEEEE",
                                  "22px Arial BOLD"),

            create_text_view_data(f"{self._winner.count('1P')}:{self._winner.count('2P')}", 795, 40, "#EEEEEE",
                                  "32px Consolas BOLD"),

            create_text_view_data(f"Timer:{self._frame_count_down:04d}", 745, 80, "#EEEEEE", "20px Consolas BOLD"),
            # create_text_view_data(f"", 785, 80, "#EEEEEE", "18px Consolas BOLD"),
            create_text_view_data(f"File :{os.path.basename(self._used_file)}", 745, 120, "#EEEEEE",
                                  "20px Consolas BOLD"),
            # create_text_view_data(f"File :{self._level_file}", 605, 80, "#EEEEEE", "10px Consolas BOLD"),
            create_text_view_data(f"Goal :{self._score_to_pass:04d} pt", 745, 160, "#EEEEEE", "20px Consolas BOLD"),
            # create_text_view_data(f"", 785, 140, "#EEEEEE", "18px Consolas BOLD"),
            create_image_view_data("squid1", 705, 220, 76, 114),
            # create_text_view_data("1P", 705, 130, "#EEEEEE", "22px Consolas BOLD"),
            create_text_view_data(f"Lv     : {self.squid1.lv}", 785, 220, "#EEEEEE", "16px Consolas BOLD"),
            create_text_view_data(f"Next Lv: {LEVEL_THRESHOLDS[self.squid1.lv - 1] - self.squid1.score :04d} pt", 785,
                                  250, "#EEEEEE", "16px Consolas BOLD"),
            create_text_view_data(f"Vel    : {self.squid1.vel:2d}", 785, 280, "#EEEEEE", "16px Consolas BOLD"),
            create_text_view_data(f"Score  : {self.squid1.score:04d} pt", 785, 310, "#EEEEEE", "16px Consolas BOLD"),

            # create_text_view_data("2P", 705, 310, "#EEEEEE", "22px Consolas BOLD"),
            create_image_view_data("squid2", 705, 410, 76, 114),
            create_text_view_data(f"Lv     : {self.squid2.lv}", 785, 410, "#EEEEEE", "16px Consolas BOLD"),
            create_text_view_data(f"Next Lv: {LEVEL_THRESHOLDS[self.squid2.lv - 1] - self.squid2.score :04d} pt", 785,
                                  440, "#EEEEEE", "16px Consolas BOLD"),
            create_text_view_data(f"Vel    : {self.squid2.vel:2d}", 785, 470, "#EEEEEE", "16px Consolas BOLD"),
            create_text_view_data(f"Score  : {self.squid2.score:04d} pt", 785, 500, "#EEEEEE", "16px Consolas BOLD"),
        ]
        game_obj_list.extend(foods_data)
        backgrounds = [
            create_image_view_data(
                'bg', self.playground.x, self.playground.y,
                self.playground.w, self.playground.h)
        ]
        foregrounds = [

        ]

        scene_progress = create_scene_progress_data(
            frame=self.frame_count, background=backgrounds,
            object_list=game_obj_list,
            foreground=foregrounds, toggle=toggle_objs,
            musics=self._music,
            sounds=self._sounds
        )
        self._sounds = []

        # self._music = []
        return scene_progress

    @check_game_result
    def get_game_result(self):
        """
        send game result
        """
        self.game_result_state = GameResultState.FINISH
        #  update record data
        self._record1['rank'] = self.squid1.rank
        self._record1['wins'] = f"{self._winner.count('1P')} / {self._game_times}"
        self._record2['rank'] = self.squid2.rank
        self._record2['wins'] = f"{self._winner.count('2P')} / {self._game_times}"

        return {
            "frame_used": self.frame_count,
            "status": self.game_result_state,
            "attachment": [
                self._record1, self._record2
            ]
        }

    def get_keyboard_command(self):
        """
        Define how your game will run by your keyboard
        """
        cmd_1p = []
        cmd_2p = []
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

        if key_pressed_list[pygame.K_w]:
            cmd_2p.append("UP")
        elif key_pressed_list[pygame.K_s]:
            cmd_2p.append("DOWN")
        elif key_pressed_list[pygame.K_a]:
            cmd_2p.append("LEFT")
        elif key_pressed_list[pygame.K_d]:
            cmd_2p.append("RIGHT")
        else:
            cmd_2p.append("NONE")

        return {get_ai_name(0): cmd_1p, get_ai_name(1): cmd_2p}

    def _create_foods(self, FOOD_TYPE, count: int = 5):
        for i in range(count):
            # add food to group
            food = FOOD_TYPE(self.foods)
            if isinstance(food, (Food1, Food2, Food3,)):
                # if food pos list is empty , re-create
                if len(self._food_pos_list) < 1:
                    self._food_pos_list = divide_window_into_grid(
                        self._food_window)
                pos = self._food_pos_list.pop()
                food.set_center_x_and_y(
                    pos[0],
                    pos[1]
                )


            elif isinstance(food, (Garbage1, Garbage2, Garbage3,)):
                if len(self._garbage_pos_list) < 1:
                    self._garbage_pos_list = divide_window_into_grid(
                        self._garbage_window, rows=1, cols=10)
                pos = self._garbage_pos_list.pop()
                food.set_center_x_and_y(
                    pos[0],
                    pos[1]
                )
        pass

    def update_winner(self):

        if self.squid1.score > self.squid2.score:
            self.squid1.rank = 1
            self.squid2.rank = 2
            self._winner.append("1P")
        elif self.squid1.score < self.squid2.score:
            self.squid1.rank = 2
            self.squid2.rank = 1
            self._winner.append("2P")
        else:
            self.squid1.rank = 1
            self.squid2.rank = 1
            self._winner.append("DRAW")

        self._record1[f"round{self._current_round_num}"] = self.squid1.score
        self._record2[f"round{self._current_round_num}"] = self.squid2.score
        temp_records = [self._record1, self._record2]
        print(pd.DataFrame(temp_records).to_string())


def revise_squid_coordinate(squid: Squid, playground: pygame.Rect):
    squid_rect = copy.deepcopy(squid.rect)
    if squid_rect.left < playground.left:
        squid_rect.left = playground.left
    elif squid_rect.right > playground.right:
        squid_rect.right = playground.right

    if squid_rect.top < playground.top:
        squid_rect.top = playground.top
    elif squid_rect.bottom > playground.bottom:
        squid_rect.bottom = playground.bottom
    squid.rect = squid_rect
    pass


def divide_window_into_grid(window: WindowConfig, rows: int = 10, cols: int = 10) -> list[(int, int)]:
    grid_positions = []

    # Calculate width and height of each grid piece
    width = (window.right - window.left) // cols
    height = (window.bottom - window.top) // rows

    # Generate grid positions
    for row in range(rows):
        for col in range(cols):
            center_x = window.left + col * width + width // 2
            center_y = window.top + row * height + height // 2
            grid_positions.append((center_x, center_y))

    # Shuffle the list to randomize the order of positions
    random.shuffle(grid_positions)

    return grid_positions
