import threading
from http.server import HTTPServer
from src.http_server import MyHandler
from src.config import HTTP_PORT, PERSONA_FILE_PATH
from src.bouyomi_worker import bouyomi_worker
from src.gemini_api import CONVERSATION_PARTNER_NAME #修正箇所

def run_server(message_queue, server_class=HTTPServer, handler_class=MyHandler, port=HTTP_PORT):
    """HTTP サーバーを起動します。"""
    handler_with_queue = lambda *args, **kwargs: handler_class(message_queue, *args, **kwargs)
    server_address = ('', port)
    httpd = server_class(server_address, handler_with_queue)
    print(f"HTTPサーバーがポート {port} で起動しました")
    httpd.serve_forever()

def create_server_thread(message_queue):
    """HTTPサーバーのスレッドを作成します。"""
    server_thread = threading.Thread(target=run_server, args=(message_queue,))
    server_thread.daemon = True
    return server_thread

def create_bouyomi_thread(message_queue,persona_file_path,conversation_partner_name):
  bouyomi_thread = threading.Thread(target=bouyomi_worker, args=(message_queue,persona_file_path,conversation_partner_name)) #修正箇所
  bouyomi_thread.daemon = True
  return bouyomi_thread
