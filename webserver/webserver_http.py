
import http.server
import socketserver

from webserver_config import Config

from webserver_routing import get_handler

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        handler = get_handler(self.path)
        handler(self)

def run_server():
    with socketserver.TCPServer((Config.HOST, Config.PORT), MyHttpRequestHandler) as httpd:
        print("serving at port", Config.PORT)
        httpd.serve_forever()
