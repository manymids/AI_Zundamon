import os
import re
import pygame
from pathlib import Path
from voicevox_core import VoicevoxCore

 # TTSマネージャー
class TTSManager:
    WAV_PATH = "./wav/"
    SPEAKER_ID = 23

    def __init__(self, id=23):
        """音声合成に必要なディレクトリとモデルを初期化します。"""
        self.SPEAKER_ID = id
        print(id)
        os.makedirs(self.WAV_PATH, exist_ok=True)
        self.core = VoicevoxCore(open_jtalk_dict_dir=Path("open_jtalk_dic_utf_8-1.11"))
        if not self.core.is_model_loaded(self.SPEAKER_ID):
            self.core.load_model(self.SPEAKER_ID)
        pygame.mixer.init()

    def tts_speak(self, text: str):
        """指定されたテキストを音声合成し再生します。"""
        self.wait_play()
        file_name = self.WAV_PATH + re.sub(r'[<>:"/|?*]', '_', text) +  f"_{self.SPEAKER_ID}.wav"
        if os.path.isfile(file_name):
            self.play_sound(file_name)
            return

        try:
            audio_query = self.core.audio_query(text, self.SPEAKER_ID)
            if self.SPEAKER_ID == 1:
                audio_query.speed_scale = 1.2
            else:
                audio_query.speed_scale = 1.1
            wave_bytes = self.core.synthesis(audio_query, self.SPEAKER_ID)
            with open(file_name, "wb") as file:
                file.write(wave_bytes)
            self.play_sound(file_name)
        except Exception as e:
            print(f"変換エラー {text}, {e}")
            
    def play_sound(self, file_name: str):
        """音声ファイルを再生"""
        try:
            pygame.mixer.music.load(file_name)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"再生エラー {file_name}, {e}")

    def wait_play(self):
        """再生中は待機する"""
        while pygame.mixer.music.get_busy():  # 再生中は待機
            pygame.time.Clock().tick(10)
    
    def get_play(self):
        """再生中かどうかを返す"""
        return pygame.mixer.music.get_busy()

