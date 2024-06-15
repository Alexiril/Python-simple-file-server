from json import JSONDecoder, JSONEncoder
from Config import DEBUG
from Functions import encrypt_symmetric
from controller.API.GetFolder import handle as getFolder
from controller.API.Rename import handle as rename
from controller.API.Delete import handle as delete
from exceptions.IncorrectApiRequest import IncorrectApiRequestException


class ApiController:

    @staticmethod
    def checkArgument(arg, req, data):
        if arg not in data or type(data[arg]) != str:
            raise IncorrectApiRequestException(
                f"No {arg} argument in {req} request data"
            )

    def handle(self, handler, url):
        if handler.command != "POST":
            raise IncorrectApiRequestException("API request was not POST.")
        req = url[0]
        cont_len = int(handler.headers.get('content-length'))
        data = handler.rfile.read(cont_len).decode()
        data = JSONDecoder().decode(data)
        result = ""
        handler.reactive_headers["Content-Type"] = "application/json"
        try:
            match req:
                case "get-folder":
                    ApiController.checkArgument("path", req, data)
                    result = getFolder(handler.root, data)
                case "rename":
                    ApiController.checkArgument("path", req, data)
                    ApiController.checkArgument("original", req, data)
                    ApiController.checkArgument("new", req, data)
                    result = rename(handler.root, data)
                case "delete":
                    ApiController.checkArgument("path", req, data)
                    ApiController.checkArgument("file", req, data)
                    result = delete(handler.root, data)
        except Exception as e:
            handler.reactive_response = getattr(e, 'response', 500)
            return JSONEncoder().encode({
                "result": "error",
                "cause": encrypt_symmetric(str(e)) if not DEBUG else str(e)
            }).encode()
        return result.encode()
