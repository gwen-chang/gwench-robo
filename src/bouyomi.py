import requests
from src.config import BOUYOMI_WAIT_TIME_PER_CHAR, BOUYOMI_WAIT_TIME_ADDITIONAL
def bouyomi_talk(text, host="localhost", port=50080):
    """棒読みちゃんにテキストを読み上げさせます。"""
    try:
        url = f"http://{host}:{port}/Talk"
        # URLエンコードを削除
        params = {"text": text}
        response = requests.get(url, params=params)
        response.raise_for_status()
        print(f"棒読みちゃんに送信: {text}")
        return len(text) * BOUYOMI_WAIT_TIME_PER_CHAR + BOUYOMI_WAIT_TIME_ADDITIONAL
    except requests.exceptions.RequestException as e:
        print(f"エラー: 棒読みちゃんへのリクエスト中にエラーが発生しました: {e}")
        return 0
