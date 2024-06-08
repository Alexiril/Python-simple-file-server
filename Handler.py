from http.server import BaseHTTPRequestHandler
from Router import Router
from controller.Api import ApiController
from controller.Error import ErrorController
from Config import CACHE_ROUTER, PRINT_ERRORS, SERVER_NAME
from controller.Favicon import FaviconController
from controller.File import FileController
from controller.Assets import AssetsController
from controller.View import ViewController

class Handler(BaseHTTPRequestHandler):

    root = "."
    router = Router()
    _router_cached = False

    @staticmethod
    def redirect(handler, redirect_to):
        handler.send_response(302)
        handler.send_header('Location', redirect_to)
        handler.end_headers()

    def __init__(self, request , client_address , server) -> None:
        if not Handler._router_cached or not CACHE_ROUTER:
            Handler._router_cached = True
            Handler.router.clear()
            Handler.router.add_route(r"^/favicon\.ico$", FaviconController().handle)
            Handler.router.add_route(r"^/\$fs/(.+)$", AssetsController().handle)
            Handler.router.add_route(r"^/view$", ViewController(Handler.root).handle)
            Handler.router.add_route(r"^/api/(.+)$", ApiController().handle)
            Handler.router.add_route(r"^/$", lambda handler, _: Handler.redirect(handler, "/view"))
            Handler.router.add_route(r"^/\$pbl/([^<>:\"|?*]*)$", FileController(Handler.root).handle)
        
        self.output = bytes()
        self.reactive_headers = {
            "Content-Type": "text/html",
            "Server": SERVER_NAME,
            'Date': self.date_time_string()
        }
        self.reactive_response = 200
        super().__init__(request, client_address, server)

    def do_GET(self):
        self.do_HEAD()
        if type(self.output) == str:
            self.output = self.output.encode()
        elif type(self.output) != bytes:
            self.output = bytes(self.output)
        try:
            self.wfile.write(self.output)
        except Exception as exception:
            if PRINT_ERRORS:
                print(exception)
        
    def do_POST(self):
        self.do_GET()

    def do_HEAD(self):
        try:
            self.output = Handler.router.route(self, self.path)
        except Exception as exception:
            self.output = ErrorController(self).handle(exception)
            if PRINT_ERRORS:
                print(exception)
        if self.output != None:
            self.reactive_headers["content-length"] = str(len(self.output))
        self.log_request(self.reactive_response)
        self.send_response_only(self.reactive_response)
        for header, value in self.reactive_headers.items():
            self.send_header(header, value)
        self.end_headers()         