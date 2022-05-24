# import datetime
#
# from DateTime import DateTime
from sqlalchemy import Column, String

from core.framework.model import Model, Extend, Seq, Inserted
from core.models import IpType
from modules.user.globals import USER_ACCOUNT_ID_TYPE, USER_ACCOUNT_NAME_TYPE


class UserActiveHistory(Model, Extend, Seq, Inserted):
    __tablename__ = 'user_active_histories'
    user_id = Column(USER_ACCOUNT_ID_TYPE)
    user_name = Column(USER_ACCOUNT_NAME_TYPE)
    user_extra = Column(String(50))
    os = Column(String(100))
    os_version = Column(String(255))
    browser = Column(String(50))
    browser_version = Column(String(50))
    ip = Column(IpType)