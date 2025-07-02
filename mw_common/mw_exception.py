class MwException(Exception):
    exceptionType: str = None
    message = None
    additionalInfo: dict = None
    code: str = None
    data: any = None

    def __init__(self, message=None, exception_type: str = None):
        super().__init__(message)
        self.exceptionType = exception_type
        self.message = message

    def other_info(self, additional_info: dict = None, code: str = None):
        self.additionalInfo = additional_info
        self.code = code
        return self

    def add_additional_info(self, key: str, value):
        if not self.additionalInfo:
            self.additionalInfo = {}
        if key:
            self.additionalInfo[key] = value
        return self

    def add_data(self, data: any):
        self.data = data
        return self
