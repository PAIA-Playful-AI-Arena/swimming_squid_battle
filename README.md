# **Easy Game**

![easy_game](https://img.shields.io/github/v/tag/PAIA-Playful-AI-Arena/easy_game)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![MLGame](https://img.shields.io/badge/MLGame->10.3.2-<COLOR>.svg)](https://github.com/PAIA-Playful-AI-Arena/MLGame)
[![pygame](https://img.shields.io/badge/pygame-2.0.1-<COLOR>.svg)](https://github.com/pygame/pygame/releases/tag/2.0.1)


這是一個吃東西小遊戲，也是 PAIA 的遊戲教學範例

![demo](https://github.com/PAIA-Playful-AI-Arena/easy_game/blob/main/asset/easy_game.gif?raw=true)

---
# 基礎介紹

## 啟動方式

- 直接啟動 [main.py](http://main.py) 即可執行

### 遊戲參數設定

```python
# main.py 
game = EasyGame(
            level: int = 1,
            level_file: str = None,
            sound: str = "off")
```
- `level`: 選定內建關卡，預設為 1 選擇第一關。
- `level_file`: 使用外部檔案作為關卡，請注意，使用此設定將會覆蓋掉關卡編號，並且不會自動進入下一關。
- `sound`: 音效。

## 玩法

- 使用鍵盤 上、下、左、右 控制方塊

## 目標

1. 在遊戲時間截止前，盡可能吃到愈多的食物吧！

### 通關條件

1. 時間結束前，吃到的食物超過`score`，即可過關。

### 失敗條件

1. 時間結束前，吃到的食物少於`score`，即算失敗。

## 遊戲系統

1. 行動機制
    
    上下左右的行動，每次移動`10.5px`
    
2. 座標系統
    - 螢幕大小 800 x 600
    - 主角方塊 30 x 30
    - 食物方塊 8 x 8

---

# 進階說明

## 使用ＡＩ玩遊戲

```bash
# 在easy game中，打開終端機
python -m mlgame -i ./ml/ml_play_template.py ./ --level 3
python -m mlgame -i ./ml/ml_play_template.py ./ --level_file /path_to_file/level_file.json
```

## ＡＩ範例

```python
import random

class MLPlay:
    def __init__(self,ai_name,*args, **kwargs):
        print("Initial ml script")

    def update(self, scene_info: dict,,*args, **kwargs):

        # print("AI received data from game :", scene_info)

        actions = ["UP", "DOWN", "LEFT", "RIGHT", "NONE"]

        return random.sample(actions, 1)

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass
```

## 遊戲資訊

- scene_info 的資料格式如下

```json
{
  "frame": 25,
  "player_x": 425,
  "player_y": 306,
  "player_size": 90,
  "player_vel": 16,
  "foods": [
    {
      "x": 656,
      "y": 210,
      "type": "GOOD_1",
      "score": 1
    },
...,
    {
      "x": 371,
      "y": 217,
      "type": "BAD_1",
      "score": -1
    }
    
  ],
  "score": 0,
  "status": "GAME_ALIVE"
}
```

- `frame`：遊戲畫面更新的編號
- `player_x`：主角方塊的Ｘ座標，表示方塊的`中心點`座標值，單位 pixel。
- `player_y`：主角方塊的Ｙ座標，表示方塊的`中心點`座標值，單位 pixel。
- `player_size`：主角方塊的大小，表示方塊的長寬，單位 pixel。
- `player_vel`：主角方塊的速度，表示方塊每幀移動的像素，單位 pixel。
- `foods`：食物的清單，清單內每一個物件都是一個食物的左上方座標值，也會提供此食物是什麼類型和分數多少。
  -  `type` 食物類型： `GOOD_1`, `GOOD_2`, `GOOD_3`, `BAD_1`, `BAD_2`, `BAD_3`
- `score`：目前得到的分數
- `score_to_pass`：通關分數
- `status`： 目前遊戲的狀態
    - `GAME_ALIVE`：遊戲進行中
    - `GAME_PASS`：遊戲通關
    - `GAME_OVER`：遊戲結束

## 動作指令

- 在 update() 最後要回傳一個字串，主角物件即會依照對應的字串行動，一次只能執行一個行動。
    - `UP`：向上移動
    - `DOWN`：向下移動
    - `LEFT`：向左移動
    - `RIGHT`：向右移動
    - `NONE`：原地不動

## 遊戲結果

- 最後結果會顯示在console介面中，若是PAIA伺服器上執行，會回傳下列資訊到平台上。

```json
{
  "frame_used": 100,
  "state": "FAIL",
  "attachment": [
    {
      "player": "1P",
      "score": 0,
      "rank": 1,
      "passed": false
    }
  ]
}
```

- `frame_used`：表示使用了多少個frame
- `state`：表示遊戲結束的狀態
    - `FAIL`：遊戲失敗
    - `FINISH`：遊戲完成
- `attachment`：紀錄遊戲各個玩家的結果與分數等資訊
    - `player`：玩家編號
    - `score`：吃到的食物總數
    - `rank`：排名
    - `passed`：是否通關

---