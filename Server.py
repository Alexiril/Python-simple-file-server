from http.server import ThreadingHTTPServer
from Handler import Handler
from Config import SITE_NAME
        
class Server(ThreadingHTTPServer):

    def __init__(self, root, bind_address="localhost", bind_port=80) -> None:
        Handler.root = root
        super().__init__((bind_address, bind_port), Handler)
        print(f"Server with site '{SITE_NAME}' started at ({bind_address}:{bind_port}).")
        self.serve_forever()
