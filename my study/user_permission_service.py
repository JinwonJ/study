from core.framework.service import Usable, use
from core.services.db import DB
from modules.user.globals import USER_LEVEL_TITLES
from modules.user.models.user_account import UserAccount
from modules.user.models.user_level import UserLevel
from modules.user.services.user_service import UserService

_db = use(DB)
_user = use(UserService)


class UserPermissionService(Usable):

    def permit(self, *and_conditions):
        """
            permit(10, 'a/b/c')
            permit('10, user/account/write', 'a/b/c')
            permit('hyper', 'a/b/c')
        """

        logger = _user.get_logger()

        print(logger)

        if not logger:
            return False

        # if self.permit_level(''):
        #     return True



        count_true = 0


        # logger['level_id'] = int
        #
        # if logger['level_id'] == UserLevel.seq:
        #
        #     permissions = UserLevel.permissions
        permissions = logger['level']['permissions']


        for or_conditions in and_conditions:

            if isinstance(or_conditions, int):
                if self.permit_level(or_conditions):
                    count_true += 1
                continue

            or_conditions = or_conditions.split(',')

            for or_condition in or_conditions:
                or_condition = or_condition.strip()

                break_segment = False

                if self.is_level(or_condition):
                    if self.permit_level(or_condition):
                        count_true += 1
                        break_segment = True
                else:
                    segments = or_condition.split('/')
                    index = 0

                    for segment in segments:
                        index += 1
                        logger = _user.get_logger()

                        path = '/'.join(segments[0:index])
                        if path in permissions:
                            count_true += 1
                            break_segment = True
                            break

                if break_segment:
                    break

        return len(and_conditions) == count_true

    def is_level(self, level):
        """ 등급 표현인지 확인

        ```python
            is_level(10)
            is_level('10')
            is_level('hyper')
            is_level('super')
            is_level('admin')
            is_level('root')
        ```
        """
        return isinstance(level, int) or (
                isinstance(level, str) and (
                level.isnumeric() or level in USER_LEVEL_TITLES
        )
        )

    def permit_level(self, level):
        """ 로그인한 사용자의 등급 확인

        ```python
            _permission = use(UserPermissionService)
            _permission.permit_level(1)
            _permission.permit_level(2)
            _permission.permit_level('hyper')
            _permission.permit_level('super')
            _permission.permit_level('admin')
            _permission.permit_level('root')
        ```
        """

        logger = _user.get_logger()

        print(logger)

        if not logger:
            return False

        if isinstance(level, str):
            level = level.lower()
            if level in USER_LEVEL_TITLES:
                level = USER_LEVEL_TITLES[level]
        return logger['level_id'] >= level.id
        # return logger('level_id') >= level
        # return logger['is_level'] == level
