import pygame
import sys
import os
import random
import math

# 日本語表示のための環境変数設定
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LANG'] = 'ja_JP.UTF-8'

# Pygameの初期化
pygame.init()

# 画面設定
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# タイトルを英語表記に変更
pygame.display.set_caption("Cat Adventure")

# 日本語フォントを直接指定
FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

try:
    # ゲーム内メッセージ用のフォントを作成
    font = pygame.font.Font(FONT_PATH, 74)
except Exception as e:
    print(f"Warning: Error loading Japanese font: {e}")
    font = pygame.font.Font(None, 74)

# 色の定義
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
RED = (255, 0, 0)

# 猫のキャラクター設定
class Cat:
    def __init__(self):
        self.width = 80  # 胴体を長くするために幅を増加
        self.height = 35  # 高さを少し調整
        self.x = 100
        self.y = WINDOW_HEIGHT - self.height - 10
        self.velocity_y = 0
        self.is_jumping = False
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # 猫の色
        self.body_color = (255, 165, 0)  # オレンジ色
        self.eye_color = (0, 200, 0)     # 緑色
        self.nose_color = (255, 192, 203) # ピンク

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -15
            self.is_jumping = True

    def move(self):
        # 重力の適用
        self.velocity_y += 0.8
        self.y += self.velocity_y

        # 地面との衝突判定
        if self.y > WINDOW_HEIGHT - self.height - 10:
            self.y = WINDOW_HEIGHT - self.height - 10
            self.velocity_y = 0
            self.is_jumping = False

        self.rect.y = self.y

    def draw(self, screen, camera_x):
        # 画面上の描画位置を計算
        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y

        # 胴体（より長い楕円）
        body_height = self.height - 5
        pygame.draw.ellipse(screen, self.body_color, 
                          (screen_x, screen_y + 10, self.width - 15, body_height))
        
        # 頭（より高い位置に、少し斜めに）
        head_radius = 20
        head_x = screen_x + self.width - 5  # 頭の位置を前側に
        head_y = screen_y - 10  # 頭の位置を高く
        pygame.draw.circle(screen, self.body_color, 
                         (head_x, head_y + head_radius), head_radius)
        
        # 首（頭と胴体をつなぐ部分）- 頭の位置に合わせて調整
        neck_points = [
            (head_x - head_radius - 5, head_y + head_radius + 15),
            (head_x - head_radius + 5, head_y + head_radius + 18),
            (head_x - head_radius + 15, head_y + head_radius + 15)
        ]
        pygame.draw.polygon(screen, self.body_color, neck_points)
        
        # 耳（より自然な三角形）- 左耳
        left_ear_points = [
            (head_x - 8, head_y + 12),
            (head_x - 18, head_y - 8),
            (head_x + 2, head_y + 8)
        ]
        pygame.draw.polygon(screen, self.body_color, left_ear_points)
        
        # 耳の内側（ピンク）- 左
        left_inner_ear_points = [
            (head_x - 7, head_y + 10),
            (head_x - 14, head_y - 4),
            (head_x, head_y + 8)
        ]
        pygame.draw.polygon(screen, self.nose_color, left_inner_ear_points)
        
        # 耳（より自然な三角形）- 右耳
        right_ear_points = [
            (head_x + 8, head_y + 12),
            (head_x + 18, head_y - 8),
            (head_x - 2, head_y + 8)
        ]
        pygame.draw.polygon(screen, self.body_color, right_ear_points)
        
        # 耳の内側（ピンク）- 右
        right_inner_ear_points = [
            (head_x + 7, head_y + 10),
            (head_x + 14, head_y - 4),
            (head_x, head_y + 8)
        ]
        pygame.draw.polygon(screen, self.nose_color, right_inner_ear_points)
        
        # 目（左）- より詳細な表現
        pygame.draw.ellipse(screen, self.eye_color, 
                          (head_x - 10, head_y + head_radius - 8, 8, 12))
        pygame.draw.circle(screen, (0, 0, 0), 
                         (head_x - 6, head_y + head_radius - 2), 3)  # 瞳
        pygame.draw.circle(screen, (255, 255, 255), 
                         (head_x - 7, head_y + head_radius - 4), 2)  # ハイライト
        
        # 目（右）- より詳細な表現
        pygame.draw.ellipse(screen, self.eye_color, 
                          (head_x + 2, head_y + head_radius - 8, 8, 12))
        pygame.draw.circle(screen, (0, 0, 0), 
                         (head_x + 6, head_y + head_radius - 2), 3)  # 瞳
        pygame.draw.circle(screen, (255, 255, 255), 
                         (head_x + 5, head_y + head_radius - 4), 2)  # ハイライト
        
        # 鼻（より大きく）
        pygame.draw.circle(screen, self.nose_color, 
                         (head_x, head_y + head_radius + 2), 3)
        
        # ひげ（6本）
        whisker_start_y = head_y + head_radius + 2
        # 左側のひげ
        pygame.draw.line(screen, (100, 100, 100), (head_x - 2, whisker_start_y), (head_x - 20, whisker_start_y - 5), 1)
        pygame.draw.line(screen, (100, 100, 100), (head_x - 2, whisker_start_y), (head_x - 20, whisker_start_y), 1)
        pygame.draw.line(screen, (100, 100, 100), (head_x - 2, whisker_start_y), (head_x - 20, whisker_start_y + 5), 1)
        # 右側のひげ
        pygame.draw.line(screen, (100, 100, 100), (head_x + 2, whisker_start_y), (head_x + 20, whisker_start_y - 5), 1)
        pygame.draw.line(screen, (100, 100, 100), (head_x + 2, whisker_start_y), (head_x + 20, whisker_start_y), 1)
        pygame.draw.line(screen, (100, 100, 100), (head_x + 2, whisker_start_y), (head_x + 20, whisker_start_y + 5), 1)
        
        # 足（4本）- より自然な位置に
        leg_color = self.body_color
        leg_width = 6
        leg_height = 12
        # 前足
        pygame.draw.rect(screen, leg_color, (screen_x + 15, screen_y + self.height - 2, leg_width, leg_height))
        pygame.draw.rect(screen, leg_color, (screen_x + 30, screen_y + self.height - 2, leg_width, leg_height))
        # 後ろ足
        pygame.draw.rect(screen, leg_color, (screen_x + self.width - 40, screen_y + self.height - 2, leg_width, leg_height))
        pygame.draw.rect(screen, leg_color, (screen_x + self.width - 25, screen_y + self.height - 2, leg_width, leg_height))
        
        # 尻尾（より自然な曲線）- さらに太さを増加
        tail_points = [
            (screen_x + 5, screen_y + self.height - 8),
            (screen_x - 10, screen_y + self.height - 15),
            (screen_x - 20, screen_y + self.height - 25),
            (screen_x - 25, screen_y + self.height - 35)
        ]
        pygame.draw.lines(screen, self.body_color, False, tail_points, 12)

# ゴール設定
class Goal:
    def __init__(self):
        self.width = 50
        self.height = 100
        self.x = WINDOW_WIDTH * 4 - 100  # 画面の4倍の位置にゴールを設置（2倍から4倍に変更）
        self.y = WINDOW_HEIGHT - self.height - 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, camera_x):
        # カメラの位置を考慮してゴールを描画
        door_x = self.x - camera_x
        door_y = self.y
        
        # ドアの枠（茶色）
        door_frame = pygame.Rect(door_x - 10, door_y - 10, self.width + 20, self.height + 10)
        pygame.draw.rect(screen, (139, 69, 19), door_frame)  # 茶色の枠
        
        # ドア本体（赤茶色）
        door_rect = pygame.Rect(door_x, door_y, self.width, self.height)
        pygame.draw.rect(screen, (165, 42, 42), door_rect)  # 赤茶色のドア
        
        # ドアノブ（金色）
        doorknob_x = door_x + self.width - 15
        doorknob_y = door_y + self.height // 2
        pygame.draw.circle(screen, (255, 215, 0), (doorknob_x, doorknob_y), 5)  # 金色のドアノブ
        
        # ドアの装飾（窓のような四角形）
        window_rect = pygame.Rect(door_x + 10, door_y + 15, self.width - 20, self.height // 3)
        pygame.draw.rect(screen, (173, 216, 230), window_rect)  # 水色の窓
        
        # 窓の格子
        pygame.draw.line(screen, (139, 69, 19), (door_x + self.width // 2, door_y + 15), 
                         (door_x + self.width // 2, door_y + 15 + self.height // 3), 2)
        pygame.draw.line(screen, (139, 69, 19), (door_x + 10, door_y + 15 + self.height // 6), 
                         (door_x + 10 + self.width - 20, door_y + 15 + self.height // 6), 2)
        
        # 玄関マット
        mat_rect = pygame.Rect(door_x, door_y + self.height, self.width, 10)
        pygame.draw.rect(screen, (50, 205, 50), mat_rect)  # 緑色のマット

# 背景クラス
class Background:
    def __init__(self):
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        
        # 家の色のバリエーション
        self.house_colors = [
            (200, 200, 200),  # 灰色
            (245, 222, 179),  # ベージュ
            (255, 250, 205),  # 薄黄色
            (188, 143, 143),  # 薄茶色
            (230, 230, 250),  # 薄紫色
            (240, 255, 240),  # 薄緑色
            (255, 228, 225),  # 薄ピンク
        ]
        
        # 屋根の色のバリエーション
        self.roof_colors = [
            (139, 69, 19),    # 茶色
            (165, 42, 42),    # 赤茶色
            (128, 128, 128),  # 濃い灰色
            (70, 130, 180),   # 青色
            (85, 107, 47),    # 暗い緑色
        ]
        
        # 住宅地の背景を表現する詳細な情報を持つ家のリスト
        # 各家は (x, y, width, height, house_color_index, roof_color_index, has_chimney) の形式
        self.houses = [
            (100, 400, 100, 150, 0, 0, True),
            (300, 350, 120, 200, 1, 1, False),
            (500, 380, 150, 170, 2, 2, True),
            (700, 420, 90, 130, 3, 0, False),
            # 追加の家（画面外）
            (900, 400, 100, 150, 4, 3, True),
            (1100, 350, 120, 200, 5, 4, False),
            (1300, 380, 150, 170, 6, 0, True),
            (1500, 420, 90, 130, 0, 1, False),
            # さらに追加の家（より遠くに）
            (1700, 400, 100, 150, 1, 2, True),
            (1900, 350, 120, 200, 2, 3, False),
            (2100, 380, 150, 170, 3, 4, True),
            (2300, 420, 90, 130, 4, 0, False),
            (2500, 400, 100, 150, 5, 1, True),
            (2700, 350, 120, 200, 6, 2, False),
            (2900, 380, 150, 170, 0, 3, True),
            (3100, 420, 90, 130, 1, 4, False),
        ]
        
        # 木のリスト (x, y, size)
        self.trees = [
            (200, 450, 50),
            (400, 470, 40),
            (600, 460, 55),
            (800, 480, 45),
            (1000, 450, 50),
            (1200, 470, 40),
            (1400, 460, 55),
            (1600, 480, 45),
            (1800, 450, 50),
            (2000, 470, 40),
            (2200, 460, 55),
            (2400, 480, 45),
            (2600, 450, 50),
            (2800, 470, 40),
            (3000, 460, 55),
            (3200, 480, 45),
        ]
        
        # 街灯のリスト (x, y)
        self.streetlights = [
            (150, 500),
            (450, 500),
            (750, 500),
            (1050, 500),
            (1350, 500),
            (1650, 500),
            (1950, 500),
            (2250, 500),
            (2550, 500),
            (2850, 500),
            (3150, 500),
        ]
        
        # 雲のリスト (x, y, width, height)
        self.clouds = [
            (200, 100, 120, 60),
            (500, 80, 150, 70),
            (800, 120, 100, 50),
            (1100, 90, 130, 65),
            (1400, 110, 110, 55),
            (1700, 70, 140, 60),
            (2000, 100, 120, 60),
            (2300, 80, 150, 70),
            (2600, 120, 100, 50),
            (2900, 90, 130, 65),
            (3200, 110, 110, 55),
        ]

    def draw(self, screen, camera_x):
        # 空（グラデーション）
        for y in range(WINDOW_HEIGHT):
            # 上から下に向かって色が変化するグラデーション
            color_value = 135 + (y / WINDOW_HEIGHT * 60)
            if color_value > 255:
                color_value = 255
            pygame.draw.line(screen, (135, color_value, 235), (0, y), (WINDOW_WIDTH, y))
        
        # 太陽
        sun_x = 150 - camera_x * 0.1  # 太陽はゆっくり動く（視差効果）
        if 0 <= sun_x <= WINDOW_WIDTH:
            pygame.draw.circle(screen, (255, 255, 0), (int(sun_x), 100), 40)
            # 太陽光線
            for i in range(8):
                angle = i * math.pi / 4
                end_x = int(sun_x + math.cos(angle) * 60)
                end_y = int(100 + math.sin(angle) * 60)
                pygame.draw.line(screen, (255, 255, 0), (int(sun_x), 100), (end_x, end_y), 3)
        
        # 雲（遠景）
        for cloud in self.clouds:
            x, y, width, height = cloud
            cloud_x = x - camera_x * 0.3  # 雲はゆっくり動く（視差効果）
            if -width <= cloud_x <= WINDOW_WIDTH:
                # 雲の形を楕円で表現
                pygame.draw.ellipse(screen, (255, 255, 255), (cloud_x, y, width, height))
                pygame.draw.ellipse(screen, (255, 255, 255), (cloud_x + width * 0.2, y - height * 0.2, width * 0.6, height * 0.6))
                pygame.draw.ellipse(screen, (255, 255, 255), (cloud_x + width * 0.4, y + height * 0.1, width * 0.6, height * 0.6))
        
        # 遠くの山（背景）
        mountain_points = [
            (0 - camera_x * 0.5, WINDOW_HEIGHT - 150),
            (300 - camera_x * 0.5, WINDOW_HEIGHT - 250),
            (600 - camera_x * 0.5, WINDOW_HEIGHT - 180),
            (900 - camera_x * 0.5, WINDOW_HEIGHT - 300),
            (1200 - camera_x * 0.5, WINDOW_HEIGHT - 200),
            (1500 - camera_x * 0.5, WINDOW_HEIGHT - 280),
            (1800 - camera_x * 0.5, WINDOW_HEIGHT - 220),
            (2100 - camera_x * 0.5, WINDOW_HEIGHT - 320),
            (2400 - camera_x * 0.5, WINDOW_HEIGHT - 180),
            (2700 - camera_x * 0.5, WINDOW_HEIGHT - 250),
            (3000 - camera_x * 0.5, WINDOW_HEIGHT - 200),
            (3300 - camera_x * 0.5, WINDOW_HEIGHT - 150),
            (3600 - camera_x * 0.5, WINDOW_HEIGHT - 150),
            (3600 - camera_x * 0.5, WINDOW_HEIGHT),
            (0 - camera_x * 0.5, WINDOW_HEIGHT)
        ]
        # 山の描画（薄い青色）
        if any(-100 <= p[0] <= WINDOW_WIDTH + 100 for p in mountain_points):
            pygame.draw.polygon(screen, (200, 220, 255), mountain_points)
        
        # 地面（草原）
        grass_color = (100, 200, 100)
        pygame.draw.rect(screen, grass_color, (0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50))
        
        # 道路
        road_color = (80, 80, 80)
        pygame.draw.rect(screen, road_color, (0, WINDOW_HEIGHT - 30, WINDOW_WIDTH, 20))
        
        # 道路の中央線
        for i in range(0, WINDOW_WIDTH + 1000, 50):
            line_x = i - (camera_x % 50)
            if 0 <= line_x <= WINDOW_WIDTH:
                pygame.draw.rect(screen, (255, 255, 255), (line_x, WINDOW_HEIGHT - 20, 30, 3))
        
        # 木（家の後ろに描画）
        for tree in self.trees:
            x, y, size = tree
            tree_x = x - camera_x
            if -size <= tree_x <= WINDOW_WIDTH:
                # 幹
                trunk_width = size // 5
                trunk_height = size // 2
                pygame.draw.rect(screen, (101, 67, 33), (tree_x - trunk_width // 2, y - trunk_height, trunk_width, trunk_height))
                # 葉（複数の円で表現）
                leaf_color = (34, 139, 34)  # 濃い緑
                pygame.draw.circle(screen, leaf_color, (int(tree_x), int(y - trunk_height - size // 3)), size // 2)
                pygame.draw.circle(screen, leaf_color, (int(tree_x - size // 4), int(y - trunk_height - size // 4)), size // 3)
                pygame.draw.circle(screen, leaf_color, (int(tree_x + size // 4), int(y - trunk_height - size // 4)), size // 3)
        
        # 家
        for house_data in self.houses:
            x, y, width, height, house_color_idx, roof_color_idx, has_chimney = house_data
            house_rect = pygame.Rect(x - camera_x, y, width, height)
            
            if -width <= house_rect.x <= WINDOW_WIDTH:  # 画面内の家のみ描画
                # 家の本体
                house_color = self.house_colors[house_color_idx]
                pygame.draw.rect(screen, house_color, house_rect)
                
                # 屋根
                roof_color = self.roof_colors[roof_color_idx]
                roof_points = [
                    (house_rect.left, house_rect.top),
                    (house_rect.left + house_rect.width // 2, house_rect.top - 40),
                    (house_rect.right, house_rect.top)
                ]
                pygame.draw.polygon(screen, roof_color, roof_points)
                
                # 煙突（一部の家のみ）
                if has_chimney:
                    chimney_x = house_rect.right - house_rect.width // 4
                    chimney_y = house_rect.top - 20
                    chimney_width = house_rect.width // 10
                    chimney_height = 30
                    pygame.draw.rect(screen, (160, 82, 45), (chimney_x, chimney_y - chimney_height, chimney_width, chimney_height))
                    # 煙（小さな円の集まり）
                    for i in range(3):
                        smoke_y = chimney_y - chimney_height - 10 - i * 15
                        smoke_x = chimney_x + chimney_width // 2 + (i % 2) * 5
                        smoke_size = 5 + i * 2
                        pygame.draw.circle(screen, (220, 220, 220), (smoke_x, smoke_y), smoke_size)
                
                # 窓（複数）
                window_color = (173, 216, 230)  # 水色
                window_width = house_rect.width // 5
                window_height = house_rect.height // 6
                
                # 上段の窓
                pygame.draw.rect(screen, window_color, (house_rect.left + house_rect.width // 4 - window_width // 2, 
                                                       house_rect.top + house_rect.height // 4, window_width, window_height))
                pygame.draw.rect(screen, window_color, (house_rect.right - house_rect.width // 4 - window_width // 2, 
                                                       house_rect.top + house_rect.height // 4, window_width, window_height))
                
                # 窓の格子
                for window_x in [house_rect.left + house_rect.width // 4 - window_width // 2, 
                                house_rect.right - house_rect.width // 4 - window_width // 2]:
                    pygame.draw.line(screen, house_color, (window_x + window_width // 2, house_rect.top + house_rect.height // 4),
                                    (window_x + window_width // 2, house_rect.top + house_rect.height // 4 + window_height), 2)
                    pygame.draw.line(screen, house_color, (window_x, house_rect.top + house_rect.height // 4 + window_height // 2),
                                    (window_x + window_width, house_rect.top + house_rect.height // 4 + window_height // 2), 2)
                
                # ドア
                door_width = house_rect.width // 3
                door_height = house_rect.height // 2
                door_x = house_rect.left + (house_rect.width - door_width) // 2
                door_y = house_rect.bottom - door_height
                
                door_color = (101, 67, 33)  # 茶色
                pygame.draw.rect(screen, door_color, (door_x, door_y, door_width, door_height))
                
                # ドアノブ
                doorknob_x = door_x + door_width - door_width // 6
                doorknob_y = door_y + door_height // 2
                pygame.draw.circle(screen, (255, 215, 0), (doorknob_x, doorknob_y), 3)
        
        # 街灯
        for light in self.streetlights:
            x, y = light
            light_x = x - camera_x
            if -20 <= light_x <= WINDOW_WIDTH:
                # 支柱
                pygame.draw.rect(screen, (50, 50, 50), (light_x - 3, y - 80, 6, 80))
                # ランプ部分
                pygame.draw.circle(screen, (255, 255, 200), (light_x, y - 80), 10)
                pygame.draw.circle(screen, (255, 255, 150), (light_x, y - 80), 5)
        
        # 前景の草（装飾）
        for i in range(0, WINDOW_WIDTH + 100, 20):
            grass_x = i - (camera_x % 20)
            if 0 <= grass_x <= WINDOW_WIDTH:
                grass_height = random.randint(5, 15)
                pygame.draw.line(screen, (50, 150, 50), (grass_x, WINDOW_HEIGHT - 50), 
                                (grass_x, WINDOW_HEIGHT - 50 - grass_height), 2)

def main():
    clock = pygame.time.Clock()
    cat = Cat()
    background = Background()
    goal = Goal()
    camera_x = 0
    game_clear = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not game_clear:
                    cat.jump()

        if not game_clear:
            # キー入力の処理
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                cat.rect.x += cat.speed
                camera_x = cat.rect.x - 100  # カメラは猫の位置に追従

            # 猫の移動処理
            cat.move()

            # ゴール判定
            if cat.rect.x >= goal.x:
                game_clear = True

        # 描画
        background.draw(screen, camera_x)
        goal.draw(screen, camera_x)
        # 猫の描画
        cat.draw(screen, camera_x)

        # ゲームクリア時のメッセージ表示
        if game_clear:
            # 英語のメッセージをフォールバックとして用意
            clear_text = font.render("Welcome Home!", True, (255, 215, 0))
            
            # 日本語フォントが利用可能かテスト
            test_text = font.render("あ", True, (255, 215, 0))
            test_width = test_text.get_width()
            
            # 日本語が正しく描画できる場合（幅が0より大きい）
            if test_width > 0:
                clear_text = font.render("おかえり！", True, (255, 215, 0))
                
            text_rect = clear_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(clear_text, text_rect)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
