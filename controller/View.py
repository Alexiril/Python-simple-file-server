from Config import SITE_NAME
from Functions import read_file, template

class ViewController:

    def __init__(self, root) -> None:
        self.root = root

    def handle(self, handler, url):
        return template(read_file("templates/folder.html").decode(), {
            "SITE_NAME": SITE_NAME,
        }).encode()
        # cookies = SimpleCookie(handler.headers.get('Cookie'))
        # url = cookies.get("fpath")
        # if url == None:
        #     url = ""
        # else:
        #     url = url.value
        # real_path = path.realpath(path.join(self.root, unquote(url)))
        # url = "/"  + url
        # try:
        #     rurl = PurePath(real_path).relative_to(PurePath(path.realpath(self.root)))
        #     if path.exists(path.join(self.root, str(rurl))):
        #         url = str(rurl)
        # except ValueError:
        #     if url == "//":
        #         real_path = self.root
        #     else:
        #         raise NotFoundException(url)
        # if url != "/" and not path.isdir(real_path):
        #     url = "/"
        #     real_path = self.root
        # url = url.replace("\\", '/')
        # back = "/" + path.join(*path.split(url)[:-1])
        # if url == "/": url = ""
        # files, folders = [], []
        # for current_file in listdir(real_path):
        #     if path.isdir(path.join(real_path, current_file)) :
        #         folders.append(current_file)
        #     else:
        #         files.append(current_file)
        # data = {
        #     "name": url,
        #     "children": []
        # }
        # for current_file in folders + files:
        #     is_folder = current_file in folders
        #     if is_folder:
        #         icon = read_file("assets/icons/folder.svg").decode()
        #     else:
        #         ext = current_file.split(".")[-1]
        #         icon = read_file(f'assets/icons/{ext if ext in icons else "blank"}.svg').decode()
        #     actual_size = path.getsize(path.join(real_path, current_file))
        #     size = determinator(actual_size) if current_file not in folders else "-"
        #     if is_folder or actual_size < 1024**2 * 2:
        #         ondblclick = f"window.location.assign(\'/{url}/{current_file}\')"
        #     else:
        #         ondblclick = f"askDownload('{current_file}', '/{url}/{current_file}')"
        #     data["children"].append({
        #         "name": current_file,
        #         "value": actual_size if not is_folder else 1024 ** 2,
        #         # "ondblclick": ondblclick,
        #         # "size": size,
        #         # "icon": icon
        #     })            
        #if url == "": url = "/"
        #cookies["fpath"] = url
        #handler.reactive_headers["Set-Cookie"] = cookies.output(None, "")
        
            #"URL": unquote(url),
            #"BACK_ADDR": back,
            #"FILES": JSONEncoder().encode(data)
