import requests
from src.config import get_config_value
import re

def bouyomi_talk(text, host="localhost", port=50080):
    """棒読みちゃんにテキストを読み上げさせます。"""
    try:
        # 半角スペースが+扱いされるため_に変換
        text = re.sub(r' ', '_', text)
        url = f"http://{host}:{port}/Talk"
        params = {"text": text}
        response = requests.get(url, params=params)
        response.raise_for_status()
        print(f"棒読みちゃんに送信: {text}")

        # ディレイ時間を計算
        wait_time_per_char = get_config_value('BOUYOMI_WAIT_TIME_PER_CHAR')
        wait_time_additional = get_config_value('BOUYOMI_WAIT_TIME_ADDITIONAL')
        max_bouyomi_char = get_config_value('MAX_BOUYOMI_CHAR')

        # 最大文字数を超えた場合は、最大文字数で計算
        char_count = min(len(text), max_bouyomi_char)

        wait_time = char_count * wait_time_per_char + wait_time_additional
        return wait_time
    except requests.exceptions.RequestException as e:
        print(f"エラー: 棒読みちゃんへのリクエスト中にエラーが発生しました: {e}")
        return 0
