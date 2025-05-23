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
        self.width = 50
        self.height = 50
        self.x = 100
        self.y = WINDOW_HEIGHT - self.height - 10
        self.velocity_y = 0
        self.is_jumping = False
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

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

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 165, 0), self.rect)  # オレンジ色の四角で猫を表現

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
        goal_rect = pygame.Rect(self.x - camera_x, self.y, self.width, self.height)
        pygame.draw.rect(screen, RED, goal_rect)
        # ゴールの旗
        flag_pole = [(self.x - camera_x, self.y), (self.x - camera_x, self.y + self.height)]
        pygame.draw.lines(screen, (255, 255, 255), False, flag_pole, 3)

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
        # 猫の描画位置をカメラに合わせて調整
        cat_screen_pos = pygame.Rect(cat.rect.x - camera_x, cat.rect.y, cat.rect.width, cat.rect.height)
        pygame.draw.rect(screen, (255, 165, 0), cat_screen_pos)

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
