# AI_Zundamon
ローカルLLMを使ったAIずんだもんです

### 機能概要
- ローカルLLM（LM Studio等）と連携し、ずんだもん/めたんが会話します
- VOICEVOXによる音声合成
- PySimpleGUI＋pygameによるキャラクター表示・口パク

### 使用ライブラリ
- [Open AI](https://pypi.org/project/openai/)
- [pygame](https://www.pygame.org/news)
- [voicevox_core](https://github.com/VOICEVOX/voicevox_core/releases)
- [onnxruntime](https://github.com/microsoft/onnxruntime/releases)
- [open_jtalk_dic_utf_8-1.11](https://sourceforge.net/projects/open-jtalk/postdownload)
- [psd-tools](https://psd-tools.readthedocs.io/en/latest/)
- [PysimpleGUI](https://www.pysimplegui.com/)
 
### 使用画像
- [ずんだもん立ち絵素材](https://www.pixiv.net/artworks/92641351)
- [四国めたん立ち絵素材](https://www.pixiv.net/artworks/92641379)
- [昭和レトロな茶の間（2枚）](https://min-chi.material.jp/fm/bg_c/retro_living/)

みんちりえ様（ https://min-chi.material.jp/ ）
坂本アヒル様 ( https://www.pixiv.net/users/12147115 )

## セットアップ

1. Python 3.8以上を推奨
2. 仮想環境を作成（任意）
3. 必要なライブラリをインストール
```
pip install -r requirements.txt

 または個別に

pip install openai pygame psd-tools PySimpleGUI
```
4. VOICEVOX Core・open_jtalk辞書をダウンロードし、パスを合わせてください

※ `voicevox_core` はpipでインストールできません。  
[公式リリースページ](https://github.com/VOICEVOX/voicevox_core/releases)から各自ダウンロードし、解凍したファイルをプロジェクトに配置してください。


## 実行方法

1. LM StudioなどローカルLLMサーバーを起動
2. 本プロジェクトのディレクトリで
```
python ai_zundamon.py
```

## 注意事項

- LM StudioやVOICEVOX Coreのセットアップが必要です
- 画像素材の利用規約を守ってください

## ライセンス

- コード: MITライセンス
- 画像素材: 各素材の利用規約に従ってください