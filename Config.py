# --- User configuration ---

ROOT = "."
SITE_NAME = "File server"
BIND_IP = "localhost"
BIND_PORT = 80
RELEASE_SYMMETRIC_KEY = "iemlgW3wIsPNdvNNVYsbG4VKnHI59xN0U7IQQlaxvro="
SSLCERT: str = ""
SSLKEY: str = ""
USE_SSL = False

# --- Developer configuration ---

DEBUG = True
PRINT_ERRORS = True
CACHE_ROUTER = True
SERVER_NAME = "Python File Server"

# --- Loading server.config ---

def _loading_config_file():

    import importlib.util
    import importlib.machinery
    import sys

    loader = importlib.machinery.SourceFileLoader('__appconfigurationfile', 'app.config')
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    this = sys.modules[__name__]
    settings = [key for key in dir(this) if key[0] != '_']
    for key in settings:
        setattr(this, key, getattr(module, key, getattr(this, key)))

try:
    _loading_config_file()
except:
    pass