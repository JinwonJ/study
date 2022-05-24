from functools import wraps
from typing import Callable

from werkzeug.exceptions import Unauthorized

from core.framework.service import Usable, use, usable
from core.services.environment import Environment


def permit(*conditions):
    """ 함수 권한 확인
     - 사용자 기능 미지원시 무조건 통과
     - 최상위 등급(root: hyper, super) 사용자 무조건 통과
     todo:
       - 계층 소속에 따른 권한 확인
    """

    if not usable('UserPermission') or use(Environment).disable_permission_validate:
        def without_user_deco(callback: Callable):
            @wraps(callback)
            def wrap(*args, **kwargs):
                return callback(*args, **kwargs)

            return wrap

        return without_user_deco

    _permission = use('UserPermission')

    def with_user_deco(callback: Callable):
        @wraps(callback)
        def wrap(*args, **kwargs):
            if not _permission.permit(*conditions):
                raise Unauthorized()
            return callback(*args, **kwargs)

        return wrap

    return with_user_deco
