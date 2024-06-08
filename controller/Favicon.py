from Functions import read_file

class FaviconController:

    def handle(self, handler, url):
        return read_file("assets/favicon.ico")