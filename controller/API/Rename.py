from json import JSONEncoder
from os import path, rename
from pathlib import PurePath
from time import sleep
from urllib.parse import unquote

from exceptions.IncorrectApiRequest import IncorrectApiRequestException
def handle(root, data):
    url_path = data["path"]
    if (len(url_path) > 0 and url_path[0] == '/'):
        url_path = url_path[1:]
    real_path = path.realpath(path.join(root, unquote(url_path)))
    try:
        rurl = PurePath(real_path).relative_to(PurePath(path.realpath(root)))
        if path.exists(path.join(root, str(rurl))):
            url_path = str(rurl)
        else:
            raise IncorrectApiRequestException(
                f"Didn't find path {url_path}", 404)
    except ValueError:
        if url_path == "/":
            real_path = root
        else:
            raise IncorrectApiRequestException(
                f"Didn't find path {url_path}", 404)
    if url_path != "/" and not path.isdir(real_path):
        url_path = "/"
        real_path = root
    from_file = unquote(data["original"])
    to_file = unquote(data["new"])
    if path.exists(p := path.join(real_path, from_file)) and \
        not path.exists(n := path.join(real_path, to_file)):
        rename(p, n)
        while not path.exists(n):
            sleep(1)
    return JSONEncoder().encode({
        "result": "ok",
        "cause": ""
    })