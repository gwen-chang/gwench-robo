import winreg
import websockets
import asyncio
from src.config import REGISTRY_KEY_PATH, REGISTRY_VALUE_NAME, WEBSOCKET_URI_FORMAT
import html #追加

def escape_html(text):
    """HTML エスケープを行います。"""
    return html.escape(text)

def get_websocket_port_from_registry():
    """レジストリから WebSocket のポート番号を取得します。"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_KEY_PATH) as key:
            value, _ = winreg.QueryValueEx(key, REGISTRY_VALUE_NAME)
            return value
    except FileNotFoundError:
        print(f"エラー: レジストリキーが見つかりません: HKCU\\{REGISTRY_KEY_PATH}")
        return None
    except Exception as e:
        print(f"エラー: レジストリからポート番号を取得できませんでした: {e}")
        return None

async def send_text_to_websocket(websocket_port, text):
    """WebSocket サーバーにテキストを送信します。"""
    if websocket_port is None:
        print("WebSocketポート番号が取得できませんでした")
        return None
    websocket_uri = WEBSOCKET_URI_FORMAT.format(websocket_port)
    try:
        async with websockets.connect(websocket_uri) as websocket:
            text = escape_html(text) # 追加
            await websocket.send(text)
            print(f"WebSocket に送信しました: {text}")
            return text
    except Exception as e:
        print(f"エラー: WebSocket への送信に失敗しました: {e}")
        return None
