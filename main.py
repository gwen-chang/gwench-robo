import time
import queue
import socket
from src.config import load_config, get_config_value
from src.thread_util import create_server_thread, create_bouyomi_thread
from src.gemini_api import CONVERSATION_PARTNER_NAME
from src.persona import load_persona_data
from src.history import clear_history
import threading
import sys

# コマンドの定義
RELOAD_PERSONA_COMMAND = "reload-persona"
RELOAD_CONFIG_COMMAND = "reload-config"
CLEAR_HISTORY_COMMAND = "clear-history"
EXIT_COMMAND = "exit"

def reload_bouyomi_thread(message_queue, persona_file_path, conversation_partner_name, persona_text, bouyomi_thread, stop_event):
    """bouyomi_threadを再起動します。"""
    print("bouyomi_threadを再起動します...")
    stop_event.set()  # 終了フラグを立てる
    bouyomi_thread.join() # bouyomi_threadが終了するまで待機
    stop_event.clear() # 終了フラグをクリア
    bouyomi_thread = create_bouyomi_thread(message_queue, persona_file_path, conversation_partner_name, persona_text, stop_event)
    bouyomi_thread.start()
    print("bouyomi_threadを再起動しました。")
    return bouyomi_thread

def reload_persona(persona_file_path):
    """persona.ini を再読み込みします。"""
    print("persona.ini を再読み込みします...")
    persona_text = load_persona_data(persona_file_path)
    print("persona.ini を再読み込みしました。")
    return persona_text

def reload_config():
    """config.ini を再読み込みします。"""
    print("config.ini を再読み込みします...")
    config_data = load_config()
    print("config.ini を再読み込みしました。")
    return config_data

def check_port_availability(port):
    """指定されたポートが使用可能かどうかを確認します。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

# --- メイン処理 ---
def main():
    message_queue = queue.Queue()

    # HTTPポートが使用可能か確認
    http_port = get_config_value('HTTP_PORT')
    if not check_port_availability(http_port):
        print(f"エラー: HTTPポート {http_port} はすでに使用されています。")
        print("config.ini で別のポートを指定し、再度実行してください。")
        input("何かキーを押すと終了します...")  # ユーザーがキーを押すまで待機
        sys.exit(1)  # エラー終了

    try:
        server_thread = create_server_thread(message_queue)
        server_thread.start()
    except OSError as e:
        print(f"エラー: HTTPサーバーの起動に失敗しました: {e}")
        if "Address already in use" in str(e):
            print(f"HTTPポート {http_port} はすでに使用されています。")
            print("config.ini で別のポートを指定し、再度実行してください。")
        input("何かキーを押すと終了します...")  # ユーザーがキーを押すまで待機
        sys.exit(1)

    # 初期ペルソナを読み込む
    config_data = load_config()
    persona_file_path = config_data['PERSONA_FILE_PATH']
    persona_text = load_persona_data(persona_file_path)

    stop_event = threading.Event()
    bouyomi_thread = create_bouyomi_thread(message_queue, persona_file_path, CONVERSATION_PARTNER_NAME, persona_text, stop_event)
    bouyomi_thread.start()

    time.sleep(1)
    print(f"プログラムが実行中です。HTTPリクエストを送信して試してください。(例: http://localhost:{http_port}/talk?text=こんにちは)")
    while True:
        try:
            command = input(f"コマンドを入力してください ({RELOAD_PERSONA_COMMAND} で persona.ini を再読み込み, {RELOAD_CONFIG_COMMAND} で config.ini を再読み込み, {CLEAR_HISTORY_COMMAND} で会話履歴を削除, {EXIT_COMMAND} で終了): ")
            if command == RELOAD_PERSONA_COMMAND:
                persona_text = reload_persona(persona_file_path)
                bouyomi_thread = reload_bouyomi_thread(message_queue, persona_file_path, CONVERSATION_PARTNER_NAME, persona_text, bouyomi_thread, stop_event)
            elif command == RELOAD_CONFIG_COMMAND:
                config_data = reload_config()
                persona_file_path = config_data['PERSONA_FILE_PATH']
                persona_text = reload_persona(persona_file_path)
                bouyomi_thread = reload_bouyomi_thread(message_queue, persona_file_path, CONVERSATION_PARTNER_NAME, persona_text, bouyomi_thread, stop_event)
            elif command == CLEAR_HISTORY_COMMAND:
                print("会話履歴を削除します...")
                clear_history()
                print("会話履歴を削除しました。")
            elif command == EXIT_COMMAND:
                print("プログラムを終了します")
                stop_event.set() # 終了フラグを立てる
                bouyomi_thread.join() # bouyomi_threadが終了するまで待機
                break
            else:
                print("無効なコマンドです。")
        except KeyboardInterrupt:
            print("プログラムを終了します")
            stop_event.set() # 終了フラグを立てる
            bouyomi_thread.join() # bouyomi_threadが終了するまで待機
            break

if __name__ == "__main__":
    main()
