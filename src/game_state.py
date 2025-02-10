from enum import Enum

from .env import PASS_OBJ
from mlgame.game.paia_game import GameState
from mlgame.view.view_model import create_scene_progress_data, create_text_view_data


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
        self.reset()
    def update(self):
        p1_score = self._game._winner.count("1P")
        p2_score = self._game._winner.count("2P")
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
            self.reset()
            self._game.set_game_state(RunningState.PLAYING)
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
        self._info_text = create_text_view_data("Ready", 230, 0, "#EEEEEE", "64px Consolas BOLD")
        self._sound.append(PASS_OBJ)

class OpeningState(GameState):
    def __init__(self, game: 'SwimmingSquidBattle'):
        self._game = game
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
            self.reset()
            self._game.set_game_state(RunningState.PLAYING)
        self.frame_count += 1

    def get_scene_progress_data(self):
        return create_scene_progress_data(
            frame=self.frame_count,
            background=[],
            object_list=[self._ready_text, self._go_text],
            foreground=[],
            toggle=[],
            musics=[], sounds=[]
            )

    def reset(self):
        self.frame_count = 0
        self._ready_text = create_text_view_data("Ready", 300, 300, "#EEEEEE", "64px Consolas BOLD")
        self._go_text = create_text_view_data("Go! ", -300, -360, "#EEEEEE", "64px Consolas BOLD")


class RunningState(Enum):
    OPENING = 0
    TRANSITION = 1
    ENDING = 2
    PLAYING = 3
    RESET = 4
