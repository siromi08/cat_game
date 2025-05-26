# 猫の冒険ゲーム (Cat Adventure)

猫の冒険ゲームは、猫のキャラクターを操作して障害物を避けながら家を目指すシンプルな2Dゲームです。

## ゲームの概要

あなたは猫となり、道路上の障害物（空き缶やカラス）を避けながら、右側にある家の玄関扉を目指します。
障害物には以下の種類があります：
- 通常の空き缶：静止している障害物
- 突進型の空き缶：猫が近づくとマッチョに変身して逃げる特殊な障害物
- 通常のカラス：上下に動く飛行障害物
- 追尾型のカラス：猫を見つけると追いかけてくる特殊な飛行障害物

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
