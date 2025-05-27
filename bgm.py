import pygame
import numpy as np
import time
from pygame.sndarray import make_sound

# Pygameの初期化
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# 音階の周波数（ドレミファソラシド）
NOTES = {
    'C4': 261.63,  # ド
    'D4': 293.66,  # レ
    'E4': 329.63,  # ミ
    'F4': 349.23,  # ファ
    'G4': 392.00,  # ソ
    'A4': 440.00,  # ラ
    'B4': 493.88,  # シ
    'C5': 523.25,  # 高いド
    'D5': 587.33,  # 高いレ
    'E5': 659.25,  # 高いミ
    'F5': 698.46,  # 高いファ
    'G5': 783.99,  # 高いソ
    'A5': 880.00,  # 高いラ
    'B5': 987.77,  # 高いシ
    'C6': 1046.50  # さらに高いド
}

# サンプリングレート
SAMPLE_RATE = 44100

def generate_sine_wave(freq, duration, volume=0.5):
    """指定された周波数、長さ、音量のサイン波を生成する"""
    num_samples = int(SAMPLE_RATE * duration)
    # サイン波を生成
    samples = np.sin(2 * np.pi * np.arange(num_samples) * freq / SAMPLE_RATE)
    # 音量調整
    samples = samples * volume
    # 16ビット整数に変換
    samples = (samples * 32767).astype(np.int16)
    return samples

def create_note(note, duration, volume=0.5, fade_in=0.1, fade_out=0.1):
    """音符を生成する（フェードイン/アウト付き）"""
    if note in NOTES:
        freq = NOTES[note]
        samples = generate_sine_wave(freq, duration, volume)
        
        # フェードイン/アウト用のサンプル数を計算
        fade_in_samples = int(SAMPLE_RATE * fade_in)
        fade_out_samples = int(SAMPLE_RATE * fade_out)
        
        # フェードイン
        if fade_in_samples > 0:
            fade_in_curve = np.linspace(0, 1, fade_in_samples)
            samples[:fade_in_samples] = samples[:fade_in_samples] * fade_in_curve
        
        # フェードアウト
        if fade_out_samples > 0:
            fade_out_curve = np.linspace(1, 0, fade_out_samples)
            samples[-fade_out_samples:] = samples[-fade_out_samples:] * fade_out_curve
        
        # ステレオに変換
        stereo_samples = np.column_stack((samples, samples))
        return stereo_samples
    return None

def create_melody(notes, durations, volumes=None, tempo=1.0):
    """メロディーを生成する"""
    if volumes is None:
        volumes = [0.5] * len(notes)
    
    all_samples = np.array([], dtype=np.int16).reshape(0, 2)
    
    for note, duration, volume in zip(notes, durations, volumes):
        if note == 'REST':
            # 休符の場合は無音を追加
            num_samples = int(SAMPLE_RATE * duration / tempo)
            silence = np.zeros((num_samples, 2), dtype=np.int16)
            all_samples = np.vstack((all_samples, silence))
        else:
            # 音符の場合はサンプルを生成して追加
            note_samples = create_note(note, duration / tempo, volume)
            if note_samples is not None:
                all_samples = np.vstack((all_samples, note_samples))
    
    return all_samples

def create_relaxing_bgm():
    """ほのぼのとした落ち着いたBGMを生成する"""
    # メロディーパート
    melody_notes = [
        'G4', 'E4', 'G4', 'A4', 'G4', 'E4', 'D4', 'E4',
        'G4', 'E4', 'G4', 'A4', 'G4', 'REST', 'G4', 'A4',
        'C5', 'B4', 'A4', 'G4', 'E4', 'D4', 'E4', 'G4',
        'E4', 'D4', 'C4', 'D4', 'E4', 'G4', 'A4', 'G4'
    ]
    
    melody_durations = [
        0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
        0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5,
        0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
        0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0
    ]
    
    melody_volumes = [
        0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4,
        0.4, 0.4, 0.4, 0.4, 0.4, 0.0, 0.4, 0.4,
        0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4,
        0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4
    ]
    
    # テンポ（数値が大きいほど遅くなる）
    tempo = 1.8
    
    # メロディーを生成
    melody_samples = create_melody(melody_notes, melody_durations, melody_volumes, tempo)
    
    # 伴奏パート（シンプルなコード進行）
    accompaniment_notes = []
    accompaniment_durations = []
    accompaniment_volumes = []
    
    # 伴奏のコード（C, G, Am, F の繰り返し）
    chords = [
        ['C4', 'E4', 'G4'],  # Cメジャー
        ['G3', 'B3', 'D4'],  # Gメジャー
        ['A3', 'C4', 'E4'],  # Aマイナー
        ['F3', 'A3', 'C4']   # Fメジャー
    ]
    
    # 各コードを2小節ずつ繰り返す
    for _ in range(2):
        for chord in chords:
            for note in chord:
                accompaniment_notes.append(note)
                accompaniment_durations.append(2.0)  # 2拍分の長さ
                accompaniment_volumes.append(0.2)    # メロディーより小さい音量
    
    # 伴奏を生成
    accompaniment_samples = create_melody(accompaniment_notes, accompaniment_durations, accompaniment_volumes, tempo)
    
    # メロディーと伴奏を合成（長さを合わせる）
    min_length = min(len(melody_samples), len(accompaniment_samples))
    combined_samples = melody_samples[:min_length] + accompaniment_samples[:min_length]
    
    # 音量を調整
    combined_samples = np.clip(combined_samples, -32767, 32767).astype(np.int16)
    
    # サウンドオブジェクトを作成
    sound = pygame.sndarray.make_sound(combined_samples)
    
    return sound

# テスト用コード
if __name__ == "__main__":
    pygame.init()
    bgm = create_relaxing_bgm()
    print("BGM created successfully!")
    bgm.play(loops=-1)
    print("Playing BGM... Press Ctrl+C to stop")
    try:
        # 10秒間再生
        time.sleep(10)
    except KeyboardInterrupt:
        pass
    pygame.quit()
