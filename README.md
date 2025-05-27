# 猫の冒険ゲーム (Cat Adventure)

猫の冒険ゲームは、猫のキャラクターを操作して障害物を避けながら家を目指すシンプルな2Dゲームです。

## ゲームの概要

あなたは猫となり、道路上の障害物（空き缶やカラス）を避けながら、右側にある家の玄関扉を目指します。
障害物には以下の種類があります：
- 通常の空き缶：静止している障害物
- 突進型の空き缶：猫が近づくとマッチョに変身して逃げる特殊な障害物
- 通常のカラス：上下に動く飛行障害物
- 追尾型のカラス：猫を見つけると追いかけてくる特殊な飛行障害物

ゲームにはほのぼのとしたBGMが流れ、プレイ体験を豊かにします。

## 開発環境

このゲームは以下の環境で開発されています：
- Python 3.x
- Pygame 2.x
- Linux/Windows/macOS（クロスプラットフォーム対応）

## インストール方法

### 1. Pythonのインストール

#### Windows
1. [Python公式サイト](https://www.python.org/downloads/)からインストーラーをダウンロード
2. インストーラーを実行（「Add Python to PATH」にチェックを入れることを推奨）
3. コマンドプロンプトで `python --version` を実行して、インストールを確認

#### macOS
1. Homebrewがインストールされている場合：`brew install python`
2. または[Python公式サイト](https://www.python.org/downloads/)からインストーラーをダウンロード
3. ターミナルで `python3 --version` を実行して、インストールを確認

#### Linux
1. 多くのディストリビューションではPythonがプリインストールされています
2. Ubuntu/Debian: `sudo apt-get install python3`
3. Fedora: `sudo dnf install python3`
4. ターミナルで `python3 --version` を実行して、インストールを確認

### 2. Pygameのインストール

Pythonがインストールされたら、以下のコマンドでPygameをインストールします：

```bash
# Windows
pip install pygame

# macOS/Linux
pip3 install pygame
```

インストールを確認するには：
```bash
# Windows
python -c "import pygame; print(pygame.ver)"

# macOS/Linux
python3 -c "import pygame; print(pygame.ver)"
```

### 3. NumPyのインストール

BGM機能のために、NumPyライブラリも必要です：

```bash
# Windows
pip install numpy

# macOS/Linux
pip3 install numpy
```

インストールを確認するには：
```bash
# Windows
python -c "import numpy; print(numpy.__version__)"

# macOS/Linux
python3 -c "import numpy; print(numpy.__version__)"
```

### 3. ゲームのダウンロード

GitHubからリポジトリをクローンするか、ZIPファイルとしてダウンロードします：

```bash
git clone https://github.com/siromi08/cat_game.git
cd cat_game
```

または[リポジトリのページ](https://github.com/siromi08/cat_game)から「Code」→「Download ZIP」でダウンロードし、解凍します。

## ゲームの実行方法

ゲームファイルがあるディレクトリで以下のコマンドを実行します：

```bash
# Windows
python cat_game.py

# macOS/Linux
python3 cat_game.py
```

## 操作方法

- **右矢印キー**：猫を右に移動
- **上矢印キー**：ジャンプ（障害物を避けるために使用）
- **Rキー**：ゲームオーバーまたはゲームクリア後にリスタート

## ゲームの目標

- 道路上の障害物（空き缶とカラス）を避けながら進む
- 右側にある家の玄関扉に到達する
- 障害物に当たるとゲームオーバー
- ゴールに到達すると「おかえり！」と表示されてゲームクリア

## 特殊な障害物

### 突進型の空き缶
- 猫が左側から近づくと検知して突進を開始
- 突進時には筋肉ムキムキのマッチョに変身
- 両腕と両足が生え、怒った表情で左方向に走って逃げる
- どの空き缶が突進型なのかは、プレイしながら発見してください！

### 追尾型のカラス
- 猫が一定距離内に入ると追尾を開始
- 追尾中は体の色が赤く変化
- 猫を追いかけるように移動する
- どのカラスが追尾型なのかは、プレイしながら発見してください！

## 開発者向け情報

ゲームのカスタマイズや拡張を行いたい場合は、`cat_game.py`ファイルを編集してください。主なクラスと機能：

- `Cat`：猫のキャラクタークラス
- `Obstacle`：障害物（空き缶）クラス
- `CrowObstacle`：カラス障害物クラス
- `Goal`：ゴール（家）クラス
- `Background`：背景クラス

## ライセンス

このゲームは自由に使用、改変、配布することができます。

## 作者

[siromi08](https://github.com/siromi08)

---

# Cat Adventure Game

Cat Adventure is a simple 2D game where you control a cat character and avoid obstacles to reach home.

## Game Overview

You play as a cat, avoiding obstacles (cans and crows) on the road while trying to reach the front door of a house on the right side.
There are several types of obstacles:
- Regular cans: Stationary obstacles
- Rushing cans: Special obstacles that transform into muscular characters and run away when the cat approaches
- Regular crows: Flying obstacles that move up and down
- Tracking crows: Special flying obstacles that chase the cat when they detect it

The game features a relaxing background music that enhances the playing experience.

## Development Environment

This game was developed using:
- Python 3.x
- Pygame 2.x
- Cross-platform compatible (Linux/Windows/macOS)

## Installation Instructions

### 1. Installing Python

#### Windows
1. Download the installer from the [Python official website](https://www.python.org/downloads/)
2. Run the installer (recommended to check "Add Python to PATH")
3. Verify installation by running `python --version` in the command prompt

#### macOS
1. If you have Homebrew installed: `brew install python`
2. Or download the installer from the [Python official website](https://www.python.org/downloads/)
3. Verify installation by running `python3 --version` in the terminal

#### Linux
1. Python is pre-installed on many distributions
2. Ubuntu/Debian: `sudo apt-get install python3`
3. Fedora: `sudo dnf install python3`
4. Verify installation by running `python3 --version` in the terminal

### 2. Installing Pygame

After Python is installed, install Pygame with the following command:

```bash
# Windows
pip install pygame

# macOS/Linux
pip3 install pygame
```

To verify the installation:
```bash
# Windows
python -c "import pygame; print(pygame.ver)"

# macOS/Linux
python3 -c "import pygame; print(pygame.ver)"
```

### 3. Installing NumPy

NumPy library is required for the BGM functionality:

```bash
# Windows
pip install numpy

# macOS/Linux
pip3 install numpy
```

To verify the installation:
```bash
# Windows
python -c "import numpy; print(numpy.__version__)"

# macOS/Linux
python3 -c "import numpy; print(numpy.__version__)"
```

### 3. Downloading the Game

Clone the repository from GitHub or download it as a ZIP file:

```bash
git clone https://github.com/siromi08/cat_game.git
cd cat_game
```

Or download from the [repository page](https://github.com/siromi08/cat_game) by clicking "Code" → "Download ZIP" and extract it.

## How to Run the Game

In the directory containing the game file, run the following command:

```bash
# Windows
python cat_game.py

# macOS/Linux
python3 cat_game.py
```

## Controls

- **Right Arrow Key**: Move the cat to the right
- **Up Arrow Key**: Jump (used to avoid obstacles)
- **R Key**: Restart after game over or game clear

## Game Objective

- Progress while avoiding obstacles (cans and crows) on the road
- Reach the front door of the house on the right
- Hitting an obstacle results in game over
- Reaching the goal displays "Welcome Home!" and completes the game

## Special Obstacles

### Rushing Cans
- Detect when the cat approaches from the left and start rushing
- Transform into muscular characters when rushing
- Grow arms and legs, and run away to the left with an angry expression
- Discover which cans are the rushing type while playing!

### Tracking Crows
- Start tracking when the cat enters within a certain distance
- Body color changes to red when tracking
- Move to follow the cat
- Discover which crows are the tracking type while playing!

## Developer Information

To customize or extend the game, edit the `cat_game.py` file. Main classes and features:

- `Cat`: Cat character class
- `Obstacle`: Obstacle (can) class
- `CrowObstacle`: Crow obstacle class
- `Goal`: Goal (house) class
- `Background`: Background class

## License

This game can be freely used, modified, and distributed.

## Author

[siromi08](https://github.com/siromi08)
