from Config import SITE_NAME
from Functions import read_file, template

class ViewController:

    def __init__(self, root) -> None:
        self.root = root

    def handle(self, handler, url):
        return template(read_file("templates/view.html").decode(), {
            "SITE_NAME": SITE_NAME,
        }).encode()