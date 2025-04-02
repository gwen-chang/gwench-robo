from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote
import urllib.parse
from src.config import get_config_value


class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, message_queue, *args, **kwargs):
        self.message_queue = message_queue
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if self.path.startswith("/talk"):
            if 'text' in query_params:
                # URLエンコードされた文字列をデコード
                text = unquote(query_params['text'][0])
                print(f"受信したテキスト: {text}")
                self.message_queue.put(text)
                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write("OK".encode("utf-8"))
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write("エラー: 'text' パラメータがありません".encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("404 Not Found".encode("utf-8"))
