class IncorrectApiRequestException(Exception):

    def __init__(self, *args: object, response = 500) -> None:
        super().__init__(*args)
        self.response = response