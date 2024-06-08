from os import path
from urllib.parse import unquote
from Functions import read_file
from Mime import mimeTypes
from exceptions.NotFound import NotFoundException
from pathlib import PurePath

class FileController:

    def __init__(self, root) -> None:
        self.root = root

    def handle(self, handler, url):
        real_path = path.realpath(path.join(self.root, unquote(url[0])))
        url = "/"  + url[0]
        try:
            rurl = PurePath(real_path).relative_to(PurePath(path.realpath(self.root)))
            if path.exists(path.join(self.root, str(rurl))):
                url = str(rurl)
        except ValueError:
            if url == "//":
                real_path = self.root
            else:
                raise NotFoundException(url)
        if url == "/" or path.isdir(real_path):
            raise NotFoundException(url)
        else:
            if path.exists(real_path):
                handler.reactive_headers["Content-Type"] = mimeTypes.get(real_path.split(".")[-1], "text/html")
                return read_file(real_path)
            raise NotFoundException(url)