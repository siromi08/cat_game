import pygame
import sys
import os

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
        # 住宅地の背景を表現する簡単な図形
        self.houses = [
            pygame.Rect(100, 400, 100, 150),
            pygame.Rect(300, 350, 120, 200),
            pygame.Rect(500, 380, 150, 170),
            pygame.Rect(700, 420, 90, 130),
            # 追加の家（画面外）
            pygame.Rect(900, 400, 100, 150),
            pygame.Rect(1100, 350, 120, 200),
            pygame.Rect(1300, 380, 150, 170),
            pygame.Rect(1500, 420, 90, 130),
            # さらに追加の家（より遠くに）
            pygame.Rect(1700, 400, 100, 150),
            pygame.Rect(1900, 350, 120, 200),
            pygame.Rect(2100, 380, 150, 170),
            pygame.Rect(2300, 420, 90, 130),
            pygame.Rect(2500, 400, 100, 150),
            pygame.Rect(2700, 350, 120, 200),
            pygame.Rect(2900, 380, 150, 170),
            pygame.Rect(3100, 420, 90, 130),
        ]

    def draw(self, screen, camera_x):
        # 空
        screen.fill(BLUE)
        # 地面
        pygame.draw.rect(screen, (100, 200, 100), (0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10))
        # 家
        for house in self.houses:
            # カメラの位置を考慮して家を描画
            house_rect = pygame.Rect(house.x - camera_x, house.y, house.width, house.height)
            if -house.width <= house_rect.x <= WINDOW_WIDTH:  # 画面内の家のみ描画
                pygame.draw.rect(screen, (200, 200, 200), house_rect)
                # 屋根
                points = [
                    (house_rect.left, house_rect.top),
                    (house_rect.left + house_rect.width // 2, house_rect.top - 30),
                    (house_rect.right, house_rect.top)
                ]
                pygame.draw.polygon(screen, (139, 69, 19), points)

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
