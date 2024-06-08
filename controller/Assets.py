from Mime import mimeTypes
from os import path
from Functions import read_file
from exceptions.NotFound import NotFoundException

class AssetsController:

    def handle(self, handler, url):
        real_path = path.join("assets", "public", url[0])
        if path.exists(real_path) and path.isfile(real_path):
            handler.reactive_headers["Content-Type"] = mimeTypes.get(real_path.split(".")[-1], "text/html")
            return read_file(real_path)
        raise NotFoundException(url)