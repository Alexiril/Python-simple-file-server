from Config import DEBUG, SITE_NAME
from Functions import encrypt_symmetric, read_file, template
from exceptions.NotFound import NotFoundException

class ErrorController:

    human_names = {
        400: 'Bad request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not found',
        408: 'Request timeout',
        429: 'Too many requests',
        500: 'Internal error',
        503: 'Service unavailable'
    }

    descriptions = {
        400: 'What did you mean?..',
        401: 'Who are you?..',
        403: 'Cannot let you in...',
        404: 'Did you lost something?..',
        408: 'Was waiting too long...',
        429: 'I need some time...',
        500: 'Yeah, I\'m totally broken...',
        503: 'The service will be back in no time!'
    }

    def __init__(self, handler) -> None:
        self.handler = handler

    def handle(self, exception):
        if type(exception) == NotFoundException:
            error_code = 404
        else:
            error_code = 500
        self.handler.reactive_response = error_code
        human_name = ErrorController.human_names[error_code]
        description = ErrorController.descriptions[error_code]
        additional_info = "Error data: " + (str(exception) if DEBUG else encrypt_symmetric(str(exception).encode()))
        return template(read_file("templates/error.html").decode(), {
            "SITE_NAME": SITE_NAME,
            "ERROR_CODE": error_code,
            "ERROR_HUMAN_NAME": human_name,
            "ERROR_DESCRIPTION": description,
            "ADDITIONAL_ERROR_INFO": additional_info
        })
