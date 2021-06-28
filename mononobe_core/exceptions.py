class MononobeException(Exception):
    def __init__(self, message: str):
        super(MononobeException, self).__init__()
        self.message = message


class MononobeNotImplemented(MononobeException):
    def __init__(self):
        super(MononobeNotImplemented, self).__init__('Not implemented')
