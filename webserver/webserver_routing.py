
# webserver_routing.py

# A simple router that maps paths to handlers.
# Handlers are functions that take a request handler object as an argument.

def handle_root(handler):
    handler.send_response(200)
    handler.send_header("Content-type", "text/html")
    handler.end_headers()
    handler.wfile.write(b"Hello, World!")

def handle_404(handler):
    handler.send_response(404)
    handler.send_header("Content-type", "text/html")
    handler.end_headers()
    handler.wfile.write(b"404 Not Found")

routes = {
    "/": handle_root,
}

def get_handler(path):
    return routes.get(path, handle_404)
