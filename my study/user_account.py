from sqlalchemy import Column, String, ForeignKey, TEXT
from sqlalchemy.orm import synonym, relationship

from core.framework.model import Model, Extend, Timestamp, Seq
from core.framework.service import use
from core.models import EmailType, TelType
from modules.user.globals import USER_ACCOUNT_TABLE_NAME, USER_ACCOUNT_ID_TYPE, USER_ACCOUNT_NAME_TYPE
from modules.user.models import UserLevelType
from modules.user.models.user_level import UserLevel
from modules.user.services.user_account_service import UserAccountService


class UserAccount(Model, Extend, Seq, Timestamp):
    __tablename__ = USER_ACCOUNT_TABLE_NAME

    string_key_ = 'id'

    join_ = {
        'level': ['id', 'permissions']
    }

    json_excludes_ = [
        'level_id',
        'password'
    ]

    id = Column(USER_ACCOUNT_ID_TYPE, unique=True, nullable=False)
    email = Column(EmailType)
    name = Column(USER_ACCOUNT_NAME_TYPE)
    phone = Column(TelType)

    ##############################
    # PASSWORD
    _password = Column('password', String(255), nullable=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = use(UserAccountService).get_password(value)

    password = synonym('_password', descriptor=password)

    ##############################
    # LEVEL
    level_seq = Column(UserLevelType, ForeignKey(UserLevel.seq))
    level = relationship(UserLevel)

    ##############################
    # PERMISSIONS
    _permissions = Column('permissions', TEXT)

    @property
    def permissions(self):
        if self._permissions:
            return self._permissions.split(',')
        return []

    @permissions.setter
    def permissions(self, value):
        if isinstance(value, list):
            value = ','.join(value)
        self._permissions = value

    permissions = synonym('_permissions', descriptor=permissions)
