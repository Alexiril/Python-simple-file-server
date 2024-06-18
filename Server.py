from http.server import ThreadingHTTPServer
from ssl import wrap_socket, PROTOCOL_TLS
from Handler import Handler
from Config import SITE_NAME, SSLCERT, SSLKEY, USE_SSL
        
class Server(ThreadingHTTPServer):

    def __init__(self, root, bind_address="localhost", bind_port=80) -> None:
        Handler.root = root
        super().__init__((bind_address, bind_port), Handler)
        print(f"Server with site '{SITE_NAME}' started at ({bind_address}:{bind_port}).")
        if USE_SSL:
            self.socket = wrap_socket(
                sock=self.socket,
                server_side = True,
                certfile = SSLCERT,
                keyfile = SSLKEY,
                ssl_version = PROTOCOL_TLS
                )
        self.serve_forever()
