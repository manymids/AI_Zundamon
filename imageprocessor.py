import cv2
from psd_tools import PSDImage
import pygame
from pygame.locals import *
from pathlib import Path
import tempfile
import os

class ImageProcessor:
    """PSD画像からキャラクター画像を合成・加工するクラス"""

    def __init__(self, file_name):
        self.psd = PSDImage.open(file_name)

    def get_metan_image(self, file_name, eye="*普通目", eyebrow="*ごきげん", mouth="*わあー", right="*普通", left="*普通", size=0.5, flip=False, shadow=False):
        """めたん画像を合成して返す"""
        for layer in list(self.psd.descendants()):
            if "!眉" == layer.parent.name:
                if eyebrow == layer.name:
                    layer.visible = True
                else:
                    layer.visible = False
            if shadow:
                if "かげり" in layer.name:
                    layer.visible = True
            if layer.name == "*普通目" or layer.name == "*普通目2" or layer.name == "*カメラ目線" or layer.name == "*目そらし":
                layer.visible = False
            if "*目セット" == layer.name:
                if eye == "*普通目" or eye == "*普通目2" or eye == "*カメラ目線" or eye == "*目そらし" or eye == "*カメラ目線2" or eye == "*目そらし2":
                    layer.visible = True
                else:
                    layer.visible = False
            elif eye ==  layer.name:
                layer.visible = True
            if "*わあー" == layer.name and mouth != "*わあー":
                layer.visible = False
            elif mouth ==  layer.name:
                layer.visible = True
            if left == layer.name and "!左腕" == layer.parent.name and "*白ロリ服" == layer.parent.parent.name:
                layer.visible = True
            elif "!左腕" == layer.parent.name and "*白ロリ服" == layer.parent.parent.name:
                layer.visible = False
            if right == layer.name and "!右腕" == layer.parent.name and "*白ロリ服" == layer.parent.parent.name:
                layer.visible = True
            elif "!右腕" == layer.parent.name and "*白ロリ服" == layer.parent.parent.name:
                layer.visible = False
        return self._compose_and_resize(self.psd, file_name, size, flip)
        
    def get_zundamon_image(self, file_name, eye="*普通目", eyebrow="*普通眉", mouth="*ほあ", right="*基本", left="*基本", size=0.55, flip=True, shadow=False):
        """ずんだもん画像を合成して返す"""
        for layer in list(self.psd.descendants()):
            if "眉" in layer.name and "*" in layer.name:
                if eyebrow == layer.name:
                    layer.visible = True
                else:
                    layer.visible = False
            if shadow:
                if "かげり" in layer.name:
                    layer.visible = True
            if layer.name == "*普通目" or layer.name == "*カメラ目線" or layer.name == "*目逸らし":
                layer.visible = False
            if "*目セット" == layer.name:
                if eye == "*普通目" or eye == "*カメラ目線" or eye == "*目逸らし":
                    layer.visible = True
                else:
                    layer.visible = False
            elif eye ==  layer.name:
                layer.visible = True
            if "*ほあー" == layer.name and mouth != "*ほあー":
                layer.visible = False
            if "*むふ" == layer.name and mouth != "*むふ":
                layer.visible = False
            elif mouth ==  layer.name:
                layer.visible = True
            if left == layer.name and "!左腕" == layer.parent.name and "*服装1" == layer.parent.parent.name:
                layer.visible = True
            elif "!左腕" == layer.parent.name and "*服装1" == layer.parent.parent.name:
                layer.visible = False

            if right == layer.name and "!右腕" == layer.parent.name and "*服装1" == layer.parent.parent.name:
                layer.visible = True
            elif "!右腕" == layer.parent.name and "*服装1" == layer.parent.parent.name:
                layer.visible = False
        return self._compose_and_resize(self.psd, file_name, size, flip)
    
    def _compose_and_resize(self, psd, file_name: str, size: float, flip: bool = False) -> pygame.Surface:
        """PSDを合成し、リサイズ・反転してpygame画像として返す"""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_name = tmp.name
        try:
            composite_image = psd.compose(force=True)
            composite_image.save(tmp_name)
            image = cv2.imread(tmp_name, -1)
            height, width = image.shape[:2]
            scale_factor = size
            resized_image = cv2.resize(image, (int(width * scale_factor), int(height * scale_factor)))
            if flip:
                resized_image = cv2.flip(resized_image, 1)
            cv2.imwrite(file_name, resized_image)
            tmp_img = pygame.image.load(file_name).convert_alpha()
            return tmp_img
        finally:
            os.remove(tmp_name)


