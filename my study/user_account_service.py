from flask_bcrypt import check_password_hash
from sqlalchemy import text

from core.framework.service import Usable, use
from core.services.db import DB
from modules.user.globals import USER_ACCOUNT_TABLE_NAME
from modules.user.utils import get_hashed_password


class UserAccountService(Usable):
    def __init__(self):
        self._db = use(DB)

    def get_password(self, value):
        return get_hashed_password(value)

    def check_password(self, id_or_account, password: str):
        if isinstance(id_or_account, str):
            query = f"""
                SELECT password
                FROM {USER_ACCOUNT_TABLE_NAME}
                WHERE
                    id = :key
            """
            id_ = id_or_account
            result, = self._db.engine.execute(text(query), key=id_)

            if not result:
                return False

            hashed_password = result[0]

        else:
            account = id_or_account
            hashed_password = getattr(account, 'password')

            if not hashed_password:
                raise ValueError('Account Model has not Password Attribute')

        # password does not required make to hash
        return check_password_hash(hashed_password, password)
