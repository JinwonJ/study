from sqlalchemy import Column, String, Boolean, text
from sqlalchemy.sql import expression

from core.framework.model import Model, Extend, Timestamp, Seq


class UserPermission(Model, Extend, Timestamp, Seq):
    __tablename__ = 'user_permissions'
    id = Column(String(50), unique=True)
    name = Column(String(50), nullable=True)
    name_en = Column(String(50), nullable=True)
    use_value = Column(Boolean, default=False, server_default=expression.false())

