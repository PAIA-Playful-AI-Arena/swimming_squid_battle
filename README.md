# **Swimming Squid** 魷來魷去

![swimming-squid](https://img.shields.io/github/v/tag/PAIA-Playful-AI-Arena/swimming-squid)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![MLGame](https://img.shields.io/badge/MLGame->10.3.2-<COLOR>.svg)](https://github.com/PAIA-Playful-AI-Arena/MLGame)
[![pygame](https://img.shields.io/badge/pygame-2.0.1-<COLOR>.svg)](https://github.com/pygame/pygame/releases/tag/2.0.1)


這是一個吃東西小遊戲，也是 PAIA 的遊戲教學範例

![demo](https://github.com/PAIA-Playful-AI-Arena/swimming-squid/blob/main/asset/swimming-squid.gif?raw=true)

---
# 基礎介紹

## 啟動方式

- 直接啟動 [main.py](http://main.py) 即可執行

### 遊戲參數設定

```python
# main.py 
game = SwimmingSquid(
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
  "frame": 15,
  "score": 8,
  "score_to_pass": 10,
  "squid_x": 350,
  "squid_y": 300,
  "squid_h": 60,
  "squid_w": 40,
  "squid_lv": 1,
  "squid_vel": 10,
  "status": "GAME_ALIVE",
  "foods": [
    {
      "h": 30,
      "score": 1,
      "type": "FOOD_1",
      "w": 30,
      "x": 40,
      "y": 134
    },
    {
      "h": 40,
      "score": 2,
      "type": "FOOD_2",
      "w": 40,
      "x": 422,
      "y": 192
    },
    {
      "h": 50,
      "score": 4,
      "type": "FOOD_3",
      "w": 50,
      "x": 264,
      "y": 476
    },
    {
      "h": 30,
      "score": -1,
      "type": "GARBAGE_1",
      "w": 30,
      "x": 100,
      "y": 496
    },
    {
      "h": 40,
      "score": -4,
      "type": "GARBAGE_2",
      "w": 40,
      "x": 633,
      "y": 432
    },
    {
      "h": 50,
      "score": -10,
      "type": "GARBAGE_3",
      "w": 50,
      "x": 54,
      "y": 194
    }
  ]

}
```

- `frame`：遊戲畫面更新的編號
- `squid_x`：玩家角色的Ｘ座標，表示方塊的`中心點`座標值，單位 pixel。
- `squid_y`：玩家角色的Ｙ座標，表示方塊的`中心點`座標值，單位 pixel。
- `squid_w`：玩家角色的寬度，單位 pixel。
- `squid_h`：玩家角色的高度，單位 pixel。
- `squid_vel`：玩家角色的速度，表示方塊每幀移動的像素，單位 pixel。
- `squid_lv`：玩家角色的等級，最小 1 ，最大 6。
- `foods`：食物的清單，清單內每一個物件都是一個食物的`中心點`座標值，也會提供此食物是什麼類型和分數多少。
  -  `type` 食物類型： `FOOD_1`, `FOOD_2`, `FOOD_3`, `GARBAGE_1`, `GARBAGE_2`, `GARBAGE_3`
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
      "squid": "1P",
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
    - `squid`：玩家編號
    - `score`：吃到的食物總數
    - `rank`：排名
    - `passed`：是否通關

---

# 參考資源
- 音效
    1. https://soundeffect-lab.info/sound/anime/
- 背景音樂
    1. https://www.motionelements.com/zh-hant/stock-music-28190007-bossa-nova-short-loop
- 圖片
    1. 魷魚 https://illustcenter.com/2022/07/03/rdesign_1659/
    2. 湯匙 https://illustcenter.com/2021/11/24/rdesign_6275/
    3. 薯條 https://illustcenter.com/2021/11/16/rdesign_5098/
    4. 空罐 https://illustcenter.com/2021/11/19/rdesign_5772/
    5. 魚1 https://illustcenter.com/2021/12/22/rdesign_8914/
    6. 魚2 https://illustcenter.com/2021/10/28/rdesign_3149/
    7. 蝦子 https://illustcenter.com/2021/10/28/rdesign_3157/