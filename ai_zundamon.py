"""AIずんだもん"""
import threading
import pygame
import PySimpleGUI as sg

from visualdisplay import VisualDisplay
from imageprocessor import ImageProcessor
from ttsmanager import TTSManager
from lmstudioclient import LMStudioClient


# 定数
ZUNDAMON_POSITION = (500, 150)
MOUTH_OPEN_TIME = 4
MOUTH_CLOSE_TIME = 4
FPS = 30
FONT_SIZE = 50
MAX_TEXT_LENGTH = 24
IMAGE_NORMAL_FACE = 2
SCREEN_SIZE = (1280, 1024)
ZUNDAMON = True

# 状態管理
state = {
    'is_speaking': False,
    'spoken_text': ''
}


def background_task(client, user_input, window, user_tts, response_tts):
    """バックグラウンドでAI応答とTTSを処理"""
    try:
        user_tts.tts_speak(user_input)
        reply = client.get_response(user_input)
        window.write_event_value('-RESPONSE-', (user_input, reply))
        state['is_speaking'] = True
        texts = reply.split('\n')
        for text in texts:
            response_tts.tts_speak(text)
            state['spoken_text'] = text
            while response_tts.get_play():
                pass
        # 会話完了を待つ
        response_tts.wait_play()
    except Exception as e:
        window.write_event_value('-RESPONSE-', (user_input, f'[エラー] {e}'))
    finally:
        state['is_speaking'] = False
        state['spoken_text'] = ''


def create_client():
    """LMStudioClientを初期化"""
    try:
        return LMStudioClient('http://localhost:1234/v1', 'gemma-3-1b-it')
    except Exception as e:
        print('クライアント初期化に失敗:', e)
        return None


def create_gui_window():
    """PySimpleGUIのウィンドウを生成"""    
    sg.theme('DefaultNoMoreNagging')
    layout = [
        [sg.Multiline(size=(80, 20), key='-OUTPUT-', disabled=True, autoscroll=True)],
        [sg.Multiline(size=(80, 5), key='-INPUT-', enter_submits=True)],
        [sg.Button('送信', bind_return_key=True), sg.Button('終了')]
    ]
    return sg.Window('LM Studio チャット', layout, finalize=True)


def get_character_images(image_processor):
    """キャラクター画像を読み込んでリストで返す"""
    if ZUNDAMON:
        return [
            image_processor.get_zundamon_image(
                "zundamon_normal_close_mouth.png", mouth="*むふ", eye="*普通目",
                left="*基本", right="*基本", size=1.0, flip=False),
            image_processor.get_zundamon_image(
                "zundamon_normal_close_eye.png", eye="*なごみ目",
                left="*基本", right="*基本", size=1.0, flip=False),
            image_processor.get_zundamon_image(
                "zundamon_normal.png", eye="*普通目",
                left="*基本", right="*基本", size=1.0, flip=False),
            image_processor.get_zundamon_image(
                "zundamon_normal2.png", eye="*上向き",
                mouth="*むふ" , left="*基本", right="*基本", size=1.0, flip=False)
       ]
    else:
        return [
            image_processor.get_metan_image(
                "metan_normal.png", eye="*普通目",
                right="*普通", left="*普通", size=1.0),
            image_processor.get_metan_image(
                "metan_normal_close_eye.png", eye="*目閉じ",
                 right="*普通", left="*普通", size=1.0),
            image_processor.get_metan_image(
                "metan_normal_close_mouth.png", mouth="*ほほえみ",
                 eye="*普通目", right="*普通", left="*普通", size=1.0),
            image_processor.get_metan_image(
                "metan_normal_close_mouth2.png", mouth="*ほほえみ",
                 eye="*カメラ目線", right="*普通", left="*普通", size=1.0),
        ]


def handle_send(user_input, window, client, user_tts, response_tts):
    """ユーザー入力を非同期で処理"""
    window['-INPUT-'].update("") # 入力欄クリア
    window['-OUTPUT-'].update(f'あなた: {user_input}\n', append=True) # 出力欄にユーザー入力表示
    threading.Thread(
        target=background_task,
        args=(client, user_input, window, user_tts, response_tts),
        daemon=True
    ).start()


def draw_zundamon_mouth(display, image_list,  image_index, mouth_counter):
    """口パク制御"""
    if state['is_speaking']:
        if mouth_counter > MOUTH_OPEN_TIME:
            display.draw_character(image_list[image_index], ZUNDAMON_POSITION)
        if mouth_counter > MOUTH_OPEN_TIME + MOUTH_CLOSE_TIME:
            mouth_counter = 0
        mouth_counter += 1
    return mouth_counter


def draw_speech_text(display, text, font_size):
    """話しているテキストを描画"""
    if not text:
        return

    # 背景用の半透明サーフェスを作成
    lines = [text[i:i + MAX_TEXT_LENGTH] for i in range(0, len(text), MAX_TEXT_LENGTH)]
    bg_width = 1200  # 必要に応じて調整
    bg_height = len(lines) * (font_size + 3) + 20
    bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
    bg_surface.fill((50, 50, 50, 180))  # RGBA: 半透明グレー

    # メイン画面に背景をblit
    bg_x = 40
    bg_y = 690
    display.screen.blit(bg_surface, (bg_x, bg_y))

    # テキスト描画
    for row, i in enumerate(range(0, len(text), MAX_TEXT_LENGTH)):
        line = text[i:i + MAX_TEXT_LENGTH]
        display.draw_text_outline(
            bg_x, bg_y + row * (font_size + 3), line, (255, 102, 255), (255, 255, 255))


def main_loop(window, client, user_tts, response_tts, display, image_list):
    """メインループ"""
    pygame.init()
    fps = FPS
    mouth_counter = 0
    image_index = 0
    try:
        while True:
            event, values = window.read(timeout=fps)
            if event in (sg.WINDOW_CLOSED, '終了'):
                break
            elif event == '送信':
                user_input = values['-INPUT-'].strip()
                if user_input:
                    handle_send(user_input, window, client, user_tts, response_tts)
            elif event == '-RESPONSE-':
                user_input, reply = values['-RESPONSE-']
                window['-OUTPUT-'].update(f'AI: {reply}\n\n', append=True)
            pygame.event.pump()
            display.refresh()
            display.draw_character(image_list[image_index + IMAGE_NORMAL_FACE], ZUNDAMON_POSITION)
            # ここで口パク状態に応じて描画する画像を決定
            mouth_counter = draw_zundamon_mouth(display, image_list, image_index, mouth_counter)
            draw_speech_text(display, state['spoken_text'], FONT_SIZE)
            display.update()
    except Exception as e:
        window['-OUTPUT-'].update(f'[致命的エラー] {e}\n', append=True)
    finally:
        window.close()
        pygame.quit()


def main():
    """各種初期化とメインループ開始"""
    client = create_client()
    if not client:
        return
    window = create_gui_window()
    if ZUNDAMON:
        user_tts = TTSManager(id=2)
        response_tts = TTSManager(id=1)
        image_processor = ImageProcessor('ずんだもん立ち絵素材2.3.psd')
    else:
        user_tts = TTSManager(id=1)
        response_tts = TTSManager(id=2)
        image_processor = ImageProcessor('四国めたん立ち絵素材2.1.psd')

    display = VisualDisplay(
        bg_image = '昭和レトロな茶の間（照明ON）.jpg',
        font_path = './msyhbd.ttc',
        font_size = FONT_SIZE,
        screen_size = SCREEN_SIZE
    )
    image_list = get_character_images(image_processor)
    main_loop(window, client, user_tts, response_tts, display, image_list)


if __name__ == "__main__":
    main()
