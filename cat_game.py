import pygame
import sys
import os

# ゲームの初期化
pygame.init()

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("猫のゴール冒険")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

# 猫のクラス
class Cat:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = 50
        self.y = HEIGHT // 2
        self.speed = 5
        self.color = (255, 165, 0)  # オレンジ色
    
    def draw(self):
        # 猫の体
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # 猫の耳
        pygame.draw.polygon(screen, self.color, [(self.x, self.y), (self.x + 10, self.y - 15), (self.x + 20, self.y)])
        pygame.draw.polygon(screen, self.color, [(self.x + 20, self.y), (self.x + 30, self.y - 15), (self.x + 40, self.y)])
        # 猫の目
        pygame.draw.circle(screen, BLACK, (self.x + 10, self.y + 15), 5)
        pygame.draw.circle(screen, BLACK, (self.x + 30, self.y + 15), 5)
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.height:
            self.y += self.speed
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# 障害物クラス
class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = BROWN
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# ゴールクラス
class Goal:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = WIDTH - 100
        self.y = HEIGHT - 100
        self.color = GREEN
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # ゴールの旗
        pygame.draw.polygon(screen, RED, [(self.x + 25, self.y), (self.x + 25, self.y - 30), (self.x + 45, self.y - 20), (self.x + 25, self.y - 10)])
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# ゲームオブジェクトの作成
cat = Cat()
goal = Goal()

# 障害物の配置
obstacles = [
    Obstacle(200, 200, 100, 30),
    Obstacle(400, 300, 30, 150),
    Obstacle(500, 100, 30, 200),
    Obstacle(300, 450, 200, 30),
    Obstacle(600, 400, 100, 30)
]

# ゲームループ
clock = pygame.time.Clock()
game_over = False
win = False

def draw_text(text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (win or game_over):
                # リセット
                cat = Cat()
                win = False
                game_over = False
    
    if not win:
        # 入力処理
        keys = pygame.key.get_pressed()
        cat.move(keys)
        
        # 衝突判定
        cat_rect = cat.get_rect()
        
        # 障害物との衝突
        for obstacle in obstacles:
            if cat_rect.colliderect(obstacle.get_rect()):
                game_over = True
        
        # ゴールとの衝突
        if cat_rect.colliderect(goal.get_rect()):
            win = True
    
    # 描画
    screen.fill(BLACK)
    
    # 障害物の描画
    for obstacle in obstacles:
        obstacle.draw()
    
    # ゴールの描画
    goal.draw()
    
    # 猫の描画
    cat.draw()
    
    # ゲームオーバーまたは勝利メッセージ
    if game_over and not win:
        draw_text("ゲームオーバー! Rキーでリスタート", 50, WIDTH // 2, HEIGHT // 2, RED)
    
    if win:
        draw_text("ゴール達成! Rキーでリスタート", 50, WIDTH // 2, HEIGHT // 2, GREEN)
    
    # 操作方法の表示
    draw_text("矢印キーで移動", 30, WIDTH // 2, 30)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
