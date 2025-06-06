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
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

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
    small_font = pygame.font.Font(FONT_PATH, 36)  # ゲームオーバー用の小さいフォント
except Exception as e:
    print(f"Warning: Error loading Japanese font: {e}")
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

# 色の定義
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
RED = (255, 0, 0)

# ゲームの状態
GAME_PLAYING = 0
GAME_CLEAR = 1
GAME_OVER = 2
# 障害物クラス
class Obstacle:
    def __init__(self, x, y, is_rushing=False):
        self.width = 20
        self.height = 30
        self.x = x
        self.y = y - self.height  # 地面からの高さを調整
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # 突進機能の追加
        self.is_rushing = is_rushing  # この個体が突進するかどうか
        self.rushing_range = 300  # この距離内に猫がいると突進開始（200から300に変更）
        self.rushing_speed = 8  # 突進時の速度
        self.is_currently_rushing = False  # 現在突進中かどうか
        self.rush_cooldown = 0  # 突進後のクールダウン
        self.max_cooldown = 60  # 突進後のクールダウン時間（フレーム数）
    
    def update(self, cat_x=None, cat_y=None):
        # 突進機能がある場合、猫との距離をチェック
        if self.is_rushing and cat_x is not None and cat_y is not None:
            # クールダウン中なら何もしない
            if self.rush_cooldown > 0:
                self.rush_cooldown -= 1
                return
                
            distance_x = cat_x - self.x
            distance_y = cat_y - self.y
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
            
            # 突進範囲内かつ猫が左側から近づいてきた場合、または既に突進中の場合は突進を続ける
            if (distance < self.rushing_range and distance_x < 0) or self.is_currently_rushing:
                self.is_currently_rushing = True
                
                # 左方向に突進（猫の反対方向）- 速度を大幅に上げる
                self.x -= 15  # 突進速度を15に増加（元の約2倍）
                
                # 一定距離突進したらクールダウンに入る
                if cat_x - self.x > 300:  # 猫から300ピクセル以上離れたら停止
                    self.is_currently_rushing = False
                    self.rush_cooldown = self.max_cooldown
                
                # 矩形の更新
                self.rect.x = self.x
                return
            else:
                self.is_currently_rushing = False
    
    def draw(self, screen, camera_x):
        # 画面上の描画位置を計算
        screen_x = self.x - camera_x
        
        # 画面内にある場合のみ描画
        if -self.width <= screen_x <= WINDOW_WIDTH:
            # 空き缶の本体（シルバー）
            can_color = (192, 192, 192)
            
            # 突進中の空き缶は色を変える（より鮮明な赤色）とマッチョになる
            if self.is_currently_rushing:
                can_color = (255, 100, 100)  # より鮮明な赤色に変更
                
                # 突進中は缶を少し大きく表示（マッチョな体型）
                width_boost = 10
                height_boost = 5
                body_rect = pygame.Rect(screen_x - width_boost/2, self.y - height_boost/2, 
                                      self.width + width_boost, self.height + height_boost)
                pygame.draw.rect(screen, can_color, body_rect)
                
                # 筋肉の表現（胸筋）
                muscle_color = (220, 80, 80)  # 筋肉の色（赤みがかった色）
                pygame.draw.arc(screen, muscle_color, 
                               (screen_x, self.y + 5, self.width/2, self.height/2), 
                               math.pi*0.5, math.pi*1.5, 3)
                pygame.draw.arc(screen, muscle_color, 
                               (screen_x + self.width/2, self.y + 5, self.width/2, self.height/2), 
                               math.pi*1.5, math.pi*2.5, 3)
                
                # 腹筋の表現
                for i in range(3):
                    pygame.draw.line(screen, muscle_color,
                                    (screen_x + 5, self.y + self.height/2 + i*5),
                                    (screen_x + self.width - 5, self.y + self.height/2 + i*5),
                                    2)
                
                # 突進エフェクト（後ろに残像）
                for i in range(1, 4):
                    alpha = 150 - i * 40  # 徐々に薄くなる
                    if alpha > 0:
                        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                        s.fill((255, 100, 100, alpha))
                        screen.blit(s, (screen_x + i * 5, self.y))
                
                # 「パワー！！！」の吹き出しを表示
                # 吹き出しの背景（白い楕円）
                bubble_width = 80
                bubble_height = 30
                bubble_x = screen_x - bubble_width // 2
                bubble_y = self.y - bubble_height - 10
                
                # 吹き出しの背景
                pygame.draw.ellipse(screen, (255, 255, 255), 
                                   (bubble_x, bubble_y, bubble_width, bubble_height))
                
                # 吹き出しの枠線
                pygame.draw.ellipse(screen, (0, 0, 0), 
                                   (bubble_x, bubble_y, bubble_width, bubble_height), 2)
                
                # 吹き出しの尻尾
                tail_points = [
                    (bubble_x + bubble_width // 2 - 10, bubble_y + bubble_height - 2),
                    (screen_x + self.width // 2, self.y),
                    (bubble_x + bubble_width // 2 + 10, bubble_y + bubble_height - 2)
                ]
                pygame.draw.polygon(screen, (255, 255, 255), tail_points)
                pygame.draw.polygon(screen, (0, 0, 0), tail_points, 2)
                
                # 「パワー！！！」のテキスト
                try:
                    # 日本語フォントを使用
                    font = pygame.font.Font(FONT_PATH, 14)
                    text = font.render("パワー！！！", True, (0, 0, 0))
                    text_rect = text.get_rect(center=(bubble_x + bubble_width // 2, bubble_y + bubble_height // 2))
                    screen.blit(text, text_rect)
                except Exception:
                    # フォントが読み込めない場合は英語で表示
                    font = pygame.font.Font(None, 14)
                    text = font.render("POWER!!!", True, (0, 0, 0))
                    text_rect = text.get_rect(center=(bubble_x + bubble_width // 2, bubble_y + bubble_height // 2))
                    screen.blit(text, text_rect)
                
                # アニメーションのための時間ベースの値
                time_val = pygame.time.get_ticks() * 0.02
                leg_phase = math.sin(time_val) * 5
                arm_phase = math.cos(time_val) * 5  # 腕は足と逆のタイミングで動く
                
                # 突進中は2本足を生やす
                leg_color = (139, 69, 19)  # 茶色の足
                leg_width = 4
                leg_height = 15
                
                # 左足
                left_leg_x = screen_x + self.width * 0.3
                if leg_phase > 0:
                    # 左足を前に出す
                    pygame.draw.line(screen, leg_color, 
                                    (left_leg_x, self.y + self.height), 
                                    (left_leg_x - 5, self.y + self.height + leg_height), 
                                    leg_width)
                else:
                    # 左足を後ろに引く
                    pygame.draw.line(screen, leg_color, 
                                    (left_leg_x, self.y + self.height), 
                                    (left_leg_x + 5, self.y + self.height + leg_height), 
                                    leg_width)
                
                # 右足
                right_leg_x = screen_x + self.width * 0.7
                if leg_phase <= 0:
                    # 右足を前に出す
                    pygame.draw.line(screen, leg_color, 
                                    (right_leg_x, self.y + self.height), 
                                    (right_leg_x - 5, self.y + self.height + leg_height), 
                                    leg_width)
                else:
                    # 右足を後ろに引く
                    pygame.draw.line(screen, leg_color, 
                                    (right_leg_x, self.y + self.height), 
                                    (right_leg_x + 5, self.y + self.height + leg_height), 
                                    leg_width)
                
                # 足の先（靴のような形）
                pygame.draw.ellipse(screen, (50, 50, 50), 
                                   (left_leg_x - 5 - 3 if leg_phase > 0 else left_leg_x + 5 - 3, 
                                    self.y + self.height + leg_height - 3, 6, 4))
                pygame.draw.ellipse(screen, (50, 50, 50), 
                                   (right_leg_x - 5 - 3 if leg_phase <= 0 else right_leg_x + 5 - 3, 
                                    self.y + self.height + leg_height - 3, 6, 4))
                
                # マッチョな腕を追加
                arm_color = (220, 150, 150)  # 腕の色
                arm_width = 6  # 太い腕
                
                # 左腕（筋肉質）
                left_arm_x = screen_x - 2
                left_arm_y = self.y + self.height * 0.3
                if arm_phase > 0:
                    # 左腕を前に振る
                    pygame.draw.line(screen, arm_color, 
                                    (left_arm_x, left_arm_y), 
                                    (left_arm_x - 15, left_arm_y + 5), 
                                    arm_width)
                    # 二の腕の筋肉表現
                    pygame.draw.ellipse(screen, arm_color, 
                                       (left_arm_x - 12, left_arm_y - 2, 10, 8))
                else:
                    # 左腕を後ろに振る
                    pygame.draw.line(screen, arm_color, 
                                    (left_arm_x, left_arm_y), 
                                    (left_arm_x - 10, left_arm_y + 15), 
                                    arm_width)
                    # 二の腕の筋肉表現
                    pygame.draw.ellipse(screen, arm_color, 
                                       (left_arm_x - 8, left_arm_y + 5, 10, 8))
                
                # 右腕（筋肉質）
                right_arm_x = screen_x + self.width + 2
                right_arm_y = self.y + self.height * 0.3
                if arm_phase <= 0:
                    # 右腕を前に振る
                    pygame.draw.line(screen, arm_color, 
                                    (right_arm_x, right_arm_y), 
                                    (right_arm_x + 15, right_arm_y + 5), 
                                    arm_width)
                    # 二の腕の筋肉表現
                    pygame.draw.ellipse(screen, arm_color, 
                                       (right_arm_x + 2, right_arm_y - 2, 10, 8))
                else:
                    # 右腕を後ろに振る
                    pygame.draw.line(screen, arm_color, 
                                    (right_arm_x, right_arm_y), 
                                    (right_arm_x + 10, right_arm_y + 15), 
                                    arm_width)
                    # 二の腕の筋肉表現
                    pygame.draw.ellipse(screen, arm_color, 
                                       (right_arm_x - 2, right_arm_y + 5, 10, 8))
                
                # 拳（こぶし）
                pygame.draw.circle(screen, (220, 150, 150), 
                                  (left_arm_x - 15 if arm_phase > 0 else left_arm_x - 10, 
                                   left_arm_y + 5 if arm_phase > 0 else left_arm_y + 15), 5)
                pygame.draw.circle(screen, (220, 150, 150), 
                                  (right_arm_x + 15 if arm_phase <= 0 else right_arm_x + 10, 
                                   right_arm_y + 5 if arm_phase <= 0 else right_arm_y + 15), 5)
                
                # 顔の表情（怒った表情）
                # 目
                eye_color = (255, 255, 255)  # 白目
                pygame.draw.circle(screen, eye_color, (screen_x + self.width * 0.3, self.y + 8), 4)
                pygame.draw.circle(screen, eye_color, (screen_x + self.width * 0.7, self.y + 8), 4)
                
                # 黒目（怒った感じに）
                pygame.draw.circle(screen, (0, 0, 0), (screen_x + self.width * 0.3 - 1, self.y + 8), 2)
                pygame.draw.circle(screen, (0, 0, 0), (screen_x + self.width * 0.7 - 1, self.y + 8), 2)
                
                # 眉毛（怒った表情）
                pygame.draw.line(screen, (0, 0, 0), 
                                (screen_x + self.width * 0.2, self.y + 4), 
                                (screen_x + self.width * 0.4, self.y + 6), 2)
                pygame.draw.line(screen, (0, 0, 0), 
                                (screen_x + self.width * 0.6, self.y + 6), 
                                (screen_x + self.width * 0.8, self.y + 4), 2)
                
                # 口（怒った表情）
                pygame.draw.arc(screen, (0, 0, 0), 
                               (screen_x + self.width * 0.3, self.y + 12, self.width * 0.4, 8), 
                               math.pi, math.pi * 2, 2)
                
            else:
                # 通常時は普通のサイズで描画
                pygame.draw.rect(screen, can_color, (screen_x, self.y, self.width, self.height))
            
            # 缶の上部（赤）
            top_color = (220, 50, 50)
            if self.is_currently_rushing:
                top_color = (255, 0, 0)  # 突進中はより鮮やかな赤に
            pygame.draw.rect(screen, top_color, (screen_x, self.y, self.width, 5))
            
            # 缶の模様（簡易的なデザイン）- 突進中は筋肉で隠れるので通常時のみ
            if not self.is_currently_rushing:
                pattern_color = (100, 100, 100)
                pygame.draw.rect(screen, pattern_color, (screen_x, self.y + self.height // 2 - 5, self.width, 10))
            
            # 缶の影
            shadow_color = (100, 100, 100)
            if self.is_currently_rushing:
                shadow_color = (150, 50, 50)  # 突進中は赤っぽく
            pygame.draw.ellipse(screen, shadow_color, (screen_x - 2, self.y + self.height - 3, self.width + 4, 6))

# カラス障害物クラス
class CrowObstacle:
    def __init__(self, x, y, is_tracking=False):
        self.width = 30
        self.height = 25
        self.x = x
        self.y = y
        self.base_y = y  # 初期Y座標を保存
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.movement_speed = 1
        self.movement_range = 40
        self.movement_counter = random.randint(0, 100)  # ランダムな初期位置
        
        # 追尾機能の追加
        self.is_tracking = is_tracking  # この個体が追尾するかどうか
        self.tracking_range = 300  # この距離内に猫がいると追尾開始
        self.tracking_speed = 2  # 追尾時の速度
        self.is_currently_tracking = False  # 現在追尾中かどうか
    
    def update(self, cat_x=None, cat_y=None):
        # 追尾機能がある場合、猫との距離をチェック
        if self.is_tracking and cat_x is not None and cat_y is not None:
            distance_x = cat_x - self.x
            distance_y = cat_y - self.y
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
            
            # 追尾範囲内なら追尾モードに
            if distance < self.tracking_range:
                self.is_currently_tracking = True
                
                # 猫の方向へ移動（X軸）
                if distance_x > 0:
                    self.x += self.tracking_speed
                elif distance_x < 0:
                    self.x -= self.tracking_speed
                
                # 猫の方向へ移動（Y軸）- 少し緩やかに
                if distance_y > 0:
                    self.y += self.tracking_speed * 0.7
                elif distance_y < 0:
                    self.y -= self.tracking_speed * 0.7
                
                # 矩形の更新
                self.rect.x = self.x
                self.rect.y = self.y
                return
            else:
                self.is_currently_tracking = False
        
        # 追尾していない場合は通常の上下動作
        self.movement_counter += 1
        # 動きの範囲を大きくして、地面すれすれまで下がるように調整
        ground_level = WINDOW_HEIGHT - 40  # 地面の少し上
        max_height = self.base_y - 100  # 最高高度
        
        # 動きの振幅を大きくし、地面すれすれまで下がるようにする
        height_range = ground_level - max_height
        offset = math.sin(self.movement_counter * 0.03) * (height_range / 2)
        mid_point = (ground_level + max_height) / 2
        
        self.y = mid_point + offset
        self.rect.y = self.y
    
    def draw(self, screen, camera_x):
        # 画面上の描画位置を計算
        screen_x = self.x - camera_x
        
        # 画面内にある場合のみ描画
        if -self.width <= screen_x <= WINDOW_WIDTH:
            # カラスの体（黒）
            body_color = (20, 20, 20)
            
            # 追尾中のカラスは色を変える（濃い赤色）
            if self.is_currently_tracking:
                body_color = (180, 0, 0)  # より濃い赤色に変更
                
            pygame.draw.ellipse(screen, body_color, (screen_x, self.y, self.width, self.height))
            
            # カラスの頭
            head_radius = 10
            pygame.draw.circle(screen, body_color, (screen_x + self.width - 5, self.y + 10), head_radius)
            
            # くちばし（オレンジ）
            beak_points = [
                (screen_x + self.width + 5, self.y + 10),
                (screen_x + self.width + 15, self.y + 12),
                (screen_x + self.width + 5, self.y + 14)
            ]
            pygame.draw.polygon(screen, (255, 165, 0), beak_points)
            
            # 目（白）
            pygame.draw.circle(screen, (255, 255, 255), (screen_x + self.width, self.y + 7), 3)
            
            # 目の色を変える（追尾中は赤い目に）
            eye_color = (0, 0, 0)
            if self.is_currently_tracking:
                eye_color = (255, 0, 0)
            pygame.draw.circle(screen, eye_color, (screen_x + self.width, self.y + 7), 1)  # 瞳
            
            # 翼（飛んでいる表現）
            wing_y = self.y + self.height // 2
            wing_height = 10
            wing_phase = math.sin(self.movement_counter * 0.2) * 5
            
            # 左翼
            left_wing_points = [
                (screen_x + 5, wing_y),
                (screen_x - 15, wing_y - wing_height - wing_phase),
                (screen_x - 5, wing_y + 5)
            ]
            pygame.draw.polygon(screen, body_color, left_wing_points)
            
            # 右翼
            right_wing_points = [
                (screen_x + self.width - 10, wing_y),
                (screen_x + self.width + 15, wing_y - wing_height + wing_phase),
                (screen_x + self.width - 5, wing_y + 5)
            ]
            pygame.draw.polygon(screen, body_color, right_wing_points)
            
            # 追尾中は「まてーー！」の吹き出しを表示
            if self.is_currently_tracking:
                # 吹き出しの背景（白い楕円）
                bubble_width = 70
                bubble_height = 30
                bubble_x = screen_x + self.width - bubble_width // 2
                bubble_y = self.y - bubble_height - 5
                
                # 吹き出しの背景
                pygame.draw.ellipse(screen, (255, 255, 255), 
                                   (bubble_x, bubble_y, bubble_width, bubble_height))
                
                # 吹き出しの枠線
                pygame.draw.ellipse(screen, (0, 0, 0), 
                                   (bubble_x, bubble_y, bubble_width, bubble_height), 2)
                
                # 吹き出しの尻尾
                tail_points = [
                    (bubble_x + bubble_width // 2, bubble_y + bubble_height - 2),
                    (screen_x + self.width, self.y),
                    (bubble_x + bubble_width // 2 + 15, bubble_y + bubble_height - 2)
                ]
                pygame.draw.polygon(screen, (255, 255, 255), tail_points)
                pygame.draw.polygon(screen, (0, 0, 0), tail_points, 2)
                
                # 「まてーー！」のテキスト
                try:
                    # 日本語フォントを使用
                    font = pygame.font.Font(FONT_PATH, 14)
                    text = font.render("まてーー！", True, (0, 0, 0))
                    text_rect = text.get_rect(center=(bubble_x + bubble_width // 2, bubble_y + bubble_height // 2))
                    screen.blit(text, text_rect)
                except Exception:
                    # フォントが読み込めない場合は英語で表示
                    font = pygame.font.Font(None, 14)
                    text = font.render("Wait!!", True, (0, 0, 0))
                    text_rect = text.get_rect(center=(bubble_x + bubble_width // 2, bubble_y + bubble_height // 2))
                    screen.blit(text, text_rect)
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
        self.width = 150  # 家の幅
        self.height = 200  # 家の高さ
        self.x = WINDOW_WIDTH * 4 - 300  # 画面の4倍の位置にゴールを設置
        self.y = WINDOW_HEIGHT - self.height - 50  # 地面より少し上に配置
        
        # ドアの位置とサイズ（家の中央下部）
        self.door_width = 50
        self.door_height = 80
        self.door_x = self.x + (self.width - self.door_width) // 2
        self.door_y = self.y + self.height - self.door_height
        
        # 当たり判定用のドアの矩形
        self.door_rect = pygame.Rect(self.door_x, self.door_y, self.door_width, self.door_height)
        
        # 飼い主さんのアニメーション用の変数
        self.owner_animation_counter = 0
        self.owner_wave_direction = 1  # 手を振る方向（1: 上がる, -1: 下がる）

    def draw(self, screen, camera_x):
        # カメラの位置を考慮して家を描画
        house_x = self.x - camera_x
        house_y = self.y
        
        # 家の本体（灰色に変更）
        house_rect = pygame.Rect(house_x, house_y, self.width, self.height)
        pygame.draw.rect(screen, (180, 180, 180), house_rect)
        
        # 屋根（茶色）
        roof_points = [
            (house_x, house_y),
            (house_x + self.width // 2, house_y - 60),
            (house_x + self.width, house_y)
        ]
        pygame.draw.polygon(screen, (139, 69, 19), roof_points)
        
        # 窓（上段）
        window_width = 40
        window_height = 50
        window_margin = 20
        
        # 左の窓
        left_window_x = house_x + window_margin
        left_window_y = house_y + window_margin
        pygame.draw.rect(screen, (173, 216, 230), (left_window_x, left_window_y, window_width, window_height))
        
        # 窓の格子（左）
        pygame.draw.line(screen, (245, 222, 179), (left_window_x + window_width // 2, left_window_y),
                         (left_window_x + window_width // 2, left_window_y + window_height), 2)
        pygame.draw.line(screen, (245, 222, 179), (left_window_x, left_window_y + window_height // 2),
                         (left_window_x + window_width, left_window_y + window_height // 2), 2)
        
        # 右の窓
        right_window_x = house_x + self.width - window_width - window_margin
        right_window_y = house_y + window_margin
        pygame.draw.rect(screen, (173, 216, 230), (right_window_x, right_window_y, window_width, window_height))
        
        # 窓の格子（右）
        pygame.draw.line(screen, (245, 222, 179), (right_window_x + window_width // 2, right_window_y),
                         (right_window_x + window_width // 2, right_window_y + window_height), 2)
        pygame.draw.line(screen, (245, 222, 179), (right_window_x, right_window_y + window_height // 2),
                         (right_window_x + window_width, right_window_y + window_height // 2), 2)
        
        # 煙突
        chimney_width = 20
        chimney_height = 40
        chimney_x = house_x + self.width - 40
        chimney_y = house_y - 20
        pygame.draw.rect(screen, (160, 82, 45), (chimney_x, chimney_y - chimney_height, chimney_width, chimney_height))
        
        # 煙
        for i in range(3):
            smoke_y = chimney_y - chimney_height - 10 - i * 15
            smoke_x = chimney_x + chimney_width // 2 + (i % 2) * 5
            smoke_size = 5 + i * 2
            pygame.draw.circle(screen, (220, 220, 220), (smoke_x, smoke_y), smoke_size)
        
        # ドア（玄関扉）- ゴールの判定に使用
        door_x = self.door_x - camera_x
        door_y = self.door_y
        
        # ドアの枠（茶色）
        door_frame = pygame.Rect(door_x - 5, door_y - 5, self.door_width + 10, self.door_height + 5)
        pygame.draw.rect(screen, (139, 69, 19), door_frame)
        
        # ドア本体（赤茶色）
        door_rect = pygame.Rect(door_x, door_y, self.door_width, self.door_height)
        pygame.draw.rect(screen, (165, 42, 42), door_rect)
        
        # ドアノブ（金色）
        doorknob_x = door_x + self.door_width - 10
        doorknob_y = door_y + self.door_height // 2
        pygame.draw.circle(screen, (255, 215, 0), (doorknob_x, doorknob_y), 5)
        
        # 玄関マット
        mat_rect = pygame.Rect(door_x - 5, door_y + self.door_height, self.door_width + 10, 10)
        pygame.draw.rect(screen, (50, 205, 50), mat_rect)
        
        # 家の周りの装飾
        
        # 左側の植木鉢
        pot_width = 20
        pot_height = 25
        pot_x = house_x - pot_width - 10
        pot_y = house_y + self.height - pot_height
        pygame.draw.rect(screen, (160, 82, 45), (pot_x, pot_y, pot_width, pot_height))
        
        # 植木鉢の植物
        plant_color = (34, 139, 34)
        pygame.draw.circle(screen, plant_color, (pot_x + pot_width // 2, pot_y - 10), 15)
        
        # 右側の植木鉢
        pot_x = house_x + self.width + 10
        pygame.draw.rect(screen, (160, 82, 45), (pot_x, pot_y, pot_width, pot_height))
        pygame.draw.circle(screen, plant_color, (pot_x + pot_width // 2, pot_y - 10), 15)
        
        # 郵便ポスト
        mailbox_width = 15
        mailbox_height = 30
        mailbox_x = house_x - 40
        mailbox_y = house_y + self.height - mailbox_height
        pygame.draw.rect(screen, (70, 130, 180), (mailbox_x, mailbox_y, mailbox_width, mailbox_height))
        pygame.draw.rect(screen, (50, 50, 50), (mailbox_x + mailbox_width // 2 - 2, mailbox_y + mailbox_height, 4, 20))
        
        # 飼い主さんを描画（ドアの前に立っている）
        owner_x = door_x - 30
        owner_y = WINDOW_HEIGHT - 50  # 地面に立っているように調整
        
        # アニメーションカウンターの更新
        self.owner_animation_counter += 1
        if self.owner_animation_counter >= 30:
            self.owner_animation_counter = 0
            self.owner_wave_direction *= -1
        
        # 手を振るアニメーション（上下に動く）
        arm_wave_offset = self.owner_animation_counter // 3 * self.owner_wave_direction
        
        # 頭（より自然な形状の楕円）
        head_radius = 12
        pygame.draw.ellipse(screen, (255, 218, 185), (owner_x - head_radius, owner_y - 65, head_radius * 2, head_radius * 2 + 2))
        # 顔の輪郭をはっきりさせる
        pygame.draw.ellipse(screen, (0, 0, 0), (owner_x - head_radius, owner_y - 65, head_radius * 2, head_radius * 2 + 2), 1)
        
        # 髪の毛（黒色に変更）
        hair_color = (0, 0, 0)  # 黒色の髪
        pygame.draw.arc(screen, hair_color, (owner_x - head_radius - 2, owner_y - 65 - 2, head_radius * 2 + 4, head_radius * 2 + 4), 3.14, 6.28, 3)
        pygame.draw.line(screen, hair_color, (owner_x - head_radius, owner_y - 60), (owner_x - head_radius, owner_y - 50), 2)
        pygame.draw.line(screen, hair_color, (owner_x + head_radius, owner_y - 60), (owner_x + head_radius, owner_y - 50), 2)
        
        # 首
        neck_height = 5
        pygame.draw.rect(screen, (255, 218, 185), (owner_x - 3, owner_y - 50, 6, neck_height))
        
        # 体（より自然な形状）
        body_width = 24
        body_height = 35
        pygame.draw.rect(screen, (30, 144, 255), (owner_x - body_width // 2, owner_y - 45, body_width, body_height))  # 上半身（シャツ）
        
        # 下半身（ズボンやスカート）
        pants_color = (0, 0, 139)  # 濃い青
        pygame.draw.rect(screen, pants_color, (owner_x - body_width // 2, owner_y - 45 + body_height, body_width, 15))
        
        # 足（より自然な形状）
        leg_width = 6
        leg_height = 30
        pygame.draw.rect(screen, (255, 218, 185), (owner_x - body_width // 2 + 3, owner_y - 45 + body_height + 15, leg_width, leg_height))  # 左足
        pygame.draw.rect(screen, (255, 218, 185), (owner_x + body_width // 2 - 3 - leg_width, owner_y - 45 + body_height + 15, leg_width, leg_height))  # 右足
        
        # 靴
        shoe_color = (0, 0, 0)  # 黒
        pygame.draw.ellipse(screen, shoe_color, (owner_x - body_width // 2 + 2, owner_y - 45 + body_height + 15 + leg_height - 3, leg_width + 2, 6))  # 左靴
        pygame.draw.ellipse(screen, shoe_color, (owner_x + body_width // 2 - 4 - leg_width, owner_y - 45 + body_height + 15 + leg_height - 3, leg_width + 2, 6))  # 右靴
        
        # 腕（より自然な形状）
        arm_width = 5
        arm_length = 20
        
        # 左腕
        pygame.draw.rect(screen, (255, 218, 185), (owner_x - body_width // 2 - arm_width, owner_y - 40, arm_width, arm_length))
        # 左手
        pygame.draw.circle(screen, (255, 218, 185), (owner_x - body_width // 2 - arm_width + arm_width // 2, owner_y - 40 + arm_length), 4)
        
        # 右腕（アニメーション付き）
        arm_angle = 0.3 - 0.2 * (arm_wave_offset / 10)  # 腕の角度（ラジアン）
        arm_end_x = owner_x + body_width // 2 + arm_length * math.cos(arm_angle)
        arm_end_y = owner_y - 40 + arm_length * math.sin(arm_angle)
        
        # 右腕の描画（回転を考慮）
        pygame.draw.line(screen, (255, 218, 185), (owner_x + body_width // 2, owner_y - 40), (arm_end_x, arm_end_y), arm_width)
        # 右手
        pygame.draw.circle(screen, (255, 218, 185), (int(arm_end_x), int(arm_end_y)), 4)
        
        # 顔のパーツ（より詳細に）
        eye_y = owner_y - 60
        
        # 目
        pygame.draw.ellipse(screen, (255, 255, 255), (owner_x - 7, eye_y - 2, 5, 4))  # 左目の白目
        pygame.draw.ellipse(screen, (255, 255, 255), (owner_x + 2, eye_y - 2, 5, 4))  # 右目の白目
        pygame.draw.circle(screen, (50, 50, 150), (owner_x - 5, eye_y), 2)  # 左目の瞳
        pygame.draw.circle(screen, (50, 50, 150), (owner_x + 4, eye_y), 2)  # 右目の瞳
        
        # 眉毛（黒色に変更）
        pygame.draw.line(screen, (0, 0, 0), (owner_x - 8, eye_y - 5), (owner_x - 3, eye_y - 4), 1)  # 左眉
        pygame.draw.line(screen, (0, 0, 0), (owner_x + 2, eye_y - 4), (owner_x + 7, eye_y - 5), 1)  # 右眉
        
        # 口（笑顔）
        pygame.draw.arc(screen, (255, 105, 180), (owner_x - 6, eye_y + 5, 12, 6), 0, 3.14, 2)
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
        
        # 前景の草（装飾）
        for i in range(0, WINDOW_WIDTH + 100, 20):
            grass_x = i - (camera_x % 20)
            if 0 <= grass_x <= WINDOW_WIDTH:
                grass_height = random.randint(5, 15)
                pygame.draw.line(screen, (50, 150, 50), (grass_x, WINDOW_HEIGHT - 50), 
                                (grass_x, WINDOW_HEIGHT - 50 - grass_height), 2)
def main():
    clock = pygame.time.Clock()
    
    # BGMを再生
    try:
        # bgm.pyからBGMを生成
        from bgm import create_relaxing_bgm
        bgm = create_relaxing_bgm()
        bgm.set_volume(0.5)  # 音量を調整（0.0〜1.0）
        bgm.play(loops=-1)  # -1でループ再生
        print("BGM started playing")
    except Exception as e:
        print(f"Warning: Could not play BGM: {e}")
    
    cat = Cat()
    background = Background()
    goal = Goal()
    
    # 障害物を配置（5つの空き缶）- 5番目の空き缶を突進型に変更（ゴール終盤の位置に）
    obstacles = [
        Obstacle(400, WINDOW_HEIGHT - 10),                # 1番目の障害物（通常）
        Obstacle(700, WINDOW_HEIGHT - 10),                # 2番目の障害物（通常）
        Obstacle(1200, WINDOW_HEIGHT - 10),               # 3番目の障害物（通常）
        Obstacle(1800, WINDOW_HEIGHT - 10),               # 4番目の障害物（通常）
        Obstacle(2500, WINDOW_HEIGHT - 10, is_rushing=True),  # 5番目の障害物（突進型）- ゴール終盤の位置
    ]
    
    # カラス障害物を配置（3羽）- 2番目のカラスを追尾型に
    crows = [
        CrowObstacle(900, WINDOW_HEIGHT - 150),                  # 1羽目のカラス（通常）
        CrowObstacle(1500, WINDOW_HEIGHT - 120, is_tracking=True),  # 2羽目のカラス（追尾型）
        CrowObstacle(2200, WINDOW_HEIGHT - 180),                 # 3羽目のカラス（通常）
    ]
    
    camera_x = 0
    game_state = GAME_PLAYING

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game_state == GAME_PLAYING:
                    cat.jump()
                # Rキーでゲームをリセット
                if event.key == pygame.K_r and (game_state == GAME_CLEAR or game_state == GAME_OVER):
                    # ゲームをリセット
                    cat = Cat()
                    camera_x = 0
                    
                    # 障害物を初期位置に戻す
                    obstacles = [
                        Obstacle(400, WINDOW_HEIGHT - 10),                # 1番目の障害物（通常）
                        Obstacle(700, WINDOW_HEIGHT - 10),                # 2番目の障害物（通常）
                        Obstacle(1200, WINDOW_HEIGHT - 10),               # 3番目の障害物（通常）
                        Obstacle(1800, WINDOW_HEIGHT - 10),               # 4番目の障害物（通常）
                        Obstacle(2500, WINDOW_HEIGHT - 10, is_rushing=True),  # 5番目の障害物（突進型）
                    ]
                    
                    # カラスも初期位置に戻す
                    crows = [
                        CrowObstacle(900, WINDOW_HEIGHT - 150),                  # 1羽目のカラス（通常）
                        CrowObstacle(1500, WINDOW_HEIGHT - 120, is_tracking=True),  # 2羽目のカラス（追尾型）
                        CrowObstacle(2200, WINDOW_HEIGHT - 180),                 # 3羽目のカラス（通常）
                    ]
                    
                    game_state = GAME_PLAYING

        if game_state == GAME_PLAYING:
            # キー入力の処理
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                cat.rect.x += cat.speed
                camera_x = cat.rect.x - 100  # カメラは猫の位置に追従

            # 猫の移動処理
            cat.move()
            
            # カラスの更新
            for crow in crows:
                crow.update(cat.rect.x, cat.rect.y)
                
            # 空き缶の更新（突進機能を持つものがあれば）
            for obstacle in obstacles:
                if hasattr(obstacle, 'update'):
                    obstacle.update(cat.rect.x, cat.rect.y)
            
            # 障害物との衝突判定
            cat_rect = pygame.Rect(cat.rect.x, cat.rect.y, cat.width - 20, cat.height)  # 猫の当たり判定を少し小さく
            
            # 空き缶との衝突判定
            for obstacle in obstacles:
                if cat_rect.colliderect(obstacle.rect):
                    game_state = GAME_OVER
                    break
            
            # カラスとの衝突判定
            if game_state == GAME_PLAYING:  # 空き缶との衝突がなかった場合のみ
                for crow in crows:
                    if cat_rect.colliderect(crow.rect):
                        game_state = GAME_OVER
                        break

            # ゴール判定（猫がドアに到達したかどうか）
            if cat.rect.x >= goal.door_x:
                game_state = GAME_CLEAR

        # 描画
        background.draw(screen, camera_x)
        
        # 障害物の描画
        for obstacle in obstacles:
            obstacle.draw(screen, camera_x)
        
        # カラスの描画
        for crow in crows:
            crow.draw(screen, camera_x)
            
        goal.draw(screen, camera_x)
        
        # 猫の描画
        cat.draw(screen, camera_x)

        # ゲームクリア時のメッセージ表示
        if game_state == GAME_CLEAR:
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
            
            # リスタート案内
            restart_text = small_font.render("Press R to Restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
            screen.blit(restart_text, restart_rect)
        
        # ゲームオーバー時のメッセージ表示
        elif game_state == GAME_OVER:
            # 英語のメッセージをフォールバックとして用意
            over_text = font.render("Game Over", True, (255, 0, 0))
            
            # 日本語フォントが利用可能かテスト
            test_text = font.render("あ", True, (255, 0, 0))
            test_width = test_text.get_width()
            
            # 日本語が正しく描画できる場合（幅が0より大きい）
            if test_width > 0:
                over_text = font.render("ゲームオーバー", True, (255, 0, 0))
                
            text_rect = over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(over_text, text_rect)
            
            # リスタート案内
            restart_text = small_font.render("Press R to Restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
