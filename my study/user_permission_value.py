from sqlalchemy import Column, String, Boolean, BIGINT, Integer, TEXT, Text

from core.framework.model import Model, Extend, Timestamp, Seq


class UserPermissionValue(Model, Extend, Timestamp, Seq):
    __tablename__ = 'user_permission_values'

    permission_seq = Column(Integer)
    value = Column(Text)
