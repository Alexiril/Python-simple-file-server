from os import path, rename
from time import sleep
from urllib.parse import unquote
from controller.File import FileController


class RenameController(FileController):

    def __init__(self, root) -> None:
        super().__init__(root)

    def handle(self, handler, url):
        url_path = "/"  + url[0]
        real_path = path.join(self.root, unquote(url_path))
        from_file = unquote(url[1])
        to_file = unquote(url[2])
        if path.exists(p := path.join(real_path, from_file)) and \
            not path.exists(n := path.join(real_path, to_file)):
            rename(p, n)
            while not path.exists(n):
                sleep(1)
        return super().handle(handler, url)