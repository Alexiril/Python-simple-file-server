from re import match
from exceptions.NotFound import NotFoundException

class Router:

    class Route:

        def __init__(self, regex, controller) -> None:
            self.regex = regex
            self.controller = controller

    def __init__(self) -> None:
        self.clear()

    def add_route(self, regex, controller):
        self.routes.append(Router.Route(regex, controller))

    def route(self, handler, url):
        for r in self.routes:
            if (m := match(r.regex, url)) != None:
                return r.controller(handler, m.groups())
        raise NotFoundException(url)
    
    def clear(self):
        self.routes = []