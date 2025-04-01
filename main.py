import time
import queue
from src.config import PERSONA_FILE_PATH
from src.thread_util import create_server_thread,create_bouyomi_thread
from src.gemini_api import CONVERSATION_PARTNER_NAME # 追加

# --- メイン処理 ---
def main():
    message_queue = queue.Queue()
    server_thread = create_server_thread(message_queue)
    server_thread.start()

    bouyomi_thread = create_bouyomi_thread(message_queue,PERSONA_FILE_PATH,CONVERSATION_PARTNER_NAME)
    bouyomi_thread.start()

    time.sleep(1)
    print("プログラムが実行中です。HTTPリクエストを送信して試してください。(例: http://localhost:51002/talk?text=こんにちは)")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("プログラムを終了します")
            break

if __name__ == "__main__":
    main()
