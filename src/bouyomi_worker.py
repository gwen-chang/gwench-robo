import time
from src.config import get_config_value
from src.bouyomi import bouyomi_talk
from src.gemini_api import gemini_worker, CONVERSATION_PARTNER_NAME
from src.websocket_util import get_websocket_port_from_registry, send_text_to_websocket
import queue
from src.persona import load_persona_data
from src.history import add_to_history, conversation_history
import threading

def bouyomi_worker(message_queue, persona_file_path, conversation_partner_name, persona_text, stop_event):
    """キューからメッセージを取得し、棒読みちゃんに送信します。"""
    while not stop_event.is_set():  # 終了フラグが立っていない間ループを続ける
        try:
            input_text = message_queue.get(block=True, timeout=0.1) #タイムアウトを0.1秒に設定
            # 会話履歴の更新(キューからのメッセージ)
            add_to_history(conversation_partner_name, input_text)

            bouyomi_time = bouyomi_talk(input_text, port=get_config_value('BOUYOMI_PORT'))
            time.sleep(bouyomi_time)
            websocket_port = get_websocket_port_from_registry()
            gemini_worker(input_text, persona_text, conversation_history, websocket_port, send_text_to_websocket, get_config_value('BOUYOMI_PORT'), bouyomi_talk, conversation_partner_name)
            message_queue.task_done()

        except queue.Empty:
            pass # キューが空の場合は何もしない
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")
            message_queue.task_done()
    print("bouyomi_worker スレッドを終了します。")
