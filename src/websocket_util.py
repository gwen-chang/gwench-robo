import winreg
import websockets
from src.config import get_config_value

def get_websocket_port_from_registry():
    """レジストリから WebSocket のポート番号を取得します。"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, get_config_value('REGISTRY_KEY_PATH')) as key:
            value, _ = winreg.QueryValueEx(key, get_config_value('REGISTRY_VALUE_NAME'))
            return value
    except FileNotFoundError:
        print(f"エラー: レジストリキーが見つかりません: HKCU\\{get_config_value('REGISTRY_KEY_PATH')}")
        return None
    except Exception as e:
        print(f"エラー: レジストリからポート番号を取得できませんでした: {e}")
        return None

async def send_text_to_websocket(websocket_port, text):
    """WebSocket サーバーにテキストを送信します。"""
    if websocket_port is None:
        print("WebSocketポート番号が取得できませんでした")
        return None
    websocket_uri = get_config_value('WEBSOCKET_URI_FORMAT').format(websocket_port)
    try:
        async with websockets.connect(websocket_uri) as websocket:
            await websocket.send(text)
            print(f"WebSocket に送信しました: {text}")
            return text
    except Exception as e:
        print(f"エラー: WebSocket への送信に失敗しました: {e}")
        return None
