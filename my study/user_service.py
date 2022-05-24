from typing import List, Callable

from flask import session, request
from termcolor import colored

from core.framework.service import Usable, use
from core.services.db import DB
from modules.user.models.user_active_history import UserActiveHistory

_db = use(DB)


class UserService(Usable):
    _LOGIN_CALLBACKS: List[Callable]

    def __init__(self):
        self._db = use(DB)
        self._LOGIN_CALLBACKS = []

    def _on_built(self):
        @self.add_login_listener
        def create_user_active_history(user):
            _db.created(
                UserActiveHistory,
                {
                    'user_id': user.id,
                    'user_name': user.name,
                    'ip': request.remote_addr,
                    'browser': request.user_agent.browser,
                    'browser_version': request.user_agent.version,
                    'os': request.user_agent.platform,
                    'os_version': request.user_agent.string
                    # todo: os_version
                }
            )

    def add_login_listener(self, callback: Callable):
        self._log('Register Login Callback:', colored(callback.__name__, 'magenta'))
        self._LOGIN_CALLBACKS.append(callback)

    def set_logger(self, user):
        """ 로그인 사용자 정보 세션에 등록 """

        logger = user.to_json()
        logger['permissions'] = logger['permissions'] + logger['level']['permissions']

        session.__setitem__('logger', logger)

        login_callbacks = self._LOGIN_CALLBACKS
        for login_callback in login_callbacks:
            login_callback(user)

    def get_logger(self):
        if 'logger' not in session:
            return None

        logger = session['logger']

        return logger

    def logout(self):
        if 'logger' in session:
            session.__delitem__('logger')
