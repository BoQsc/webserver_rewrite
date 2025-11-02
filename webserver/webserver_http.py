
import http.server
import socketserver

from webserver_config import Config

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, World!")

def run_server():
    with socketserver.TCPServer((Config.HOST, Config.PORT), MyHttpRequestHandler) as httpd:
        print("serving at port", Config.PORT)
        httpd.serve_forever()
