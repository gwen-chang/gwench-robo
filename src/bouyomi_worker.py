import time
from src.config import BOUYOMI_PORT, PERSONA_FILE_PATH
from src.bouyomi import bouyomi_talk
from src.gemini_api import gemini_worker,CONVERSATION_PARTNER_NAME #修正箇所
from src.websocket_util import get_websocket_port_from_registry, send_text_to_websocket
import queue #追加
from src.persona import load_persona_data #追加
import html #追加
from src.history import add_to_history, conversation_history #修正箇所

def escape_html(text):
    """HTML エスケープを行います。"""
    return html.escape(text)

def bouyomi_worker(message_queue,persona_file_path,conversation_partner_name):
    """キューからメッセージを取得し、棒読みちゃんに送信します。"""
    while True:
        try:
            input_text = message_queue.get(block=True)
            # 会話履歴の更新(キューからのメッセージ)
            persona_text = load_persona_data(persona_file_path)
            #エスケープ処理
            input_text = escape_html(input_text) #追加
            persona_text = escape_html(persona_text) #追加
            add_to_history(conversation_partner_name,input_text)

            bouyomi_time = bouyomi_talk(input_text, port=BOUYOMI_PORT)
            time.sleep(bouyomi_time)
            websocket_port = get_websocket_port_from_registry()
            gemini_worker(input_text, persona_text, conversation_history,websocket_port,send_text_to_websocket,BOUYOMI_PORT,bouyomi_talk,conversation_partner_name)
            message_queue.task_done()

        except queue.Empty:
            print("キューが空です。")
            message_queue.task_done()
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")
            message_queue.task_done()
