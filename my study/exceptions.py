from werkzeug.exceptions import HTTPException


class InvalidColumn(HTTPException):
    """ 잘못된 열 요청시 사용
    """
    code = 400

    def __init__(self, name):
        super().__init__()
        self.description = f'{name} is invalid Column Name'


class InvalidItem(HTTPException):
    """ 잘못된 행 요청시 사용

    """
    code = 400

    def __init__(self, name):
        super().__init__()
        self.description = 'Invalid Item'


class InvalidType(HTTPException):
    """ 잘못된 값 유형시 사용

    """
    code = 400

    def __init__(self, type: str, value=None):
        super().__init__()
        if value:
            self.description = f'`{value}` is not {type}'
        else:
            self.description = f'Invalid {type}'


class Required(HTTPException):
    """ 필수 값 일 때 사용

    """
    code = 400

    def __init__(self, name):
        super().__init__()
        self.description = f'`{name}` is required'
