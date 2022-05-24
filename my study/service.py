from typing import TypeVar, Callable

from core.framework.log import Loggable
from core.utils.shadow_inject import shadow_inject

NAMED_SERVICE = {}


class Usable(Loggable):
    """ 서비스 클래스 확장
    """
    _run_on_built = False

    @classmethod
    def inject(cls):
        return shadow_inject(cls)


def usable(usable_class):
    """ 사용 가능한 서비스 클래스 여부 확인
    :example:
        if usable(UserService):
            pass

        if usable('User')
            pass
    """
    if isinstance(usable_class, str):
        service = NAMED_SERVICE.get(usable_class)

        if service:
            return service

        return None

    if Usable in usable_class.__mro__:
        return usable_class

    return None


T = TypeVar('T')
UsableClass = TypeVar('UsableClass', str, Callable[[Usable], T])


def use(usable_class: T) -> T:
    """ 서비스 클래스 반환
    :param usable_class: `Usable` 확장 클래스
    :return: 요청 클래스 실체
    """

    if isinstance(usable_class, str):
        service = usable(usable_class)

        if service:
            return use(service)

        raise Exception(f'{usable_class} is not exported')

    if not usable(usable_class):
        raise Exception(f'{str(usable_class.__name__)} is not Usable Class')

    instance = shadow_inject(usable_class)

    return instance
