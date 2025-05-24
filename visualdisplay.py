import pygame
import re

class VisualDisplay:
    """画面描画を担当するクラス"""    

    def __init__(self, bg_image, font_path, font_size=40, screen_size=(800, 600)):
        """背景画像・フォントなどを初期化"""
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.font = pygame.font.Font(font_path, font_size)
        self.background = pygame.image.load(bg_image).convert()
        pygame.display.set_caption("ずんだもんと会話する")
        self.font_size = font_size

    def draw_text(self, x: int, y: int, message: str, fg_color, bg_color=(0, 0, 0)):
        """複数行テキストを縁取り付きで描画"""
        lines = re.split(r'[。\n]+', message)
        y -= 40 if len(lines) > 1 else 0
        for line in lines:
            self.draw_text_outline(x, y, line, fg_color, bg_color)
            y += self.font_size + 3

    def draw_text_outline(self, x: int, y: int, message: str, fg_color, bg_color=(0, 0, 0)):
        """縁取り付きでテキストを描画"""
        text = self.font.render(message, True, bg_color)
        self.screen.blit(text, (x + 1, y))
        self.screen.blit(text, (x - 1, y))
        self.screen.blit(text, (x, y + 1))
        self.screen.blit(text, (x, y - 1))
        text = self.font.render(message, True, fg_color)
        self.screen.blit(text, (x, y))

    def refresh(self):
        """背景を再描画"""
        self.screen.fill((0,0,0))
        self.screen.blit(self.background, (0, 0))

    def draw_character(self, image, pos):
        """キャラクター画像を描画"""
        self.screen.blit(image, pos)

    def update(self):
        """画面を更新"""        
        pygame.display.update()
