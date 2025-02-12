from enum import Enum
from math import sin
import math

from .env import HEIGHT, IMG_ID_OPENNING_BG, IMG_ID_OPENNING_LOGO, IMG_ID_TRANSITION_BG, IMG_ID_TRANSITION_CROWN, IMG_ID_TRANSITION_P1, IMG_ID_TRANSITION_P2, PASS_OBJ, WIDTH
from mlgame.game.paia_game import GameState
from mlgame.view.view_model import create_image_view_data, create_scene_progress_data, create_text_view_data


class EndingState(GameState):
    def __init__(self,game):
        self._game = game
        self.frame_count = 0
        self._info_text = {}
        self._sound = [PASS_OBJ]
        self.reset()
    def update(self):
        result = f"1P {self._game._winner.count('1P')} vs 2P {self._game._winner.count('2P')}"
        if self._game._winner.count("1P") > self._game._game_times / 2:  # 1P 贏
            result+="  1P win !"

        elif self._game._winner.count("2P") > self._game._game_times / 2:  # 2P 贏
            result+="  2P win!"
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
            self.reset()
            self._game.set_game_state(RunningState.RESET)
            
        self.frame_count += 1
    def get_scene_progress_data(self):
        return create_scene_progress_data(
            frame=self.frame_count,
            background=[],
            object_list=[self._info_text],
            foreground=[],
            toggle=[],
            musics=[], sounds=self._sound
            )
    def reset(self):
        self.frame_count = 0
        self._info_text = create_text_view_data("Ending", 130, 0, "#EEEEEE", "64px Consolas BOLD")
        self._sound = [PASS_OBJ]


class TransitionState(GameState):
    def __init__(self,game):
        self._game = game
        self.frame_count = 0
        self._info_text = {}
        self._sound = [PASS_OBJ]
        self._crown_x = 0
        self._crown_y = HEIGHT/2-125
        self._crown_y_degree = 0
        self._crown_y_bias = 0
        self._p1_score = 0
        self._p2_score = 0
        self.reset()
    def update(self):
        self._p1_score = self._game.squid1.score
        self._p2_score = self._game.squid2.score
        self._crown_y_degree += 0.15
        self._crown_y_bias = 10*sin(self._crown_y_degree)
        if self._p1_score > self._p2_score:
            self._crown_x = WIDTH/2-368
        elif self._p1_score < self._p2_score:
            self._crown_x = WIDTH/2+124
        
        if self.frame_count == 0:
            self._sound = [PASS_OBJ]
        else:
            self._sound = []

        if self.frame_count < 90:
            pass
        elif 91 <= self.frame_count:
            self.reset()
            self._game.set_game_state(RunningState.PLAYING)
        self.frame_count += 1
        
    def get_scene_progress_data(self):
        return create_scene_progress_data(
            frame=self.frame_count,
            background=[
                create_image_view_data(IMG_ID_TRANSITION_BG, 0, 0, 1280, 768),
                ],
            object_list=[
                create_image_view_data(IMG_ID_TRANSITION_P1, WIDTH/2-328, HEIGHT/2-164/2, 164, 164),
                create_image_view_data(IMG_ID_TRANSITION_P2, WIDTH/2+164, HEIGHT/2-164/2, 164, 164),
                create_text_view_data(f"{self._p1_score:03d}pt", WIDTH/2-328, HEIGHT/2+164, "#EEEEEE", "48px Burnfont BOLD"),
                create_text_view_data(f"{self._p2_score:03d}pt", WIDTH/2+164, HEIGHT/2+164, "#EEEEEE", "48px Burnfont BOLD"),
                create_image_view_data(IMG_ID_TRANSITION_CROWN, self._crown_x, self._crown_y+self._crown_y_bias, 114, 80),
                ],
            foreground=[],
            toggle=[],
            musics=[], sounds=self._sound
            )
    def reset(self):
        self.frame_count = 0
        self._info_text = create_text_view_data("Ready", 230, 0, "#EEEEEE", "64px Consolas BOLD")
        self._sound.append(PASS_OBJ)

class OpeningState(GameState):
    def __init__(self, game: 'SwimmingSquidBattle'):
        self._game = game
        self.frame_count = 0
        # self._ready_text = create_text_view_data("Ready", 300, 300, "#EEEEEE", "64px Consolas BOLD")
        # self._go_text = create_text_view_data("Go! ", -300, -360, "#EEEEEE", "64px Consolas BOLD")
        self._logo_bias_degree = 0
        self._logo_bias = sin(self._logo_bias_degree)
    def update(self):
        if self.frame_count < 90:
            self._logo_bias_degree += 0.15
            self._logo_bias = 15*sin(self._logo_bias_degree)
        elif 90 <= self.frame_count:
            self.frame_count=0
            self.reset()
            self._game.set_game_state(RunningState.PLAYING)
        self.frame_count += 1

    def get_scene_progress_data(self):
        return create_scene_progress_data(
            frame=self.frame_count,
            background=[
                create_image_view_data(IMG_ID_OPENNING_BG, 0, 0, 1280, 768),
                create_image_view_data(IMG_ID_OPENNING_LOGO, 1280/2-506/2, 768/2-256/2+self._logo_bias, 506, 256),
                ],
            object_list=[
                # self._ready_text, self._go_text
                ],
            foreground=[],
            toggle=[],
            musics=[], sounds=[]
            )

    def reset(self):
        self.frame_count = 0
        self._logo_bias_degree = 0
        self._logo_bias = sin(self._logo_bias_degree)

class RunningState(Enum):
    OPENING = 0
    TRANSITION = 1
    ENDING = 2
    PLAYING = 3
    RESET = 4
